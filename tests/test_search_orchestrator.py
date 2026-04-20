"""Tests for the SearchOrchestrator feature.

The orchestrator depends on an LLM for routing and synthesis, so tests use
a deterministic ``llm_fn`` mock instead of live API calls.  This keeps the
test suite fast, hermetic, and runnable without credentials.

Mock strategy
-------------
* The *router* mock returns a valid JSON route payload.
* The *synthesis* mock returns a canned answer string.
* Both are delivered by a single ``llm_fn`` that inspects the prompt to decide
  which role it is playing (router call contains ``intent_class``;
  synthesis call contains ``synthesise``/``answer``).
"""

import json
from typing import Callable

import pytest

from kmds.search.search_orchestrator import (
    OrchestratorResult,
    OrchestratorRoute,
    SearchFilters,
    SearchOrchestrator,
)
from kmds.utils.path_utils import get_kb_file_path

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_llm_fn(intent_class: str = "exploratory_search") -> Callable[[str], str]:
    """Return a mock llm_fn that routes to *intent_class* and echoes synthesis."""

    router_payload = json.dumps(
        {
            "intent_class": intent_class,
            "filters": {},
            "explanation": f"Test routing to {intent_class}.",
        }
    )

    def _mock_llm(prompt: str) -> str:
        # Router call: prompt contains the intent_classes list
        if "intent_class" in prompt and "search template" in prompt:
            return router_payload
        # Synthesis call: return a canned answer
        return "Mocked synthesised answer from the knowledge base."

    return _mock_llm


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def app_kb_path():
    return get_kb_file_path("test_kb_app_workflow.xml")


@pytest.fixture()
def exp_kb_path():
    return get_kb_file_path("test_kb_exp_workflow.xml")


@pytest.fixture()
def app_orchestrator(app_kb_path):
    """Orchestrator backed by the app workflow KB, no LLM credentials needed."""
    return SearchOrchestrator(
        kb_path=app_kb_path,
        llm_fn=_make_llm_fn("exploratory_search"),
    )


# ---------------------------------------------------------------------------
# Construction tests
# ---------------------------------------------------------------------------


class TestSearchOrchestratorConstruction:
    def test_constructs_with_app_kb(self, app_kb_path):
        orc = SearchOrchestrator(
            kb_path=app_kb_path,
            llm_fn=_make_llm_fn(),
        )
        assert orc is not None

    def test_constructs_with_exp_kb(self, exp_kb_path):
        orc = SearchOrchestrator(
            kb_path=exp_kb_path,
            llm_fn=_make_llm_fn("all_observations_search"),
        )
        assert orc is not None

    def test_raises_on_bad_path(self):
        with pytest.raises(ValueError, match="Could not load"):
            SearchOrchestrator(
                kb_path="/nonexistent/path/kb.xml",
                llm_fn=_make_llm_fn(),
            )

    def test_semantic_index_is_populated(self, app_orchestrator):
        assert app_orchestrator._index.count() > 0


# ---------------------------------------------------------------------------
# Route parsing tests
# ---------------------------------------------------------------------------


class TestOrchestratorRouteParsing:
    def test_valid_json_parsed_correctly(self, app_orchestrator):
        raw = json.dumps(
            {
                "intent_class": "data_representation_search",
                "filters": {"keyword": "imputation"},
                "explanation": "Query is about data prep.",
            }
        )
        route = app_orchestrator._parse_route(raw)
        assert route.intent_class == "data_representation_search"
        assert route.filters.keyword == "imputation"

    def test_markdown_fences_stripped(self, app_orchestrator):
        raw = "```json\n{\"intent_class\": \"modelling_choice_search\", \"filters\": {}, \"explanation\": \"x\"}\n```"
        route = app_orchestrator._parse_route(raw)
        assert route.intent_class == "modelling_choice_search"

    def test_invalid_json_falls_back_to_semantic(self, app_orchestrator):
        route = app_orchestrator._parse_route("this is not json at all")
        assert route.intent_class == "semantic_search"

    def test_invalid_intent_class_falls_back(self, app_orchestrator):
        raw = json.dumps(
            {"intent_class": "nonexistent_template", "filters": {}, "explanation": ""}
        )
        route = app_orchestrator._parse_route(raw)
        assert route.intent_class == "semantic_search"

    def test_filters_with_seq_range(self, app_orchestrator):
        raw = json.dumps(
            {
                "intent_class": "exploratory_search",
                "filters": {"finding_seq_min": 2, "finding_seq_max": 5},
                "explanation": "narrow by sequence",
            }
        )
        route = app_orchestrator._parse_route(raw)
        assert route.filters.finding_seq_min == 2
        assert route.filters.finding_seq_max == 5


# ---------------------------------------------------------------------------
# Ask / integration tests (mock LLM)
# ---------------------------------------------------------------------------


