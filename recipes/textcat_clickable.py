import itertools as it
import random

import prodigy
from prodigy import set_hashes
from prodigy.components.loaders import JSONL


def build_html(candidate):
    style = "padding-left: 0.5rem; padding-right: 0.5rem; margin-left: 0.5rem; margin-right: 0.5rem; background-color: #E5E7EB;"
    result = ""
    for tag in candidate["tags"]:
        result += f"<span style='{style}'>{tag}</span>"
    return {
        **candidate,
        "html": f"{result}<p style='max-width: 90%;'>{candidate['title']}</p>",
        "label": "clickable",
        "meta": {**candidate["meta"], "link": candidate["link"]},
    }


def lazy_shuffle(stream):
    rep_stream = it.cycle(stream)
    while True:
        candidate = next(rep_stream)
        if random.random() < 0.1:
            yield candidate


@prodigy.recipe(
    "textcat_clickable",
    dataset=("Dataset to save answers to", "positional", None, str),
    examples=("Examples to load from disk", "positional", None, str),
)
def textcat_clickable(dataset, examples):
    # set up stream and set hashes just on text key
    stream = (set_hashes(ex, input_keys=("title")) for ex in JSONL(examples))
    stream = (build_html(ex) for ex in lazy_shuffle(stream))

    # delete html key in output data and add label key
    def before_db(examples):
        for ex in examples:
            del ex["html"]
        return examples

    return {
        "before_db": before_db,
        "dataset": dataset,
        "stream": stream,
        "view_id": "classification",
    }
