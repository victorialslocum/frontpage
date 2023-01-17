from collections import Counter
import typer
import spacy
import srsly
from prodigy.components.db import connect
from spacy.matcher import Matcher
from pathlib import Path
from rich.console import Console
from rich.table import Table

def main(
    database: str = typer.Argument(..., help="Name of the Prodigy database"),
    patterns: Path = typer.Argument(..., help="Path to patterns file"),
    model: Path = typer.Argument(..., help="Path to spaCy model")
):
    """Evaluate matcher and spaCy model."""
    
    nlp = spacy.load("en_core_web_sm")
    db = connect()

    dataset = db.get_dataset_examples(database)

    name = str(database)

    matcher = Matcher(nlp.vocab)
    patterns = srsly.read_json(patterns)
    matcher.add(name, patterns)

    def matcher_evaluate(text):
        doc = nlp(text)
        matches = matcher(doc)
        if len(matches) > 0:
            return True
        return False

    matcher_eval = Counter([(matcher_evaluate(d["text"]), d["answer"]) for d in dataset]).items()

    model_path = Path(model) / "model-best"
    textcat_model = spacy.load(model_path)

    def model_evaluate(text):
        doc = textcat_model(nlp(text))
        prediction = doc.cats
        if prediction[name] > 0.5:
            return True
        return False

    model_eval = Counter([(model_evaluate(d["text"]), d["answer"]) for d in dataset]).items()

    table = Table("Type", "False, reject","True, accept", "False, accept", "True, reject", "Accuracy (%)", title="Values")

    def get_values(counter):
        columns = [(False, 'reject'), (True, 'accept'), (False, 'accept'), (True, 'reject')]
        
        rows = [value for key, value in sorted(counter) if key in columns]

        acc = round(((rows[1] + rows[2]) / sum(rows)) * 100, 2)
        return rows, acc

    matcher_rows, matcher_acc = get_values(matcher_eval)
    model_rows, model_acc = get_values(model_eval)


    table.add_row("Matcher", str(matcher_rows[1]),  str(matcher_rows[2]),  str(matcher_rows[0]),  str(matcher_rows[3]), str(matcher_acc))
    table.add_row("Model", str(model_rows[1]),  str(model_rows[2]),  str(model_rows[0]),  str(model_rows[3]), str(model_acc))

    console = Console()
    console.print(table)

if __name__ == "__main__":
    typer.run(main)


