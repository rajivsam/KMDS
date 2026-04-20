from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from kmds.ontology import kmds_ontology as ontology_model
from kmds.ontology.intent_types import IntentType
from kmds.ontology.kmds_ontology import (
    DataRepresentationObservation,
    ExperimentalObservation,
    ExploratoryObservation,
    KnowledgeApplicationWorkflow,
    KnowledgeExtractionExperimentationWorkflow,
    ModelSelectionObservation,
    ModellingChoiceObservation,
    Workflow,
)
from kmds.tagging.tag_types import (
    DataRepresentationTags,
    ExperimentationTags,
    ExploratoryTags,
    ModelSelectionTags,
    ModellingChoiceTags,
)
from kmds.utils.load_utils import get_workflow, load_kb

ObservationFamily = Literal[
    "exploratory",
    "data_representation",
    "modelling_choice",
    "model_selection",
    "experimental",
]

DEFAULT_WORKFLOW_ORDER: tuple[str, ...] = (
    "exploratory",
    "data_representation",
    "modelling_choice",
    "model_selection",
)

FAMILY_PHASE_ORDER: dict[str, Optional[int]] = {
    "exploratory": 1,
    "data_representation": 2,
    "modelling_choice": 3,
    "model_selection": 4,
    "experimental": None,
}

FAMILY_METADATA: dict[str, dict[str, Any]] = {
    "exploratory": {
        "ontology_class": ExploratoryObservation,
        "ontology_class_name": "ExploratoryObservation",
        "relationship": "has_exploratory_observations",
        "type_property": "exploratory_observation_type",
        "default_intent": IntentType.DATA_UNDERSTANDING.value,
    },
    "data_representation": {
        "ontology_class": DataRepresentationObservation,
        "ontology_class_name": "DataRepresentationObservation",
        "relationship": "has_data_representation_observations",
        "type_property": "data_representation_observation_type",
        "default_intent": IntentType.FEATURE_ASSESSMENT.value,
    },
    "modelling_choice": {
        "ontology_class": ModellingChoiceObservation,
        "ontology_class_name": "ModellingChoiceObservation",
        "relationship": "has_modeling_choice_observations",
        "type_property": "modelling_choice_observation_type",
        "default_intent": IntentType.MODEL_EXPLANATION.value,
    },
    "model_selection": {
        "ontology_class": ModelSelectionObservation,
        "ontology_class_name": "ModelSelectionObservation",
        "relationship": "has_model_selection_observations",
        "type_property": "model_selection_observation_type",
        "default_intent": IntentType.MODEL_SELECTION.value,
    },
    "experimental": {
        "ontology_class": ExperimentalObservation,
        "ontology_class_name": "ExperimentalObservation",
        "relationship": "has_experimental_observations",
        "type_property": "experimental_observation_type",
        "default_intent": IntentType.DATA_UNDERSTANDING.value,
    },
}

