import argparse
from pathlib import Path
from typing import Callable, Optional

from kmds.ontology import kmds_ontology as ontology_model
from kmds.utils.load_utils import load_kb
from kmds.utils.summary_logger import log_exploratory_summary


def _read_summary(summary: Optional[str], summary_file: Optional[str]) -> str:
    if summary and summary.strip():
        return summary.strip()
    if summary_file:
        content = Path(summary_file).read_text(encoding="utf-8").strip()
        if content:
            return content
    raise ValueError("Provide a non-empty summary using --summary or --summary-file")


def run_summary_ingest(
    *,
    summary: str,
    workflow_name: str,
    project_file_path: str,
    project_mode: str,
    workflow_type: Optional[str] = None,
    no_prompt: bool = False,
    intent: Optional[str] = None,
    prompt_fn: Callable[[str], str] = input,
) -> str:
    project_path = Path(project_file_path)

    if project_mode == "update":
        if not project_path.exists():
            raise ValueError(
                f"Project file does not exist for update: {project_file_path}"
            )
        onto = load_kb(str(project_path))
        if onto is None:
            raise ValueError(
                f"Could not load project knowledge base: {project_file_path}"
            )
    elif project_mode == "create":
        if project_path.exists():
            raise ValueError(
                f"Project file already exists: {project_file_path}. Use update mode to modify it."
            )
    else:
        raise ValueError("project_mode must be either 'create' or 'update'")

    workflow = log_exploratory_summary(
        project_summary=summary,
        workflow_name=workflow_name,
        workflow_type=workflow_type,
        prompt_on_ambiguity=not no_prompt,
        input_fn=prompt_fn,
        intent=intent,
    )

    output_path = project_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ontology_model.onto.save(file=str(output_path), format="rdfxml")

    action = "Created" if project_mode == "create" else "Updated"
    print(
        "{} project '{}' with workflow '{}' and {} exploratory observations at {}".format(
            action,
            project_path.name,
            workflow_name,
            len(workflow.has_exploratory_observations),
            output_path,
        )
    )
    return str(output_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create/update exploratory observations from a project summary block."
    )
    parser.add_argument("--summary", type=str, default=None, help="Project summary text")
    parser.add_argument(
        "--summary-file",
        type=str,
        default=None,
        help="Path to a text file containing the project summary",
    )
    parser.add_argument(
        "--workflow-name",
        type=str,
        required=True,
        help="Workflow name for the created/updated workflow",
    )
    parser.add_argument(
        "--project-file",
        type=str,
        required=True,
        help="Project knowledge base file path (.xml recommended; RDF/XML format)",
    )
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--create-project",
        action="store_true",
        help="Create a new project knowledge base at --project-file",
    )
    mode_group.add_argument(
        "--update-project",
        action="store_true",
        help="Update an existing project knowledge base at --project-file",
    )
    parser.add_argument(
        "--workflow-type",
        type=str,
        choices=["application", "experimental"],
        default=None,
        help="Optional explicit workflow type to skip inference",
    )
    parser.add_argument(
        "--intent",
        type=str,
        default=None,
        help="Optional intent tag applied to each generated exploratory observation",
    )
    parser.add_argument(
        "--no-prompt",
        action="store_true",
        help="Do not prompt on ambiguity; fail instead",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    summary = _read_summary(args.summary, args.summary_file)
    project_mode = "create" if args.create_project else "update"
    run_summary_ingest(
        summary=summary,
        workflow_name=args.workflow_name,
        project_file_path=args.project_file,
        project_mode=project_mode,
        workflow_type=args.workflow_type,
        no_prompt=args.no_prompt,
        intent=args.intent,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
