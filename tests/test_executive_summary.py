from pathlib import Path

import pytest

from kmds.cli.summary_ingest import run_summary_ingest
from kmds.utils.executive_summary import (
    export_executive_summary,
    generate_executive_summary,
)


def _build_project(tmp_path: Path) -> Path:
    project_fp = tmp_path / "exec_summary_project.xml"
    run_summary_ingest(
        summary=(
            "This is a production reporting workflow. "
            "Missing values were observed in customer segment fields. "
            "Key attributes were selected for monthly trend reporting."
        ),
        workflow_name="exec_summary_workflow",
        project_file_path=str(project_fp),
        project_mode="create",
        workflow_type="application",
        no_prompt=True,
    )
    return project_fp


def test_generate_executive_summary_local(tmp_path: Path):
    project_fp = _build_project(tmp_path)
    text = generate_executive_summary(str(project_fp), use_llm=False)
    assert "Executive Summary" in text
    assert "Project Type:" in text
    assert "Highlights by stage:" in text


def test_generate_executive_summary_with_llm_callable(tmp_path: Path):
    project_fp = _build_project(tmp_path)
    text = generate_executive_summary(
        str(project_fp),
        use_llm=True,
        llm_fn=lambda prompt: "LLM Executive Summary Output",
    )
    assert text == "LLM Executive Summary Output"


def test_export_executive_summary_writes_file(tmp_path: Path):
    project_fp = _build_project(tmp_path)
    out_fp = tmp_path / "executive_summary.txt"
    result = export_executive_summary(
        kb_path=str(project_fp),
        output_file=str(out_fp),
        use_llm=False,
    )
    assert result == str(out_fp)
    assert out_fp.exists()
    assert "Executive Summary" in out_fp.read_text(encoding="utf-8")


def test_generate_executive_summary_markdown_format(tmp_path: Path):
    project_fp = _build_project(tmp_path)
    text = generate_executive_summary(
        str(project_fp),
        use_llm=False,
        summary_format="markdown",
    )
    assert text.startswith("# Executive Summary")
    assert "## Highlights by stage" in text


def test_generate_executive_summary_invalid_format_raises(tmp_path: Path):
    project_fp = _build_project(tmp_path)
    with pytest.raises(ValueError):
        generate_executive_summary(
            str(project_fp),
            use_llm=False,
            summary_format="markdowntext",
        )
