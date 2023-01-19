from collections import Counter
from pathlib import Path

import spacy
import srsly
import typer
from prodigy.components.db import connect
from rich.console import Console
from rich.table import Table


def main(
    dataset: str = typer.Argument(..., help="Name of the Prodigy dataset"),
    patterns: Path = typer.Argument(..., help="Path to patterns file"),
    model: Path = typer.Argument(..., help="Path to spaCy model"),
):
    """Evaluate matcher and spaCy model."""

    nlp = spacy.load("en_core_web_sm")
    db = connect()

    dataset = db.get_dataset_examples(dataset)

    label = dataset[0]["label"]
    results = {}

    patterns = srsly.read_jsonl(patterns)
    ruler = nlp.add_pipe("span_ruler")
    ruler.add_patterns(patterns)

    def matcher_evaluate(text):
        doc = nlp(text)
        matches = doc.spans["ruler"]
        if len(matches) > 0:
            return True
        return False

    matcher_results = Counter(
        [(matcher_evaluate(d["text"]), d["answer"]) for d in dataset]
    ).items()
    results["matcher"] = matcher_results

    model_path = Path(model) / "model-best"
    textcat_model = spacy.load(model_path)

    def model_evaluate(text):
        doc = textcat_model(nlp(text))
        prediction = doc.cats
        if prediction[label] > 0.5:
            return True
        return False

    model_results = Counter(
        [(model_evaluate(d["text"]), d["answer"]) for d in dataset]
    ).items()
    results["model"] = model_results

    table = Table(
        "Name",
        "False, negative",
        "True, positive",
        "False, positive",
        "True, negative",
        "Accuracy (%)",
        title="Values",
    )

    def get_values(counter):
        columns = [
            (False, "reject"),
            (True, "accept"),
            (False, "accept"),
            (True, "reject"),
        ]

        rows = [value for key, value in sorted(counter) if key in columns]

        acc = round(((rows[1] + rows[2]) / sum(rows)) * 100, 2)
        return rows, acc

    for key in results:
        rows, acc = get_values(results[key])
        table.add_row(
            key, str(rows[1]), str(rows[2]), str(rows[0]), str(rows[3]), str(acc)
        )

    console = Console()
    console.print(table)


if __name__ == "__main__":
    typer.run(main)
