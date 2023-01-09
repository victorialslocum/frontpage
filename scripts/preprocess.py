from pathlib import Path

import srsly
import typer


def process(item):
    return {
        "text": f"{item['title']}\n{item['description']}",
        "title": item["title"],
        "description": item["description"],
        "meta": item["meta"],
    }


def main(folder: Path, out: Path):
    full_data = []
    for file in folder.glob("*.jsonl"):
        full_data.extend([process(item) for item in srsly.read_jsonl(file)])
    srsly.write_jsonl(out, full_data)


if __name__ == "__main__":
    typer.run(main)
