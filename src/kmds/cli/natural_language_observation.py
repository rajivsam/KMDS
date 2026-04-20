import argparse
import json
from pathlib import Path
from typing import Optional

from kmds.utils.natural_language_observation import (
    log_text_as_observation,
    map_text_to_observation,
    summarize_observation_text,
)


def _read_text(text: Optional[str], text_file: Optional[str]) -> str:
    if text and text.strip():
        return text.strip()
    if text_file:
        content = Path(text_file).read_text(encoding="utf-8").strip()
        if content:
            return content
    raise ValueError("Provide non-empty text using --text or --text-file")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Map natural-language text into KMDS observation objects or log it to a KMDS knowledge base."
    )
    parser.add_argument("--text", type=str, default=None, help="Natural-language observation text")
    parser.add_argument(
        "--text-file",
        type=str,
        default=None,
        help="Path to a text file containing the natural-language observation",
    )
    parser.add_argument(
        "--mode",
        choices=["summary", "log"],
        default="summary",
        help="summary returns a classified summary; log validates and writes to a KMDS KB",
    )
    parser.add_argument(
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )
    parser.add_argument("--workflow-name", type=str, default=None, help="Workflow name for log mode")
    parser.add_argument("--project-file", type=str, default=None, help="Knowledge base file for log mode")
    parser.add_argument(
        "--workflow-type",
        choices=["application", "experimental"],
        default=None,
        help="Workflow type when creating a KB in log mode",
    )
    parser.add_argument(
        "--finding-sequence",
        type=int,
        default=None,
        help="Optional explicit finding sequence; otherwise the next sequence is assigned",
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--create-project", action="store_true")
    mode_group.add_argument("--update-project", action="store_true")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    text = _read_text(args.text, args.text_file)
    if args.mode == "summary":
        mapping = map_text_to_observation(text, finding_sequence=args.finding_sequence)
        if args.output_format == "json":
            print(json.dumps(mapping.model_dump(), indent=2))
        else:
            print(summarize_observation_text(text))
        return 0

    if not args.workflow_name or not args.project_file:
        raise ValueError("--workflow-name and --project-file are required in log mode")

    project_mode = "update" if args.update_project else "create"
    result = log_text_as_observation(
        text=text,
        workflow_name=args.workflow_name,
        project_file_path=args.project_file,
        project_mode=project_mode,
        workflow_type=args.workflow_type,
        finding_sequence=args.finding_sequence,
    )

    if args.output_format == "json":
        print(json.dumps(result.model_dump(), indent=2))
    else:
        print(
            f"{result.action} KMDS project '{Path(result.project_file).name}' with "
            f"{result.mapping.observation_type} in workflow '{result.workflow_name}'."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())