class TestSearchOrchestratorAsk:
    def test_ask_returns_orchestrator_result(self, app_kb_path):
        orc = SearchOrchestrator(
            kb_path=app_kb_path,
            llm_fn=_make_llm_fn("exploratory_search"),
        )
        result = orc.ask("What data quality observations exist?")
        assert isinstance(result, OrchestratorResult)

    def test_ask_result_has_answer(self, app_kb_path):
        orc = SearchOrchestrator(
            kb_path=app_kb_path,
            llm_fn=_make_llm_fn("exploratory_search"),
        )
        result = orc.ask("data quality issues?")
        assert isinstance(result.answer, str)
        assert len(result.answer) > 0

    def test_ask_result_has_intent_class(self, app_kb_path):
        orc = SearchOrchestrator(
            kb_path=app_kb_path,
            llm_fn=_make_llm_fn("exploratory_search"),
        )
        result = orc.ask("missing values")
        assert result.intent_class in {
            "exploratory_search",
            "data_representation_search",
            "modelling_choice_search",
            "model_selection_search",
            "all_observations_search",
            "semantic_search",
        }

    def test_ask_result_has_raw_records(self, app_kb_path):
        orc = SearchOrchestrator(
            kb_path=app_kb_path,
            llm_fn=_make_llm_fn("exploratory_search"),
        )
        result = orc.ask("relevance of features")
        assert isinstance(result.results, list)

    def test_all_observations_template(self, app_kb_path):
        orc = SearchOrchestrator(
            kb_path=app_kb_path,
            llm_fn=_make_llm_fn("all_observations_search"),
        )
        result = orc.ask("give me everything")
        assert isinstance(result, OrchestratorResult)
        assert len(result.results) > 0

    def test_semantic_fallback_route(self, app_kb_path):
        """Routing directly to semantic_search should still produce a result."""
        orc = SearchOrchestrator(
            kb_path=app_kb_path,
            llm_fn=_make_llm_fn("semantic_search"),
        )
        result = orc.ask("anything at all")
        assert result.intent_class == "semantic_search"
        assert isinstance(result.results, list)

    def test_llm_failure_falls_back_gracefully(self, app_kb_path):
        """When the LLM raises, the orchestrator falls back to semantic search."""

        def _broken_llm(prompt: str) -> str:
            raise RuntimeError("Simulated LLM outage")

        orc = SearchOrchestrator(kb_path=app_kb_path, llm_fn=_broken_llm)
        result = orc.ask("feature engineering")
        # Should not raise; should fall back to semantic search
        assert isinstance(result, OrchestratorResult)
        assert result.intent_class == "semantic_search"

    def test_n_results_cap(self, app_kb_path):
        orc = SearchOrchestrator(
            kb_path=app_kb_path,
            llm_fn=_make_llm_fn("all_observations_search"),
            n_results=2,
        )
        result = orc.ask("any observation")
        assert len(result.results) <= 2

    def test_repr_is_informative(self, app_kb_path):
        orc = SearchOrchestrator(
            kb_path=app_kb_path,
            llm_fn=_make_llm_fn("exploratory_search"),
        )
        result = orc.ask("data quality")
        rep = repr(result)
        assert "OrchestratorResult" in rep
        assert "intent=" in rep


# ---------------------------------------------------------------------------
# Filter application tests
# ---------------------------------------------------------------------------


class TestFilterApplication:
    @pytest.fixture()
    def orc(self, app_kb_path):
        return SearchOrchestrator(
            kb_path=app_kb_path, llm_fn=_make_llm_fn()
        )

    def test_obs_type_filter(self, orc):
        records = [
            {"obs_type": "Data Quality Observation", "finding": "f1", "finding_seq": 1},
            {"obs_type": "Relevance Observation", "finding": "f2", "finding_seq": 2},
        ]
        f = SearchFilters(obs_type_filter="quality")
        out = orc._apply_filters(records, f)
        assert len(out) == 1
        assert out[0]["obs_type"] == "Data Quality Observation"

    def test_keyword_filter(self, orc):
        records = [
            {"obs_type": "t", "finding": "imputation strategy used", "finding_seq": 1},
            {"obs_type": "t", "finding": "outlier removal", "finding_seq": 2},
        ]
        f = SearchFilters(keyword="imputation")
        out = orc._apply_filters(records, f)
        assert len(out) == 1
        assert "imputation" in out[0]["finding"]

    def test_seq_range_filter(self, orc):
        records = [
            {"obs_type": "t", "finding": "f1", "finding_seq": 1},
            {"obs_type": "t", "finding": "f2", "finding_seq": 3},
            {"obs_type": "t", "finding": "f3", "finding_seq": 5},
        ]
        f = SearchFilters(finding_seq_min=2, finding_seq_max=4)
        out = orc._apply_filters(records, f)
        assert len(out) == 1
        assert out[0]["finding_seq"] == 3

    def test_empty_filters_pass_all(self, orc):
        records = [{"obs_type": "t", "finding": "f", "finding_seq": 1}]
        out = orc._apply_filters(records, SearchFilters())
        assert out == records
