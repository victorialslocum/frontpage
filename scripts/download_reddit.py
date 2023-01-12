import datetime as dt
from pathlib import Path

import httpx
import srsly
import typer
from rich.console import Console
from schemas import Content


def main(
    subreddit: str = typer.Option(..., help="Name of the subreddit to scrape."),
    tag: str = typer.Option(..., help="Comma seperated tags to add to data."),
    keep_reddit: bool = typer.Option(
        False, is_flag=True, help="Keep links that are hosted by reddit."
    ),
):
    """Fetch data from reddit."""
    subreddit = subreddit.lower()
    console = Console(no_color=True)
    resp_data = httpx.get(f"https://www.reddit.com/r/{subreddit}.json").json()
    resp_data = resp_data["data"]["children"]
    dataset = []
    for child in resp_data:
        created = dt.datetime.fromtimestamp(child["data"]["created_utc"])
        url = child["data"]["url"]
        keep = False
        if (not keep_reddit) and "reddit" in url:
            keep = True
        if not url.startswith("http"):
            keep = False
        if keep:
            if created > dt.datetime.now() - dt.timedelta(days=2):
                content_item = Content(
                    title=child["data"]["title"],
                    description=child["data"]["selftext"],
                    link=url,
                    created=created.strftime("%Y-%m-%d"),
                    tags=list(set(["reddit", tag, subreddit])),
                    meta={
                        "num_comments": child["data"]["num_comments"],
                    },
                )
                dataset.append(dict(content_item))

    out_path = Path("assets") / f"reddit-{subreddit}-{dt.date.today()}.jsonl"
    srsly.write_jsonl(out_path, dataset)
    console.log(f"Written {len(dataset)} results in [bold]{out_path}.")


if __name__ == "__main__":
    typer.run(main)
