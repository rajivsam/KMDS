import os
from pathlib import Path
from typing import Callable, Optional

from pandas import DataFrame

from kmds.ontology.kmds_ontology import (
    KnowledgeApplicationWorkflow,
    KnowledgeExtractionExperimentationWorkflow,
)
from kmds.utils.load_utils import (
    get_workflow,
    load_data_rep_observations,
    load_exp_observations,
    load_kb,
    load_model_selection_observations,
    load_modelling_choice_observations,
)


def _sorted_findings(df: DataFrame, max_items: int) -> list[str]:
    if df is None or df.shape[0] == 0:
        return []
    sorted_df = df.sort_values("finding_seq")
    findings = sorted_df["finding"].astype(str).tolist()
    return findings[:max_items]


def extract_kg_snapshot(kb_path: str, max_findings_per_section: int = 3) -> dict:
    """Extract structured content from a KMDS knowledge graph."""
    onto = load_kb(kb_path)
    if onto is None:
        raise ValueError(f"Could not load knowledge graph from {kb_path}")

    workflow = get_workflow(onto)
    if workflow is None:
        raise ValueError("No workflow instance found in the knowledge graph")

    if isinstance(workflow, KnowledgeApplicationWorkflow):
        workflow_type = "Application Workflow"
    elif isinstance(workflow, KnowledgeExtractionExperimentationWorkflow):
        workflow_type = "Experimental Workflow"
    else:
        workflow_type = "Workflow"

    df_exp = load_exp_observations(onto)
    df_dr = load_data_rep_observations(onto)
    df_mc = load_modelling_choice_observations(onto)
    df_ms = load_model_selection_observations(onto)

    snapshot = {
        "workflow_id": str(getattr(workflow, "name", "workflow")),
        "workflow_type": workflow_type,
        "description": getattr(workflow, "description", "") or "",
        "counts": {
            "exploration": int(df_exp.shape[0]),
            "data_representation": int(df_dr.shape[0]),
            "modelling_choice": int(df_mc.shape[0]),
            "model_selection": int(df_ms.shape[0]),
        },
        "highlights": {
            "exploration": _sorted_findings(df_exp, max_findings_per_section),
            "data_representation": _sorted_findings(df_dr, max_findings_per_section),
            "modelling_choice": _sorted_findings(df_mc, max_findings_per_section),
            "model_selection": _sorted_findings(df_ms, max_findings_per_section),
        },
    }
    return snapshot


def _compose_non_technical_summary(snapshot: dict) -> str:
    counts = snapshot["counts"]
    highlights = snapshot["highlights"]

    def _fmt(items: list[str]) -> str:
        if not items:
            return "No notable items were logged in this area yet."
        return " ".join(f"- {item}" for item in items)

    total = sum(counts.values())
    summary = (
        "Executive Summary\n"
        "=================\n\n"
        f"Project Type: {snapshot['workflow_type']}\n"
        f"Workflow Identifier: {snapshot['workflow_id']}\n"
        f"Total Logged Observations: {total}\n\n"
        "What this means in plain language:\n"
        "This project record captures what the team learned while understanding data, "
        "preparing it, making modelling decisions, and evaluating outcomes.\n\n"
        "Highlights by stage:\n"
        f"1. Exploration ({counts['exploration']} items): {_fmt(highlights['exploration'])}\n"
        f"2. Data Representation ({counts['data_representation']} items): {_fmt(highlights['data_representation'])}\n"
        f"3. Modelling Choices ({counts['modelling_choice']} items): {_fmt(highlights['modelling_choice'])}\n"
        f"4. Model Selection ({counts['model_selection']} items): {_fmt(highlights['model_selection'])}\n\n"
        "Executive takeaway:\n"
        "The knowledge graph provides a traceable record of project rationale and findings, "
        "which supports better governance, continuity between teams, and faster decision-making."
    )
    return summary


