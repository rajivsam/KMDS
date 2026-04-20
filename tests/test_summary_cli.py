from pathlib import Path

import pytest

from kmds.cli.summary_ingest import run_summary_ingest
from kmds.utils.load_utils import load_exp_observations, load_kb


def test_run_summary_ingest_writes_output_kb(tmp_path: Path):
    output_fp = tmp_path / "summary_output.owl"
    summary = (
        "We are running experiments to compare feature choices. "
        "Missing values were observed in the account age field."
    )

    run_summary_ingest(
        summary=summary,
        workflow_name="ba_intake_cli",
        project_file_path=str(output_fp),
        project_mode="create",
        no_prompt=True,
    )

    assert output_fp.exists()
    onto = load_kb(str(output_fp))
    df_exp = load_exp_observations(onto)
    assert df_exp.shape[0] >= 1


def test_run_summary_ingest_ambiguous_raises_when_no_prompt(tmp_path: Path):
    output_fp = tmp_path / "ambiguous.owl"
    summary = "New project kickoff notes from business team."

    with pytest.raises(ValueError):
        run_summary_ingest(
            summary=summary,
            workflow_name="ambiguous_case",
            project_file_path=str(output_fp),
            project_mode="create",
            no_prompt=True,
        )


def test_run_summary_ingest_ambiguous_prompt_resolves(tmp_path: Path):
    output_fp = tmp_path / "prompt_resolved.owl"
    summary = "Project intake notes for upcoming quarter."

    run_summary_ingest(
        summary=summary,
        workflow_name="prompt_case",
        project_file_path=str(output_fp),
        project_mode="create",
        no_prompt=False,
        prompt_fn=lambda _: "application",
    )

    assert output_fp.exists()


def test_run_summary_ingest_update_requires_existing_project(tmp_path: Path):
    missing_fp = tmp_path / "missing_project.owl"
    with pytest.raises(ValueError):
        run_summary_ingest(
            summary="Daily reporting notes.",
            workflow_name="missing_update",
            project_file_path=str(missing_fp),
            project_mode="update",
            no_prompt=True,
            workflow_type="application",
        )


def test_run_summary_ingest_create_rejects_existing_project(tmp_path: Path):
    project_fp = tmp_path / "existing_project.owl"

    run_summary_ingest(
        summary="Initial project summary for daily reporting.",
        workflow_name="existing_project",
        project_file_path=str(project_fp),
        project_mode="create",
        no_prompt=True,
        workflow_type="application",
    )

    with pytest.raises(ValueError):
        run_summary_ingest(
            summary="Second summary should require update mode.",
            workflow_name="existing_project",
            project_file_path=str(project_fp),
            project_mode="create",
            no_prompt=True,
            workflow_type="application",
        )


def test_run_summary_ingest_update_existing_project(tmp_path: Path):
    project_fp = tmp_path / "update_project.owl"

    run_summary_ingest(
        summary="Initial summary with relevance checks.",
        workflow_name="update_target",
        project_file_path=str(project_fp),
        project_mode="create",
        no_prompt=True,
        workflow_type="application",
    )

    run_summary_ingest(
        summary="Follow-up summary with missing values in customer id.",
        workflow_name="update_target",
        project_file_path=str(project_fp),
        project_mode="update",
        no_prompt=True,
        workflow_type="application",
    )

    assert project_fp.exists()
