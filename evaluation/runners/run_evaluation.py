import json
from pathlib import Path

from evaluation.metrics.page_accuracy import page_accuracy

ROOT = Path(__file__).parents[1]


def load_jsonl(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main() -> None:
    cases = load_jsonl(ROOT / "datasets" / "page_location.jsonl")
    report = {
        "cases": len(cases),
        "note": "Dataset fixtures are examples; connect this runner to a seeded test workspace before claiming model quality.",
        "baseline_page_accuracy": sum(
            page_accuracy([], set(case["expected_pages"])) for case in cases
        )
        / len(cases)
        if cases
        else None,
    }
    output = ROOT / "reports" / "latest.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