SUBTYPE_RULES: tuple[dict[str, Any], ...] = (
    {
        "family": "exploratory",
        "observation_type": ExploratoryTags.DATA_QUALITY_OBSERVATION.value,
        "keywords": {
            "missing",
            "null",
            "na",
            "noise",
            "outlier",
            "duplicate",
            "inconsistent",
            "quality",
            "error",
            "drift",
            "invalid",
            "imbalance",
        },
        "phrases": ("data quality", "missing value", "null value"),
    },
    {
        "family": "exploratory",
        "observation_type": ExploratoryTags.RELEVANCE_OBSERVATION.value,
        "keywords": {
            "relevant",
            "selected",
            "scope",
            "subset",
            "baseline",
            "needed",
            "focus",
            "coverage",
        },
        "phrases": ("in scope", "out of scope", "selected field"),
    },
    {
        "family": "data_representation",
        "observation_type": DataRepresentationTags.FEATURE_ENGG_OBSERVATION.value,
        "keywords": {
            "feature",
            "derived",
            "engineered",
            "embedding",
            "aggregated",
            "window",
            "lag",
            "ratio",
            "encoded",
        },
        "phrases": ("feature engineering", "derived feature"),
    },
    {
        "family": "data_representation",
        "observation_type": DataRepresentationTags.DATA_TRANSFORMATION_OBSERVATION.value,
        "keywords": {
            "transform",
            "normalized",
            "scaled",
            "standardized",
            "encoded",
            "tokenized",
            "imputed",
            "bucketed",
            "reshaped",
            "filtered",
        },
        "phrases": ("data transformation", "log transform", "one hot"),
    },
    {
        "family": "modelling_choice",
        "observation_type": ModellingChoiceTags.MODELLING_ASSUMPTION_OBSERVATION.value,
        "keywords": {
            "assume",
            "assumption",
            "assumed",
            "linearity",
            "stationary",
            "iid",
            "independent",
            "normality",
        },
        "phrases": ("we assume", "under the assumption"),
    },
    {
        "family": "modelling_choice",
        "observation_type": ModellingChoiceTags.MODELLING_CHOICE_OBSERVATION.value,
        "keywords": {
            "chose",
            "selected",
            "picked",
            "configured",
            "hyperparameter",
            "pruning",
            "regularization",
            "architecture",
            "xgboost",
            "randomforest",
            "random",
            "forest",
        },
        "phrases": ("we chose", "model choice", "selected model"),
    },
    {
        "family": "model_selection",
        "observation_type": ModelSelectionTags.MODEL_SELECTION_SETUP_DESCRIPTION.value,
        "keywords": {
            "cross",
            "validation",
            "fold",
            "holdout",
            "split",
            "benchmark",
            "evaluation",
            "protocol",
            "setup",
        },
        "phrases": ("cross validation", "train test split", "evaluation setup"),
    },
    {
        "family": "model_selection",
        "observation_type": ModelSelectionTags.MODEL_SELECTION_RESULT_SUMMARY.value,
        "keywords": {
            "outperformed",
            "best",
            "won",
            "higher",
            "lower",
            "improved",
            "decreased",
            "increased",
            "accuracy",
            "precision",
            "recall",
            "auc",
            "f1",
            "rmse",
            "mae",
        },
        "phrases": ("performed better", "result summary", "final model"),
    },
    {
        "family": "model_selection",
        "observation_type": ModelSelectionTags.MODEL_SELECTION_STATEMENT.value,
        "keywords": {
            "recommend",
            "selection",
            "selected",
            "final",
            "candidate",
            "comparison",
            "ranking",
            "metric",
        },
        "phrases": ("model selection", "selected as final"),
    },
    {
        "family": "model_selection",
        "observation_type": ModelSelectionTags.MODEL_SELECTION_OBSERVATION.value,
        "keywords": {
            "accuracy",
            "precision",
            "recall",
            "auc",
            "f1",
            "lift",
            "score",
            "drop",
            "increase",
            "decrease",
            "metric",
        },
        "phrases": ("model accuracy", "performance changed"),
    },
    {
        "family": "experimental",
        "observation_type": ExperimentationTags.HYPOTHESIS_STATEMENT.value,
        "keywords": {
            "hypothesis",
            "hypothesize",
            "expect",
            "should",
            "if",
            "then",
        },
        "phrases": ("our hypothesis", "we expect"),
    },
    {
        "family": "experimental",
        "observation_type": ExperimentationTags.EXPERIMENTAL_CONJECTURE.value,
        "keywords": {
            "conjecture",
            "suspect",
            "believe",
            "might",
            "may",
            "possibly",
        },
        "phrases": ("we conjecture", "we suspect"),
    },
    {
        "family": "experimental",
        "observation_type": ExperimentationTags.RESULT_SUMMARY.value,
        "keywords": {
            "result",
            "conclusion",
            "summary",
            "observed",
            "showed",
            "demonstrated",
        },
        "phrases": ("experiment showed", "result summary"),
    },
    {
        "family": "experimental",
        "observation_type": ExperimentationTags.EXPERIMENTAL_OBSERVATION.value,
        "keywords": {
            "experiment",
            "trial",
            "ablation",
            "run",
            "observed",
            "treatment",
        },
        "phrases": ("during the experiment",),
    },
)

