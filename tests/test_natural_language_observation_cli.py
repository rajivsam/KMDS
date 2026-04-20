from pathlib import Path

from kmds.cli.natural_language_observation import main as observe_main


def test_observe_cli_summary_mode_json():
    rc = observe_main(
        [
            "--text",
            "Missing values were observed in the customer_age field during intake validation.",
            "--mode",
            "summary",
            "--output-format",
            "json",
        ]
    )
    assert rc == 0


def test_observe_cli_log_mode_creates_project(tmp_path: Path):
    project_fp = tmp_path / "cli_nl_observation.xml"
    rc = observe_main(
        [
            "--text",
            "Missing values were observed in the customer_age field during intake validation.",
            "--mode",
            "log",
            "--workflow-name",
            "cli_workflow",
            "--project-file",
            str(project_fp),
            "--workflow-type",
            "application",
            "--create-project",
        ]
    )
    assert rc == 0
    assert project_fp.exists()