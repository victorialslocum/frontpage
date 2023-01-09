from pathlib import Path
from schemas import Content
import srsly
import typer


def main(folder: Path, out: Path):
    """Concat all files and double-check the schema."""
    full_data = []
    for file in folder.glob("*.jsonl"):
        full_data.extend([dict(Content(**item)) for item in srsly.read_jsonl(file)])
    srsly.write_jsonl(out, full_data)


if __name__ == "__main__":
    typer.run(main)
