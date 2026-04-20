"""LLM-driven search orchestrator for KMDS knowledge bases.

The orchestrator uses an LLM as a *router* to map a natural language user
query to one of the structured observation-category search templates, executes
the matched template, and synthesises the raw results into a concise natural
language answer.

If the query cannot be mapped to any specific template the system falls back
to semantic vector search across all indexed observations (ChromaDB + sentence-
transformers).

Architecture
------------
**Step 1 – Context Injection**
    A ``tool description`` string that lists every available API template and
    its purpose is injected into the LLM routing prompt so the model always
    knows its options.

**Step 2 – Intent Classification & Entity Extraction** *(LLM router)*
    The LLM returns a Pydantic-validated JSON payload identifying:

    * ``intent_class`` – which observation-category template to invoke.
    * ``filters`` – optional parameters extracted from the query text (obs type,
      keyword, sequence range).
    * ``explanation`` – one-sentence rationale for transparency.

**Step 3 – Template Execution**
    The corresponding KMDS API function is called with the extracted filters.

**Step 4 – LLM Synthesis**
    The LLM converts the raw observation records into a readable answer.

**Step 5 – Semantic Fallback** *(catch-all)*
    When no template matches, or when the LLM or a template returns no results,
    the SemanticIndex is queried instead.
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Callable, Literal, Optional

from pydantic import BaseModel, ValidationError

from kmds.search.semantic_index import SemanticIndex
from kmds.utils.load_utils import (
    load_data_rep_observations,
    load_exp_observations,
    load_kb,
    load_model_selection_observations,
    load_modelling_choice_observations,
    load_observations,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Pydantic schema for the LLM router output
# ---------------------------------------------------------------------------

IntentClass = Literal[
    "exploratory_search",
    "data_representation_search",
    "modelling_choice_search",
    "model_selection_search",
    "all_observations_search",
    "semantic_search",
]


class SearchFilters(BaseModel):
    """Optional parameters the LLM may extract from the user query.

    All fields are optional.  Any field left as ``None`` is ignored during
    the post-retrieval filtering step.
    """

    obs_type_filter: Optional[str] = None
    """Substring to match against the observation-type label (case-insensitive)."""

    finding_seq_min: Optional[int] = None
    """Include only observations with ``finding_seq`` >= this value."""

    finding_seq_max: Optional[int] = None
    """Include only observations with ``finding_seq`` <= this value."""

    keyword: Optional[str] = None
    """Additional keyword to filter the finding text (case-insensitive substring)."""


class OrchestratorRoute(BaseModel):
    """Structured output produced by the LLM router.

    The LLM is instructed to return a JSON object that conforms to this
    schema.  Pydantic validates and coerces the payload before execution.
    """

    intent_class: IntentClass
    """Which search template best matches the user query."""

    filters: SearchFilters = SearchFilters()
    """Optional query parameters extracted from the query text."""

    explanation: str = ""
    """Brief explanation of why this route was chosen (surfaced to the caller)."""


# ---------------------------------------------------------------------------
# Tool descriptions – injected verbatim into the LLM routing prompt
# ---------------------------------------------------------------------------

_TOOL_DESCRIPTIONS: dict[str, str] = {
    "exploratory_search": (
        "Search exploratory / EDA observations. Use for questions about data "
        "quality, relevance, missing values, outliers, distributions, or "
        "initial data understanding."
    ),
    "data_representation_search": (
        "Search data representation observations. Use for questions about "
        "feature engineering, data transformations, encodings, scaling, or "
        "preparation of data for modelling."
    ),
    "modelling_choice_search": (
        "Search modelling choice observations. Use for questions about "
        "algorithm selection rationale, modelling assumptions, hyperparameter "
        "decisions, or pipeline design choices."
    ),
    "model_selection_search": (
        "Search model selection observations. Use for questions about model "
        "comparison, evaluation metrics, benchmarking results, or the final "
        "model recommendation."
    ),
    "all_observations_search": (
        "Search across ALL observation types. Use for broad questions that "
        "span multiple workflow phases, or when the intent cannot be narrowed "
        "to a single category."
    ),
    "semantic_search": (
        "Semantic vector similarity search (fallback). Use when the query does "
        "not clearly map to a specific workflow phase, or when nuanced "
        "natural-language similarity matching is needed."
    ),
}

_ROUTER_SYSTEM_PROMPT = """\
You are a search router for a knowledge management system (KMDS) that stores
data science project observations (findings, decisions, results) as a
knowledge graph.

