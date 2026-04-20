from kmds.ontology.kmds_ontology import (
    KnowledgeApplicationWorkflow,
    KnowledgeExtractionExperimentationWorkflow,
    PipelineType,
)
from kmds.tagging.tag_types import ExploratoryTags
from kmds.utils.summary_logger import infer_workflow_type, log_exploratory_summary


def test_infer_workflow_type_experimental():
    summary = "We will run multiple experiments to compare candidate models and evaluate hypotheses."
    inferred = infer_workflow_type(summary, prompt_on_ambiguity=False)
    assert inferred == PipelineType.KNOWLEDGE_EXTRACTION_EXPERIMENT_WORKFLOW


def test_infer_workflow_type_application():
    summary = "This is a scheduled reporting application with an established dashboard pipeline."
    inferred = infer_workflow_type(summary, prompt_on_ambiguity=False)
    assert inferred == PipelineType.KNOWLEDGE_APPLICATION_WORKFLOW


def test_infer_workflow_type_ambiguous_prompts_user():
    summary = "We are starting a new project and gathering notes from teams."
    inferred = infer_workflow_type(
        summary,
        prompt_on_ambiguity=True,
        input_fn=lambda _: "experimental",
    )
    assert inferred == PipelineType.KNOWLEDGE_EXTRACTION_EXPERIMENT_WORKFLOW


def test_log_exploratory_summary_creates_workflow_and_observations():
    summary = (
        "We run experiments to compare feature sets. "
        "There are missing values in customer age. "
        "The selected fields look relevant for segmentation."
    )
    wf = log_exploratory_summary(
        project_summary=summary,
        workflow_name="business analyst intake",
        prompt_on_ambiguity=False,
    )

    assert isinstance(wf, KnowledgeExtractionExperimentationWorkflow)
    assert len(wf.has_exploratory_observations) >= 2
    obs_types = [o.exploratory_observation_type for o in wf.has_exploratory_observations]
    assert ExploratoryTags.DATA_QUALITY_OBSERVATION.value in obs_types


def test_log_exploratory_summary_appends_to_existing_workflow():
    existing = KnowledgeApplicationWorkflow("summary_logger_existing_app")
    wf = log_exploratory_summary(
        project_summary="This production workflow runs daily reporting for operations.",
        workflow_name="daily_ops",
        workflow=existing,
        prompt_on_ambiguity=False,
    )
    initial_count = len(wf.has_exploratory_observations)

    wf = log_exploratory_summary(
        project_summary="Data quality issue: missing product category labels in feed.",
        workflow_name="daily_ops",
        workflow=existing,
        prompt_on_ambiguity=False,
        workflow_type="application",
    )
    assert len(wf.has_exploratory_observations) > initial_count
    sequences = [obs.finding_sequence for obs in wf.has_exploratory_observations]
    assert sequences == sorted(sequences)
