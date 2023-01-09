import datetime as dt
from datetime import date
from pathlib import Path

import arxiv
import srsly
import typer
from rich.console import Console


def main(
    query: str = typer.Option(...),
    tag: str = typer.Option(...),
    n: int = typer.Option(None),
    path_out: Path = typer.Option("assets"),
):
    console = Console(no_color=True)

    save_all = False if not n else True
    n = 100 if not n else n
    # Start the query
    items = arxiv.Search(
        query=query,
        max_results=int(n),
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    # Add items to dataset
    dataset = []
    for result in items.results():
        created = result.published.date()
        keep = created > (dt.date.today() - dt.timedelta(days=30))
        if keep or save_all:
            summary = str(result.summary).replace("\n", " ")
            dataset.append(
                {
                    "title": result.title,
                    "description": summary,
                    "meta": {
                        "link": result.entry_id,
                        "tags": ["arxiv", tag],
                        "query": query,
                        "created": str(created)[:10],
                    },
                }
            )

    # Write file
    write_path = Path(path_out) / f"arxiv-{date.today()}.jsonl"
    srsly.write_jsonl(write_path, dataset, append=True, append_new_line=False)
    console.log(f"Written {len(dataset)} results into [bold]{write_path}.")


if __name__ == "__main__":
    typer.run(main)