Available search templates:
{tool_descriptions}

For the user query below, return a JSON object (and NOTHING else) with these
exact fields:
  "intent_class" : one of {intent_classes}
  "filters"      : an object with zero or more of:
                     "obs_type_filter"  (string, optional)
                     "finding_seq_min"  (integer, optional)
                     "finding_seq_max"  (integer, optional)
                     "keyword"          (string, optional)
  "explanation"  : a single sentence explaining your choice

Reply with ONLY valid JSON.  Do not include markdown fences or prose.
"""

_SYNTHESIS_SYSTEM_PROMPT = """\
You are a helpful assistant explaining data science project knowledge-base
search results in clear, concise natural language.

User question: {query}

The search used the "{intent_class}" template and returned {n} result(s):

{results_text}

Write a concise answer (3–10 sentences).  Group related findings where
possible.  Do not add information absent from the results above.
If there are no results, say so clearly.
"""


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


class OrchestratorResult:
    """Result returned by :meth:`SearchOrchestrator.ask`.

    Attributes
    ----------
    answer:
        Synthesised natural language answer.
    intent_class:
        The search template that was ultimately executed.
    route_explanation:
        The LLM's own explanation for its routing choice.
    results:
        Raw observation record dicts that informed the answer.
    """

    def __init__(
        self,
        answer: str,
        intent_class: str,
        route_explanation: str,
        results: list[dict[str, Any]],
    ) -> None:
        self.answer = answer
        self.intent_class = intent_class
        self.route_explanation = route_explanation
        self.results = results

    def __repr__(self) -> str:
        snippet = (self.answer[:77] + "...") if len(self.answer) > 80 else self.answer
        return (
            f"OrchestratorResult("
            f"intent={self.intent_class!r}, "
            f"n_results={len(self.results)}, "
            f"answer={snippet!r})"
        )


# ---------------------------------------------------------------------------
# Main orchestrator class
# ---------------------------------------------------------------------------


class SearchOrchestrator:
    """LLM-driven search orchestrator for a KMDS knowledge base.

    The orchestrator routes natural language queries through an LLM to
    identify the best search template, executes it against the loaded
    knowledge base, and synthesises the results into a natural language
    answer.

    Parameters
    ----------
    kb_path:
        Path to the KMDS ``.xml`` knowledge-base file.
    persist_dir:
        Directory to persist the semantic vector index.  ``None`` keeps the
        index in memory (rebuilt on each interpreter session).
    llm_fn:
        Optional callable ``(prompt: str) -> str`` for your own LLM backend.
        If ``None``, the orchestrator uses Google GenAI (requires
        ``GOOGLE_API_KEY`` environment variable).
    model:
        Google GenAI model name (ignored when *llm_fn* is supplied).
    embedding_model:
        Sentence-transformers model used for the semantic fallback index.
    n_results:
        Default maximum number of observation records returned per query.

    Examples
    --------
    Using Google GenAI (default)::

        import os
        os.environ["GOOGLE_API_KEY"] = "your-key"

        from kmds.search import SearchOrchestrator

        orc = SearchOrchestrator("my_project.xml", persist_dir="./idx")
        result = orc.ask("What data quality issues were found?")
        print(result.answer)

    Using a custom LLM backend::

        def my_llm(prompt: str) -> str:
            # call any LLM here
            return my_model.generate(prompt)

        orc = SearchOrchestrator("my_project.xml", llm_fn=my_llm)
        result = orc.ask("Which model was selected and why?")
        print(result.answer)
        print(result.results)      # raw records
    """

    def __init__(
        self,
        kb_path: str,
        *,
        persist_dir: Optional[str] = None,
        llm_fn: Optional[Callable[[str], str]] = None,
        model: str = "gemini-1.5-flash",
        embedding_model: str = SemanticIndex.DEFAULT_MODEL,
        n_results: int = 5,
    ) -> None:
        self._kb_path = kb_path
        self._llm_fn = llm_fn
        self._model = model
        self._n_results = n_results

        # Load the ontology once and keep it alive for the session.
        self._onto = load_kb(kb_path)
        if self._onto is None:
            raise ValueError(f"Could not load knowledge base from '{kb_path}'")

        # Build (or reload from disk) the semantic fallback index.
        self._index = SemanticIndex(
            persist_dir=persist_dir,
            model_name=embedding_model,
        )
        if self._index.count() == 0:
            self._index.build_from_onto(self._onto)

    # ------------------------------------------------------------------
    # LLM helpers
    # ------------------------------------------------------------------

    def _call_llm(self, prompt: str) -> str:
        """Invoke the configured LLM and return its raw text response."""
        if self._llm_fn is not None:
            return self._llm_fn(prompt)
        return self._call_google_genai(prompt)

    def _call_google_genai(self, prompt: str) -> str:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY environment variable is not set. "
                "Set it or supply llm_fn= to SearchOrchestrator()."
            )
        from google import genai  # noqa: PLC0415 – optional dependency

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=self._model, contents=prompt
        )
        text = getattr(response, "text", None)
        if not text or not str(text).strip():
            raise ValueError("LLM returned an empty response.")
        return str(text).strip()

    # ------------------------------------------------------------------
    # Routing
    # ------------------------------------------------------------------

    def _build_router_prompt(self, query: str) -> str:
        tool_lines = "\n".join(
            f'  "{k}": {v}' for k, v in _TOOL_DESCRIPTIONS.items()
        )
        intent_classes = json.dumps(list(_TOOL_DESCRIPTIONS.keys()))
        system = _ROUTER_SYSTEM_PROMPT.format(
            tool_descriptions=tool_lines,
            intent_classes=intent_classes,
        )
        return f"{system}\n\nUser query: {query}"

    def _parse_route(self, llm_response: str) -> OrchestratorRoute:
        """Parse and validate the LLM router JSON response.

        On any parse or validation error the method logs a warning and
        returns a ``semantic_search`` fallback route.
        """
        # Strip accidental markdown code fences that some models add.
        cleaned = re.sub(r"```[a-z]*\n?", "", llm_response).strip()
        try:
            data = json.loads(cleaned)
            return OrchestratorRoute.model_validate(data)
        except (json.JSONDecodeError, ValidationError) as exc:
            logger.warning(
                "LLM router returned an unparseable response (%s); "
                "falling back to semantic_search.\nRaw: %s",
                exc,
                llm_response[:300],
            )
            return OrchestratorRoute(
                intent_class="semantic_search",
                explanation="Fallback – router response could not be parsed.",
            )

    # ------------------------------------------------------------------
    # Template execution
    # ------------------------------------------------------------------

    def _apply_filters(
        self, records: list[dict[str, Any]], filters: SearchFilters
    ) -> list[dict[str, Any]]:
        """Apply optional post-retrieval filters extracted by the LLM."""
        out = records
        if filters.obs_type_filter:
            needle = filters.obs_type_filter.lower()
            out = [r for r in out if needle in str(r.get("obs_type", "")).lower()]
        if filters.keyword:
            needle = filters.keyword.lower()
            out = [
                r for r in out if needle in str(r.get("finding", "")).lower()
            ]
        if filters.finding_seq_min is not None:
            out = [
                r
                for r in out
                if int(r.get("finding_seq") or 0) >= filters.finding_seq_min
            ]
        if filters.finding_seq_max is not None:
            out = [
                r
                for r in out
                if int(r.get("finding_seq") or 0) <= filters.finding_seq_max
            ]
        return out

    _LOADERS: dict[str, Any] = {
        "exploratory_search": load_exp_observations,
        "data_representation_search": load_data_rep_observations,
        "modelling_choice_search": load_modelling_choice_observations,
        "model_selection_search": load_model_selection_observations,
        "all_observations_search": load_observations,
    }

    def _execute_template(
        self, route: OrchestratorRoute, query: str
    ) -> tuple[list[dict[str, Any]], str]:
        """Run the selected API template.

        Returns
        -------
        tuple[list[dict], str]
            ``(records, intent_class_actually_used)``
        """
        intent = route.intent_class

        # ----- Semantic fallback path -----
        if intent == "semantic_search":
            raw = self._index.search(query, n_results=self._n_results)
            return raw, "semantic_search"

        # ----- Structured template path -----
        loader = self._LOADERS.get(intent)
        if loader is None:
            logger.warning(
                "Unknown intent_class '%s'; falling back to semantic_search.", intent
            )
            return self._index.search(query, n_results=self._n_results), "semantic_search"

        df = loader(self._onto)
        if df is None or df.shape[0] == 0:
            logger.info(
                "Template '%s' returned 0 observations; "
                "falling back to semantic_search.",
                intent,
            )
            return self._index.search(query, n_results=self._n_results), "semantic_search"

        records: list[dict[str, Any]] = df.to_dict(orient="records")
        records = self._apply_filters(records, route.filters)

        # If filters reduced results to zero, fall back.
        if not records:
            logger.info(
                "Filters on template '%s' produced 0 results; "
                "falling back to semantic_search.",
                intent,
            )
            return self._index.search(query, n_results=self._n_results), "semantic_search"

        return records[: self._n_results], intent

    # ------------------------------------------------------------------
    # Synthesis
    # ------------------------------------------------------------------

    def _build_synthesis_prompt(
        self, query: str, results: list[dict[str, Any]], intent_class: str
    ) -> str:
        if not results:
            results_text = "(No matching observations found.)"
        else:
            lines: list[str] = []
            for i, r in enumerate(results, 1):
                obs_type = r.get("obs_type", "")
                finding = r.get("finding", "")
                seq = r.get("finding_seq", "")
                intent_tag = (
                    f" [intent: {r['intent']}]" if "intent" in r else ""
                )
                lines.append(
                    f"[{i}] ({obs_type}{intent_tag}, seq={seq}): {finding}"
                )
            results_text = "\n".join(lines)

        return _SYNTHESIS_SYSTEM_PROMPT.format(
            query=query,
            n=len(results),
            intent_class=intent_class,
            results_text=results_text,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ask(self, query: str) -> OrchestratorResult:
        """Route a natural language query and return a synthesised answer.

        This is the single public entry point for the orchestrator.  It
        performs all five steps internally (routing, execution, synthesis,
        fallback) and returns an :class:`OrchestratorResult`.

        Parameters
        ----------
        query:
            Free-form natural language question about the knowledge base.

        Returns
        -------
        OrchestratorResult
        """
        # ── Step 1 & 2: Route ──────────────────────────────────────────
        try:
            router_prompt = self._build_router_prompt(query)
            llm_response = self._call_llm(router_prompt)
            route = self._parse_route(llm_response)
        except Exception as exc:
            logger.warning(
                "LLM routing call failed (%s); using semantic_search fallback.", exc
            )
            route = OrchestratorRoute(
                intent_class="semantic_search",
                explanation=f"LLM unavailable: {exc}",
            )

        logger.info(
            "Routed '%s' → '%s'  (reason: %s)",
            query,
            route.intent_class,
            route.explanation,
        )

        # ── Step 3: Execute ────────────────────────────────────────────
        results, intent_used = self._execute_template(route, query)

        # ── Step 4: Synthesise ─────────────────────────────────────────
        synthesis_prompt = self._build_synthesis_prompt(query, results, intent_used)
        try:
            answer = self._call_llm(synthesis_prompt)
        except Exception as exc:
            logger.warning(
                "LLM synthesis call failed (%s); formatting raw results.", exc
            )
            if not results:
                answer = "No matching observations were found."
            else:
                answer = "\n".join(
                    f"{i}. [{r.get('obs_type', '')}] {r.get('finding', '')}"
                    for i, r in enumerate(results, 1)
                )

        return OrchestratorResult(
            answer=answer,
            intent_class=intent_used,
            route_explanation=route.explanation,
            results=results,
        )
