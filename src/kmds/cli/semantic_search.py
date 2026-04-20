"""CLI entry point for semantic search over a KMDS knowledge base.

Usage example::

    kmds-search --project-file kb.xml --query "missing values in intake data"
    kmds-search --project-file kb.xml --query "imputation" --n-results 3
    kmds-search --project-file kb.xml --query "model accuracy" --persist-dir ./idx
"""

import argparse
import json
from typing import Optional

from kmds.search import SemanticIndex


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Semantic search over a KMDS knowledge graph."
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
        help="Natural language search query.",
    )
    parser.add_argument(
        "--n-results",
        type=int,
        default=5,
        help="Maximum number of results to return (default: 5).",
    )
    parser.add_argument(
        "--persist-dir",
        type=str,
        default=None,
        help=(
            "Directory to persist / load the vector index. "
            "If omitted the index is built in memory for this run only."
        ),
    )
    parser.add_argument(
        "--model",
        type=str,
        default=SemanticIndex.DEFAULT_MODEL,
        help=f"Sentence-transformers model name (default: {SemanticIndex.DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text).",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    idx = SemanticIndex(persist_dir=args.persist_dir, model_name=args.model)

    # Build the index.  If a persist_dir was given and the index already
    # contains documents we skip rebuilding so repeated queries are fast.
    if idx.count() == 0:
        idx.build(args.project_file)

    results = idx.search(args.query, n_results=args.n_results)

    if args.output_format == "json":
        print(json.dumps(results, indent=2))
    else:
        if not results:
            print("No results found.")
            return 0
        print(f"\nSearch results for: '{args.query}'\n")
        for i, r in enumerate(results, start=1):
            obs_type = r.get("obs_type", "")
            workflow = r.get("workflow_name", "")
            seq = r.get("finding_seq", "")
            distance = r.get("distance", 0.0)
            finding = r.get("finding", "")
            intent_part = f"  Intent   : {r['intent']}\n" if "intent" in r else ""
            print(
                f"[{i}] {obs_type}  |  workflow: {workflow}  |  seq: {seq}"
                f"  |  distance: {distance:.4f}\n"
                f"{intent_part}"
                f"  Finding  : {finding}\n"
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
