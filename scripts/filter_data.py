from pathlib import Path

import spacy
import srsly
import typer


def filter_data(
    # fmt: off
    content_in: Path = typer.Argument(..., help="A file with content as jsonl to filter"), 
    spacy_model: str = typer.Argument(..., help="A trained spaCy model"), 
    tag: str = typer.Argument(..., help="A tag to indicate which tag to only consider"), 
    expected_class: str = typer.Argument(..., help="The expected class to come out of the spaCy model"), 
    file_out: Path = typer.Argument(..., help="A file to write the filtered content into"), 
    threshold: float = typer.Option(0.5, help="The classification threshold")
    # fmt: on
):
    nlp = spacy.load(spacy_model)
    stream = srsly.read_jsonl(content_in)
    stream = (ex for ex in stream if tag in ex["tags"])
    stream = ({**d, "text": f"{d['title']} {d['description']}"} for d in stream)
    text_stream = (ex["text"] for ex in stream)
    together = zip(text_stream, stream)
    stream = (
        ex
        for doc, ex in nlp.pipe(together, as_tuples=True)
        if doc.cats[expected_class] > threshold
    )
    srsly.write_jsonl(file_out, stream, append=True, append_new_line=False)


if __name__ == "__main__":
    typer.run(filter_data)