METRIC_PATTERN = re.compile(
    r"\b(accuracy|precision|recall|auc|f1|rmse|mae|mape|lift|loss|latency|throughput)\b",
    re.IGNORECASE,
)
NUMERIC_PATTERN = re.compile(
    r"(?<!\w)\d+(?:\.\d+)?(?:%)?(?!\w)",
    re.IGNORECASE,
)
TIMESTAMP_PATTERN = re.compile(
    r"\b(?:\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|q[1-4]\s*\d{4}|jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b",
    re.IGNORECASE,
)
COMPONENT_PATTERN = re.compile(
    r"\b(?:after|before|for|in|on|of|with)\s+([a-zA-Z][a-zA-Z0-9_\-\s]{2,40})",
    re.IGNORECASE,
)
GENERIC_COMPONENTS = {
    "data",
    "dataset",
    "model",
    "feature",
    "pipeline",
    "workflow",
    "pruning",
    "encoder",
    "classifier",
    "validation",
    "training",
    "holdout",
}


class ExtractedEntities(BaseModel):
    metric: Optional[str] = None
    value: Optional[str] = None
    timestamp: Optional[str] = None
    affected_component: Optional[str] = None


class ObservationMapping(BaseModel):
    input_text: str
    workflow_family: ObservationFamily
    workflow_phase_order: Optional[int]
    observation_type: str
    ontology_class_name: str
    relationship_property: str
    type_property: str
    intent: Optional[str]
    finding: str
    finding_sequence: Optional[int] = None
    extracted_entities: ExtractedEntities = Field(default_factory=ExtractedEntities)
    validation_passed: bool
    validation_errors: list[str] = Field(default_factory=list)
    rationale: str
    confidence: float


class ObservationLogResult(BaseModel):
    mapping: ObservationMapping
    project_file: str
    workflow_name: str
    action: str
    json_ld: dict[str, Any]
    python_code: str


def _safe_identifier(name: str) -> str:
    identifier = re.sub(r"[^a-zA-Z0-9_]+", "_", name.strip()).strip("_")
    return identifier or "workflow"


@lru_cache(maxsize=1)
def _get_tokenizer() -> Any:
    try:
        import spacy

        return spacy.blank("en")
    except Exception:
        return None


def _tokenize(text: str) -> list[str]:
    nlp = _get_tokenizer()
    if nlp is None:
        return re.findall(r"[a-zA-Z0-9_\-]+", text.lower())
    return [token.text.lower() for token in nlp(text) if not token.is_space and not token.is_punct]


def _extract_entities(text: str) -> ExtractedEntities:
    metric_match = METRIC_PATTERN.search(text)
    value_match = NUMERIC_PATTERN.search(text)
    timestamp_match = TIMESTAMP_PATTERN.search(text)
    component = None
    for match in COMPONENT_PATTERN.finditer(text):
        candidate = match.group(1).strip(" .,")
        candidate = re.split(r"\b(?:on|during|at|by)\b", candidate, maxsplit=1)[0].strip(" .,")
        lowered = candidate.lower()
        if lowered and lowered not in {"the model", "the data", "the dataset"}:
            component = candidate
            break
    if component is None:
        lowered_text = text.lower()
        for term in GENERIC_COMPONENTS:
            if term in lowered_text:
                component = term
                break

    return ExtractedEntities(
        metric=metric_match.group(1).lower() if metric_match else None,
        value=value_match.group(0) if value_match else None,
        timestamp=timestamp_match.group(0) if timestamp_match else None,
        affected_component=component,
    )


def _score_rule(text: str, tokens: set[str], rule: dict[str, Any]) -> int:
    score = 0
    for keyword in rule["keywords"]:
        normalized = keyword.lower()
        if " " in normalized:
            if normalized in text:
                score += 2
        elif normalized in tokens:
            score += 1
    for phrase in rule.get("phrases", ()):
        if phrase.lower() in text:
            score += 2
    return score


def _classify(text: str) -> tuple[dict[str, Any], float]:
    normalized = text.lower()
    tokens = set(_tokenize(text))
    entities = _extract_entities(text)
    scores: list[tuple[int, dict[str, Any]]] = []
    for rule in SUBTYPE_RULES:
        score = _score_rule(normalized, tokens, rule)
        if rule["family"] == "model_selection" and (entities.metric or entities.value):
            score += 1
        scores.append((score, rule))
    best_score, best_rule = max(scores, key=lambda item: item[0])
    confidence = 0.0 if best_score <= 0 else min(0.99, 0.35 + (best_score * 0.12))
    return best_rule, round(confidence, 2)


