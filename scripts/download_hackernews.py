import asyncio
import datetime as dt
from datetime import date
from pathlib import Path

import httpx
import srsly
import typer
from rich.console import Console
from schemas import Content


async def fetch_url(url, client):
    r = await client.get(url)
    return r


async def fetch_urls(urls):
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*[fetch_url(u, client) for u in urls])
    return [r.json() for r in results]


def main(
    path_out: Path = typer.Option("assets", help="Path to write file into."),
    n: int = typer.Option(100, help="Only looks at the top `n` stories."),
    max_age: int = typer.Option(3, help="Max age of a result in days."),
):
    """Fetch data from hackernews."""
    console = Console(no_color=True)

    # Start the query
    ids = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()
    urls = [f"https://hacker-news.firebaseio.com/v0/item/{i}.json" for i in ids]
    responses = asyncio.run(fetch_urls(urls=urls))

    # Add items to dataset
    dataset = []
    for result in responses[:n]:
        if "url" in result.keys():
            created = dt.datetime.fromtimestamp(result["time"])
            if created > dt.datetime.now() - dt.timedelta(days=max_age):
                content_item = Content(
                    title=result["title"],
                    description=result["url"],
                    link=result["url"],
                    created=created.strftime("%Y-%m-%d"),
                    tags=["hackernews"],
                    meta={
                        "score": result["score"],
                    },
                )
                dataset.append(dict(content_item))

    # Write file
    write_path = Path(path_out) / f"hackernews-{date.today()}.jsonl"
    srsly.write_jsonl(write_path, dataset, append=True, append_new_line=False)
    console.log(f"Written {len(dataset)} results into [bold]{write_path}.")


if __name__ == "__main__":
    typer.run(main)
