from pathlib import Path

import srsly
import typer
from prodigy import set_hashes
from prodigy.components.filters import filter_duplicates
from schemas import Content


def main(folder: Path, out: Path):
    """Concat all files and double-check the schema."""
    full_data = []
    for file in folder.glob("**/*.jsonl"):
        full_data.extend(list(srsly.read_jsonl(file)))

    stream = (set_hashes(eg) for eg in full_data)
    stream = filter_duplicates(stream, by_input=True, by_task=True)
    stream = (dict(Content(**item)) for item in stream)
    srsly.write_jsonl(out, full_data)


if __name__ == "__main__":
    typer.run(main)