def _validate_text(text: str, rule: dict[str, Any], entities: ExtractedEntities, confidence: float) -> list[str]:
    errors: list[str] = []
    stripped = text.strip()
    if len(stripped) < 12:
        errors.append("Input is too short to form a meaningful KMDS observation.")
    if len(_tokenize(stripped)) < 4:
        errors.append("Input needs more context before it can be mapped to the ontology.")
    if confidence < 0.45:
        errors.append("Could not classify the text confidently into an existing KMDS observation type.")
    if not (entities.metric or entities.value or entities.timestamp or entities.affected_component):
        errors.append(
            "Input does not expose a metric, value, timestamp, or affected component clearly enough for structured extraction."
        )
    if rule["family"] == "model_selection" and not (entities.metric or entities.value):
        errors.append("Model-selection observations should include a metric or measurable outcome.")
    return errors


def map_text_to_observation(
    text: str,
    *,
    finding_sequence: Optional[int] = None,
    intent: Optional[str] = None,
) -> ObservationMapping:
    stripped = text.strip()
    rule, confidence = _classify(stripped)
    family = rule["family"]
    entities = _extract_entities(stripped)
    errors = _validate_text(stripped, rule, entities, confidence)
    metadata = FAMILY_METADATA[family]
    resolved_intent = intent or metadata["default_intent"]
    rationale_bits = [
        f"classified as {rule['observation_type']}",
        f"family={family}",
    ]
    if entities.metric:
        rationale_bits.append(f"metric={entities.metric}")
    if entities.value:
        rationale_bits.append(f"value={entities.value}")
    if entities.affected_component:
        rationale_bits.append(f"component={entities.affected_component}")

    return ObservationMapping(
        input_text=stripped,
        workflow_family=family,
        workflow_phase_order=FAMILY_PHASE_ORDER[family],
        observation_type=rule["observation_type"],
        ontology_class_name=metadata["ontology_class_name"],
        relationship_property=metadata["relationship"],
        type_property=metadata["type_property"],
        intent=resolved_intent,
        finding=stripped,
        finding_sequence=finding_sequence,
        extracted_entities=entities,
        validation_passed=not errors,
        validation_errors=errors,
        rationale="; ".join(rationale_bits),
        confidence=confidence,
    )


def summarize_observation_text(text: str) -> str:
    mapping = map_text_to_observation(text)
    status = "valid" if mapping.validation_passed else "needs more detail"
    phase = (
        f"phase {mapping.workflow_phase_order}"
        if mapping.workflow_phase_order is not None
        else "experimentation track"
    )
    return (
        f"{mapping.observation_type} in the {mapping.workflow_family} family "
        f"({phase}); validation {status}; confidence={mapping.confidence:.2f}."
    )


