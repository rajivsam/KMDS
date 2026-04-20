import re
from typing import Callable, List, Optional

from kmds.ontology.kmds_ontology import (
    ExploratoryObservation,
    KnowledgeApplicationWorkflow,
    KnowledgeExtractionExperimentationWorkflow,
    PipelineType,
    Workflow,
)
from kmds.tagging.tag_types import ExploratoryTags


APPLICATION_KEYWORDS = {
    "application",
    "production",
    "deploy",
    "deployment",
    "reporting",
    "dashboard",
    "operational",
    "routine",
    "cadence",
    "scheduled",
    "established",
}

EXPERIMENT_KEYWORDS = {
    "experiment",
    "experimental",
    "hypothesis",
    "evaluate",
    "comparison",
    "compare",
    "benchmark",
    "prototype",
    "trial",
    "ablation",
    "tuning",
}

DATA_QUALITY_KEYWORDS = {
    "missing",
    "null",
    "na",
    "outlier",
    "duplicate",
    "inconsistent",
    "error",
    "noise",
    "quality",
}


def _safe_identifier(name: str, suffix: str = "") -> str:
    base = re.sub(r"[^a-zA-Z0-9_]+", "_", name.strip()).strip("_")
    if not base:
        base = "workflow"
    return f"{base}{suffix}"


def _parse_pipeline_type(value: str) -> Optional[PipelineType]:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"application", "app", "knowledge application workflow"}:
        return PipelineType.KNOWLEDGE_APPLICATION_WORKFLOW
    if normalized in {
        "experimental",
        "experiment",
        "knowledge extraction experiment workflow",
    }:
        return PipelineType.KNOWLEDGE_EXTRACTION_EXPERIMENT_WORKFLOW
    return None


def infer_workflow_type(
    project_summary: str,
    workflow_type: Optional[str] = None,
    prompt_on_ambiguity: bool = True,
    input_fn: Callable[[str], str] = input,
) -> PipelineType:
    """Infer workflow type from free text.

    If classification is ambiguous and prompt_on_ambiguity is True, this function
    asks the user to choose application or experimental.
    """
    explicit_type = _parse_pipeline_type(workflow_type) if workflow_type else None
    if explicit_type is not None:
        return explicit_type

    tokens = re.findall(r"[a-zA-Z]+", project_summary.lower())
    app_score = sum(1 for tok in tokens if tok in APPLICATION_KEYWORDS)
    exp_score = sum(1 for tok in tokens if tok in EXPERIMENT_KEYWORDS)

    if app_score > exp_score:
        return PipelineType.KNOWLEDGE_APPLICATION_WORKFLOW
    if exp_score > app_score:
        return PipelineType.KNOWLEDGE_EXTRACTION_EXPERIMENT_WORKFLOW

    if not prompt_on_ambiguity:
        raise ValueError(
            "Could not infer workflow type from summary. Provide workflow_type or enable prompting."
        )

    user_choice = input_fn(
        "Could not determine workflow type from summary. Enter 'application' or 'experimental': "
    )
    resolved = _parse_pipeline_type(user_choice)
    if resolved is None:
        raise ValueError(
            "Invalid workflow type input. Expected 'application' or 'experimental'."
        )
    return resolved


def parse_exploratory_findings(project_summary: str) -> List[str]:
    """Extract candidate findings from a block of summary text."""
    chunks = re.split(r"[\n\r]+|[.;]", project_summary)
    findings = []
    for chunk in chunks:
        item = re.sub(r"^[-*\d\)\(\s]+", "", chunk.strip())
        if len(item) >= 6:
            findings.append(item)

    if not findings and project_summary.strip():
        findings = [project_summary.strip()]
    return findings


def infer_exploratory_observation_type(finding: str) -> str:
    """Classify exploratory finding as data quality or relevance."""
    tokens = re.findall(r"[a-zA-Z]+", finding.lower())
    has_quality_signal = any(tok in DATA_QUALITY_KEYWORDS for tok in tokens)
    if has_quality_signal:
        return ExploratoryTags.DATA_QUALITY_OBSERVATION.value
    return ExploratoryTags.RELEVANCE_OBSERVATION.value


def _create_workflow_instance(
    workflow_name: str, pipeline_type: PipelineType
) -> Workflow:
    if pipeline_type == PipelineType.KNOWLEDGE_APPLICATION_WORKFLOW:
        next_id = len(KnowledgeApplicationWorkflow.instances()) + 1
        identifier = _safe_identifier(workflow_name, f"_app_{next_id}")
        return KnowledgeApplicationWorkflow(identifier)

    next_id = len(KnowledgeExtractionExperimentationWorkflow.instances()) + 1
    identifier = _safe_identifier(workflow_name, f"_exp_{next_id}")
    return KnowledgeExtractionExperimentationWorkflow(identifier)


def log_exploratory_summary(
    project_summary: str,
    workflow_name: str,
    workflow: Optional[Workflow] = None,
    workflow_type: Optional[str] = None,
    prompt_on_ambiguity: bool = True,
    input_fn: Callable[[str], str] = input,
    intent: Optional[str] = None,
) -> Workflow:
    """Create/update a workflow and append exploratory observations from summary text."""
    if project_summary is None or not project_summary.strip():
        raise ValueError("project_summary must be a non-empty string")

    pipeline_type = infer_workflow_type(
        project_summary=project_summary,
        workflow_type=workflow_type,
        prompt_on_ambiguity=prompt_on_ambiguity,
        input_fn=input_fn,
    )

    target_workflow = workflow
    if target_workflow is None:
        target_workflow = _create_workflow_instance(workflow_name, pipeline_type)

    target_workflow.description = project_summary.strip()
    findings = parse_exploratory_findings(project_summary)

    existing = list(target_workflow.has_exploratory_observations)
    next_sequence = len(existing) + 1

    for finding in findings:
        obs = ExploratoryObservation()
        obs.finding = finding
        obs.finding_sequence = next_sequence
        obs.exploratory_observation_type = infer_exploratory_observation_type(finding)
        if intent is not None:
            obs.intent = intent
        existing.append(obs)
        next_sequence += 1

    target_workflow.has_exploratory_observations = existing
    return target_workflow
