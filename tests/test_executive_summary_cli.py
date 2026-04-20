from pathlib import Path

from kmds.cli.executive_summary import main as exec_summary_main
from kmds.cli.summary_ingest import run_summary_ingest


def test_exec_summary_cli_exports_text_file(tmp_path: Path):
    project_fp = tmp_path / "exec_cli_project.xml"
    output_fp = tmp_path / "exec_cli_summary.txt"

    run_summary_ingest(
        summary="Experimental evaluation showed missing values and quality checks.",
        workflow_name="exec_cli_workflow",
        project_file_path=str(project_fp),
        project_mode="create",
        workflow_type="experimental",
        no_prompt=True,
    )

    rc = exec_summary_main(
        [
            "--project-file",
            str(project_fp),
            "--output-file",
            str(output_fp),
        ]
    )

    assert rc == 0
    assert output_fp.exists()
    assert "Executive Summary" in output_fp.read_text(encoding="utf-8")


def test_exec_summary_cli_exports_markdown_file(tmp_path: Path):
    project_fp = tmp_path / "exec_cli_project_md.xml"
    output_fp = tmp_path / "exec_cli_summary.md"

    run_summary_ingest(
        summary="Application workflow with data quality and relevance observations.",
        workflow_name="exec_cli_workflow_md",
        project_file_path=str(project_fp),
        project_mode="create",
        workflow_type="application",
        no_prompt=True,
    )

    rc = exec_summary_main(
        [
            "--project-file",
            str(project_fp),
            "--output-file",
            str(output_fp),
            "--format",
            "markdown",
        ]
    )

    assert rc == 0
    assert output_fp.exists()
    assert output_fp.read_text(encoding="utf-8").startswith("# Executive Summary")
