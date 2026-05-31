"""Command-line evaluator for CultureTrust AI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from .report import render_markdown_report
    from .scoring import score_dataset
except ImportError:  # Allows `python src/evaluator.py` during local experiments.
    from report import render_markdown_report
    from scoring import score_dataset


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, content: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content, indent=2, ensure_ascii=False), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate AI responses for cultural awareness, social usefulness, safety, and transparency.",
    )
    parser.add_argument(
        "--cases",
        default="data/evaluation_cases.json",
        help="Path to the evaluation cases JSON file.",
    )
    parser.add_argument(
        "--responses",
        default="examples/sample_response.json",
        help="Path to the AI responses JSON file.",
    )
    parser.add_argument(
        "--output",
        default="reports/sample_report.md",
        help="Path for the generated Markdown report.",
    )
    parser.add_argument(
        "--json-output",
        default=None,
        help="Optional path for the generated JSON score report.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cases_path = Path(args.cases)
    responses_path = Path(args.responses)

    cases = load_json(cases_path)
    response_payload = load_json(responses_path)
    responses = response_payload.get("responses", [])

    evaluation = score_dataset(cases, responses)
    markdown = render_markdown_report(
        evaluation,
        model_name=response_payload.get("model_name", "Unknown model"),
        model_version=response_payload.get("model_version"),
    )

    write_text(Path(args.output), markdown)

    if args.json_output:
        write_json(Path(args.json_output), evaluation)

    print(f"CultureTrust AI score: {evaluation['overall_score']} / 100")
    print(f"Risk level: {evaluation['risk_level']}")
    print(f"Report written to: {args.output}")


if __name__ == "__main__":
    main()
