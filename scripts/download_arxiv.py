import datetime as dt
from datetime import date
from pathlib import Path

import arxiv
import srsly
import typer
from rich.console import Console
from schemas import Content


def main(
    query: str = typer.Option(..., help="Query to send to arxiv"),
    tag: str = typer.Option(..., help="Comma seperated tags to add to data."),
    n: int = typer.Option(
        None,
        help="If specified, `max_age` is ignored. Refers to the number of results to save",
    ),
    path_out: Path = typer.Option("assets", help="Path to write file to."),
    max_age: Path = typer.Option(3, help="Max age of a result in days."),
):
    """Fetch data from arxiv."""
    console = Console(no_color=True)

    tags = ["arxiv"]
    tags.extend(tag.split(","))
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
        keep = created > (dt.date.today() - dt.timedelta(days=max_age))
        if keep or save_all:
            summary = str(result.summary).replace("\n", " ")
            content_item = Content(
                title=result.title,
                description=summary,
                link=result.entry_id,
                created=str(created)[:10],
                tags=tags,
                meta={"query": query},
            )
            dataset.append(dict(content_item))

    # Write file
    write_path = Path(path_out) / f"arxiv-{date.today()}.jsonl"
    srsly.write_jsonl(write_path, dataset, append=True, append_new_line=False)
    console.log(f"Written {len(dataset)} results into [bold]{write_path}.")


if __name__ == "__main__":
    typer.run(main)
