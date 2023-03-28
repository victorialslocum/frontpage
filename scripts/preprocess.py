import itertools as it
from pathlib import Path

import srsly
import typer
from prodigy import set_hashes
from prodigy.components.filters import filter_duplicates
from schemas import Content

def remove_meta(d):
    if 'meta' in d:
        del d['meta']
    return d

def main(folder: Path, out: Path):
    """Concat all files and double-check the schema."""
    glob = folder.glob("**/*.jsonl")
    full_data = it.chain(*list(srsly.read_jsonl(file) for file in glob))

    stream = (set_hashes(remove_meta(eg)) for eg in full_data)
    stream = filter_duplicates(stream, by_input=True, by_task=True)
    stream = (dict(Content(**item)) for item in stream)
    srsly.write_jsonl(out, full_data)


if __name__ == "__main__":
    typer.run(main)