def build_observation_jsonld(mapping: ObservationMapping, base_iri: Optional[str] = None) -> dict[str, Any]:
    namespace = base_iri or ontology_model.onto.base_iri
    payload: dict[str, Any] = {
        "@context": {
            "kmds": namespace,
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@type": f"kmds:{mapping.ontology_class_name}",
        "kmds:finding": {
            "@value": mapping.finding,
            "@type": "xsd:string",
        },
        f"kmds:{mapping.type_property}": {
            "@value": mapping.observation_type,
            "@type": "xsd:string",
        },
    }
    if mapping.finding_sequence is not None:
        payload["kmds:finding_sequence"] = {
            "@value": mapping.finding_sequence,
            "@type": "xsd:integer",
        }
    if mapping.intent:
        payload["kmds:intent"] = {
            "@value": mapping.intent,
            "@type": "xsd:string",
        }
    return payload


def build_observation_python_code(
    mapping: ObservationMapping,
    *,
    workflow_variable: str = "workflow",
    ontology_variable: str = "onto",
) -> str:
    sequence_literal = mapping.finding_sequence if mapping.finding_sequence is not None else "<sequence>"
    intent_block = ""
    if mapping.intent:
        intent_block = f"observation.intent = {mapping.intent!r}\n"
    return (
        "from kmds.ontology.kmds_ontology import *\n\n"
        f"observation = {mapping.ontology_class_name}(namespace={ontology_variable})\n"
        f"observation.finding = {mapping.finding!r}\n"
        f"observation.finding_sequence = {sequence_literal}\n"
        f"observation.{mapping.type_property} = {mapping.observation_type!r}\n"
        f"{intent_block}"
        f"{workflow_variable}.{mapping.relationship_property} = list({workflow_variable}.{mapping.relationship_property}) + [observation]\n"
    )


def _create_workflow(workflow_name: str, workflow_type: str) -> Workflow:
    normalized = workflow_type.strip().lower()
    identifier = _safe_identifier(workflow_name)
    if normalized == "experimental":
        return KnowledgeExtractionExperimentationWorkflow(identifier)
    return KnowledgeApplicationWorkflow(identifier)


def _next_sequence(workflow: Workflow, relationship_property: str) -> int:
    current = list(getattr(workflow, relationship_property, []))
    return len(current) + 1


def _find_workflow_by_name(onto: Any, workflow_name: str) -> Optional[Workflow]:
    target_name = _safe_identifier(workflow_name)
    with onto:
        for workflow in Workflow.instances():
            candidate_name = getattr(workflow, "name", None) or getattr(workflow, "_name", None)
            if candidate_name == target_name:
                return workflow
    return None


def _append_observation(workflow: Workflow, mapping: ObservationMapping) -> None:
    metadata = FAMILY_METADATA[mapping.workflow_family]
    observation_class = metadata["ontology_class"]
    observation = observation_class(namespace=ontology_model.onto)
    observation.finding = mapping.finding
    observation.finding_sequence = mapping.finding_sequence
    setattr(observation, mapping.type_property, mapping.observation_type)
    if mapping.intent:
        observation.intent = mapping.intent
    collection = list(getattr(workflow, mapping.relationship_property, []))
    collection.append(observation)
    setattr(workflow, mapping.relationship_property, collection)


def log_text_as_observation(
    *,
    text: str,
    workflow_name: str,
    project_file_path: str,
    project_mode: str,
    workflow_type: Optional[str] = None,
    finding_sequence: Optional[int] = None,
    intent: Optional[str] = None,
) -> ObservationLogResult:
    mapping = map_text_to_observation(text, finding_sequence=finding_sequence, intent=intent)
    if not mapping.validation_passed:
        raise ValueError(" ".join(mapping.validation_errors))

    project_path = Path(project_file_path)
    if project_mode not in {"create", "update"}:
        raise ValueError("project_mode must be either 'create' or 'update'")

    if project_mode == "update":
        if not project_path.exists():
            raise ValueError(f"Project file does not exist for update: {project_file_path}")
        onto = load_kb(str(project_path))
        if onto is None:
            raise ValueError(f"Could not load project knowledge base: {project_file_path}")
        workflow = _find_workflow_by_name(onto, workflow_name) or get_workflow(onto)
        if workflow is None:
            workflow = _create_workflow(workflow_name, workflow_type or "application")
        action = "Updated"
    else:
        if project_path.exists():
            raise ValueError(
                f"Project file already exists: {project_file_path}. Use update mode to modify it."
            )
        action = "Created"
        default_workflow_type = workflow_type
        if default_workflow_type is None:
            default_workflow_type = "experimental" if mapping.workflow_family == "experimental" else "application"
        workflow = _create_workflow(
            workflow_name,
            default_workflow_type,
        )

    if mapping.finding_sequence is None:
        mapping = mapping.model_copy(
            update={"finding_sequence": _next_sequence(workflow, mapping.relationship_property)}
        )

    if not getattr(workflow, "description", None):
        workflow.description = "Workflow updated from natural-language observation ingestion."

    _append_observation(workflow, mapping)

    project_path.parent.mkdir(parents=True, exist_ok=True)
    ontology_model.onto.save(file=str(project_path), format="rdfxml")

    return ObservationLogResult(
        mapping=mapping,
        project_file=str(project_path),
        workflow_name=workflow_name,
        action=action,
        json_ld=build_observation_jsonld(mapping),
        python_code=build_observation_python_code(mapping),
    )


def mapping_to_json(mapping: ObservationMapping) -> str:
    return json.dumps(mapping.model_dump(), indent=2)