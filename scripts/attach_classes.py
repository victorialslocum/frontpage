from pathlib import Path

import spacy
import srsly
import typer


def attach_classes(
    # fmt: off
    content_in: Path = typer.Argument(..., help="A file with content as jsonl to filter"), 
    spacy_model: str = typer.Argument(..., help="A trained spaCy model"), 
    file_out: Path = typer.Argument(..., help="A file to write the filtered content into"), 
    # fmt: on
):
    nlp = spacy.load(spacy_model)
    stream = srsly.read_jsonl(content_in)
    stream = ({**d, "text": f"{d['title']} {d['description']}"} for d in stream)
    text_stream = (ex["text"] for ex in stream)
    together = zip(text_stream, stream)
    stream = (
        {**ex, "classes": {k: v for k, v in doc.cats.items()}}
        for doc, ex in nlp.pipe(together, as_tuples=True)
    )
    srsly.write_jsonl(file_out, stream, append=True, append_new_line=False)


if __name__ == "__main__":
    typer.run(attach_classes)
