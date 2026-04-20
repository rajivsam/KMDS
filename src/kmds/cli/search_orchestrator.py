"""CLI entry point for the LLM-driven search orchestrator.

Usage examples::

    # Ask a question (uses Google GenAI – requires GOOGLE_API_KEY)
    kmds-ask --project-file kb.xml --query "What data quality issues were found?"

    # Persist the vector index so repeated queries skip embedding rebuild
    kmds-ask --project-file kb.xml --query "Which model was selected?" \\
              --persist-dir ./my_idx

    # Use a specific LLM model
    kmds-ask --project-file kb.xml --query "Feature engineering steps?" \\
              --model gemini-2.0-flash

    # Show the route chosen and raw records alongside the answer
    kmds-ask --project-file kb.xml --query "transformation decisions" --verbose
"""

import argparse
import json
import os
import sys
from typing import Optional

from kmds.search.search_orchestrator import SearchOrchestrator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kmds-ask",
        description=(
            "Natural language search orchestrator for a KMDS knowledge base.\n"
            "An LLM routes the query to the best observation template, "
            "executes it, and synthesises a plain-English answer."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--project-file",
        type=str,
        required=True,
        help="Path to the KMDS knowledge-base file (.xml).",
    )
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Natural language question to ask about the knowledge base.",
    )
    parser.add_argument(
        "--persist-dir",
        type=str,
        default=None,
        help=(
            "Directory to persist / reload the semantic vector index. "
            "Omit to use an in-memory index (rebuilt each run)."
        ),
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-1.5-flash",
        help="Google GenAI model name (default: gemini-1.5-flash).",
    )
    parser.add_argument(
        "--n-results",
        type=int,
        default=5,
        help="Maximum number of raw observations to retrieve (default: 5).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help=(
            "Print the routing decision and raw result records in addition "
            "to the synthesised answer."
        ),
    )
    parser.add_argument(
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format: 'text' (default) or 'json'.",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not os.path.isfile(args.project_file):
        print(
            f"Error: project file not found: {args.project_file}",
            file=sys.stderr,
        )
        return 1

    try:
        orchestrator = SearchOrchestrator(
            kb_path=args.project_file,
            persist_dir=args.persist_dir,
            model=args.model,
            n_results=args.n_results,
        )
    except ValueError as exc:
        print(f"Error initialising orchestrator: {exc}", file=sys.stderr)
        return 1

    result = orchestrator.ask(args.query)

    if args.output_format == "json":
        payload = {
            "answer": result.answer,
            "intent_class": result.intent_class,
            "route_explanation": result.route_explanation,
            "results": result.results,
        }
        print(json.dumps(payload, indent=2))
        return 0

    # ── Human-readable output ──────────────────────────────────────────
    print(f"\nQuery: {args.query}\n")

    if args.verbose:
        print(f"Route      : {result.intent_class}")
        print(f"Explanation: {result.route_explanation}\n")

    print("Answer")
    print("======")
    print(result.answer)

    if args.verbose and result.results:
        print(f"\nRaw observations ({len(result.results)}):")
        print("-" * 60)
        for i, r in enumerate(result.results, 1):
            obs_type = r.get("obs_type", "")
            seq = r.get("finding_seq", "")
            finding = r.get("finding", "")
            intent_tag = f"  intent: {r['intent']}" if "intent" in r else ""
            dist_tag = (
                f"  distance: {r['distance']:.4f}" if "distance" in r else ""
            )
            print(f"[{i}] {obs_type} | seq={seq}{dist_tag}{intent_tag}")
            print(f"     {finding}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
