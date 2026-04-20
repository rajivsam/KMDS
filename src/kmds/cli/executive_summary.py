import argparse
from typing import Optional

from kmds.utils.executive_summary import export_executive_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export a non-technical executive summary from a KMDS knowledge graph."
    )
    parser.add_argument(
        "--project-file",
        type=str,
        required=True,
        help="Project knowledge graph file path (.xml recommended)",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        required=True,
        help="Destination file for executive summary text",
    )
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Try LLM-based summary generation and fallback to local summary if unavailable",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-1.5-flash",
        help="LLM model identifier when --use-llm is set",
    )
    parser.add_argument(
        "--max-findings-per-section",
        type=int,
        default=3,
        help="Maximum findings to include from each workflow stage",
    )
    parser.add_argument(
        "--format",
        choices=["text", "markdown"],
        default="text",
        help="Output format for executive summary",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    output_path = export_executive_summary(
        kb_path=args.project_file,
        output_file=args.output_file,
        use_llm=args.use_llm,
        model=args.model,
        max_findings_per_section=args.max_findings_per_section,
        summary_format=args.format,
    )
    print(f"Executive summary exported to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
