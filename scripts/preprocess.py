import itertools as it
from pathlib import Path

import srsly
import typer
from schemas import Content

def remove_meta(d):
    if 'meta' in d:
        del d['meta']
    return d

def dedup(stream):
    uniq = {}
    for ex in stream:
        uniq[hash(ex['title'])] = ex
    for ex in uniq.values():
        yield ex

def main(folder: Path, out: Path):
    """Concat all files and double-check the schema."""
    glob = folder.glob("**/*.jsonl")
    full_data = it.chain(*list(srsly.read_jsonl(file) for file in glob))
    stream = (dict(Content(**item)) for item in dedup(full_data))
    srsly.write_jsonl(out, stream)


if __name__ == "__main__":
    typer.run(main)
