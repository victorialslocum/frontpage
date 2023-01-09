import datetime as dt
from pathlib import Path

import httpx
import srsly
import typer
from rich.console import Console


def main(subreddit: str = typer.Option(...), tag: str = typer.Option(...)):
    console = Console(no_color=True)
    resp_data = httpx.get(f"https://www.reddit.com/r/{subreddit}.json").json()["data"][
        "children"
    ]
    dataset = []
    for child in resp_data:
        created = dt.datetime.fromtimestamp(child["data"]["created_utc"])
        if created > dt.datetime.now() - dt.timedelta(days=2):
            dataset.append(
                {
                    "title": child["data"]["title"],
                    "description": child["data"]["selftext"],
                    "meta": {
                        "link": child["data"]["permalink"],
                        "tags": list(set(["reddit", tag, subreddit])),
                        "num_comments": child["data"]["num_comments"],
                        "created": created.strftime("%Y-%m-%d"),
                    },
                }
            )

    out_path = Path("assets") / f"reddit-{subreddit}-{dt.date.today()}.jsonl"
    srsly.write_jsonl(out_path, dataset)
    console.log(f"Written {len(dataset)} results in {out_path}.")


if __name__ == "__main__":
    typer.run(main)