def _compose_non_technical_markdown_summary(snapshot: dict) -> str:
    counts = snapshot["counts"]
    highlights = snapshot["highlights"]

    def _fmt(items: list[str]) -> str:
        if not items:
            return "- No notable items were logged in this area yet."
        return "\n".join(f"- {item}" for item in items)

    total = sum(counts.values())
    summary = (
        "# Executive Summary\n\n"
        f"- **Project Type:** {snapshot['workflow_type']}\n"
        f"- **Workflow Identifier:** {snapshot['workflow_id']}\n"
        f"- **Total Logged Observations:** {total}\n\n"
        "## What this means in plain language\n"
        "This project record captures what the team learned while understanding data, "
        "preparing it, making modelling decisions, and evaluating outcomes.\n\n"
        "## Highlights by stage\n"
        f"### 1. Exploration ({counts['exploration']} items)\n{_fmt(highlights['exploration'])}\n\n"
        f"### 2. Data Representation ({counts['data_representation']} items)\n{_fmt(highlights['data_representation'])}\n\n"
        f"### 3. Modelling Choices ({counts['modelling_choice']} items)\n{_fmt(highlights['modelling_choice'])}\n\n"
        f"### 4. Model Selection ({counts['model_selection']} items)\n{_fmt(highlights['model_selection'])}\n\n"
        "## Executive takeaway\n"
        "The knowledge graph provides a traceable record of project rationale and findings, "
        "which supports better governance, continuity between teams, and faster decision-making."
    )
    return summary


def _build_llm_prompt(snapshot: dict) -> str:
    counts = snapshot["counts"]
    highlights = snapshot["highlights"]
    return (
        "You are writing for non-technical executives. "
        "Write a concise, non-technical executive summary in plain English. "
        "Avoid jargon and avoid implementation details. "
        "Use short sections and bullet points.\n\n"
        f"Workflow type: {snapshot['workflow_type']}\n"
        f"Workflow identifier: {snapshot['workflow_id']}\n"
        f"Counts: exploration={counts['exploration']}, data_representation={counts['data_representation']}, "
        f"modelling_choice={counts['modelling_choice']}, model_selection={counts['model_selection']}\n"
        f"Exploration highlights: {highlights['exploration']}\n"
        f"Data representation highlights: {highlights['data_representation']}\n"
        f"Modelling choice highlights: {highlights['modelling_choice']}\n"
        f"Model selection highlights: {highlights['model_selection']}\n"
    )


def _generate_with_google_genai(prompt: str, model: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is required for Google GenAI summary generation")

    from google import genai

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=model, contents=prompt)
    text = getattr(response, "text", None)
    if text is None or not str(text).strip():
        raise ValueError("Google GenAI returned an empty response")
    return str(text).strip()


def generate_executive_summary(
    kb_path: str,
    *,
    use_llm: bool = False,
    llm_fn: Optional[Callable[[str], str]] = None,
    model: str = "gemini-1.5-flash",
    max_findings_per_section: int = 3,
    summary_format: str = "text",
) -> str:
    """Generate a non-technical executive summary from a knowledge graph."""
    snapshot = extract_kg_snapshot(kb_path, max_findings_per_section=max_findings_per_section)
    if summary_format not in {"text", "markdown"}:
        raise ValueError("summary_format must be either 'text' or 'markdown'")

    fallback = (
        _compose_non_technical_markdown_summary(snapshot)
        if summary_format == "markdown"
        else _compose_non_technical_summary(snapshot)
    )

    if not use_llm:
        return fallback

    prompt = _build_llm_prompt(snapshot)
    prompt = (
        prompt
        + f"\nRequired output format: {summary_format}. "
        + "If markdown, use headings and bullet points. If text, use plain text headings."
    )
    try:
        if llm_fn is not None:
            return llm_fn(prompt)
        return _generate_with_google_genai(prompt, model)
    except Exception:
        return fallback


def export_executive_summary(
    kb_path: str,
    output_file: str,
    *,
    use_llm: bool = False,
    llm_fn: Optional[Callable[[str], str]] = None,
    model: str = "gemini-1.5-flash",
    max_findings_per_section: int = 3,
    summary_format: str = "text",
) -> str:
    """Generate and write an executive summary to disk."""
    summary = generate_executive_summary(
        kb_path,
        use_llm=use_llm,
        llm_fn=llm_fn,
        model=model,
        max_findings_per_section=max_findings_per_section,
        summary_format=summary_format,
    )
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(summary, encoding="utf-8")
    return str(output_path)
