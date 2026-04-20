from pathlib import Path

import pytest

from kmds.utils.load_utils import load_kb
from kmds.utils.natural_language_observation import (
    build_observation_jsonld,
    build_observation_python_code,
    log_text_as_observation,
    map_text_to_observation,
    summarize_observation_text,
)


def test_map_text_to_model_selection_observation_extracts_entities():
    mapping = map_text_to_observation(
        "The model accuracy dropped by 5% after pruning on 2026-04-20."
    )
    assert mapping.workflow_family == "model_selection"
    assert mapping.observation_type == "Model Selection Observation"
    assert mapping.extracted_entities.metric == "accuracy"
    assert mapping.extracted_entities.value == "5%"
    assert mapping.extracted_entities.timestamp == "2026-04-20"
    assert mapping.extracted_entities.affected_component == "pruning"


def test_map_text_to_data_quality_observation():
    mapping = map_text_to_observation(
        "Missing values were observed in the customer_age field during intake validation."
    )
    assert mapping.workflow_family == "exploratory"
    assert mapping.observation_type == "Data Quality Observation"
    assert mapping.validation_passed is True


def test_map_text_to_feature_engineering_observation():
    mapping = map_text_to_observation(
        "We engineered a rolling 7 day demand feature from timestamped order counts."
    )
    assert mapping.workflow_family == "data_representation"
    assert mapping.observation_type == "Feature Engineering Observation"


def test_map_text_to_modelling_assumption_observation():
    mapping = map_text_to_observation(
        "We assume the residuals are independent and approximately normal for the classifier diagnostics."
    )
    assert mapping.workflow_family == "modelling_choice"
    assert mapping.observation_type == "Modelling Assumption Observation"


def test_vague_text_fails_validation():
    mapping = map_text_to_observation("Looks better now")
    assert mapping.validation_passed is False
    assert mapping.validation_errors


def test_summary_includes_type_and_phase():
    summary = summarize_observation_text(
        "Missing values were observed in the customer_age field during intake validation."
    )
    assert "Data Quality Observation" in summary
    assert "phase 1" in summary


def test_jsonld_uses_existing_kmds_properties_only():
    mapping = map_text_to_observation(
        "We chose XGBoost after comparing several tree ensembles on validation AUC 0.91."
    )
    json_ld = build_observation_jsonld(mapping)
    assert "@type" in json_ld
    assert "kmds:finding" in json_ld
    assert f"kmds:{mapping.type_property}" in json_ld
    unexpected = set(json_ld.keys()) - {
        "@context",
        "@type",
        "kmds:finding",
        "kmds:finding_sequence",
        f"kmds:{mapping.type_property}",
        "kmds:intent",
    }
    assert not unexpected


def test_python_code_uses_exact_schema_property_names():
    mapping = map_text_to_observation(
        "We chose XGBoost after comparing several tree ensembles on validation AUC 0.91."
    )
    code = build_observation_python_code(mapping)
    assert mapping.ontology_class_name in code
    assert mapping.type_property in code
    assert mapping.relationship_property in code


def test_log_text_as_observation_creates_project_file(tmp_path: Path):
    project_fp = tmp_path / "nl_observation_project.xml"
    result = log_text_as_observation(
        text="Missing values were observed in the customer_age field during intake validation.",
        workflow_name="nl_ingest_workflow",
        project_file_path=str(project_fp),
        project_mode="create",
        workflow_type="application",
    )

    assert project_fp.exists()
    assert result.mapping.observation_type == "Data Quality Observation"
    kb_text = project_fp.read_text(encoding="utf-8")
    assert "Missing values were observed in the customer_age field during intake validation." in kb_text
    assert "Data Quality Observation" in kb_text
    assert "has_exploratory_observations" in kb_text


def test_log_text_as_observation_updates_existing_project(tmp_path: Path):
    project_fp = tmp_path / "nl_observation_update.xml"
    log_text_as_observation(
        text="Missing values were observed in the customer_age field during intake validation.",
        workflow_name="nl_ingest_workflow",
        project_file_path=str(project_fp),
        project_mode="create",
        workflow_type="application",
    )
    result = log_text_as_observation(
        text="We engineered a rolling 7 day demand feature from timestamped order counts.",
        workflow_name="nl_ingest_workflow",
        project_file_path=str(project_fp),
        project_mode="update",
    )

    assert result.mapping.finding_sequence == 1
    kb_text = project_fp.read_text(encoding="utf-8")
    assert "Feature Engineering Observation" in kb_text
    assert "Missing values were observed in the customer_age field during intake validation." in kb_text
    assert "We engineered a rolling 7 day demand feature from timestamped order counts." in kb_text
    assert "has_data_representation_observations" in kb_text


def test_log_text_as_observation_rejects_invalid_text(tmp_path: Path):
    project_fp = tmp_path / "invalid_nl_observation.xml"
    with pytest.raises(ValueError):
        log_text_as_observation(
            text="Looks better now",
            workflow_name="nl_ingest_workflow",
            project_file_path=str(project_fp),
            project_mode="create",
            workflow_type="application",
        )