import itertools as it
import random

import prodigy
import srsly
from prodigy import set_hashes
from prodigy.components.loaders import JSONL
from spacy.matcher import Matcher


def stream_of_pairs(stream):
    candidates = []
    rep_stream = it.cycle(stream)
    while True:
        candidate = next(rep_stream)
        if random.random() < 0.5:
            candidates.append(candidate)
        if len(candidates) == 2:
            yield candidates
            candidates = []


def build_html(candidate):
    style = "padding-left: 0.5rem; padding-right: 0.5rem; margin-left: 0.5rem; margin-right: 0.5rem; background-color: #E5E7EB;"
    result = ""
    for tag in candidate["tags"]:
        result += f"<span style='{style}'>{tag}</span>"
    return f"{result}<p style='max-width: 90%;'>{candidate['title']}</p>"


def make_example(c1, c2):
    return {
        "text": "Which example is better?",
        "options": [
            {"id": c1["_input_hash"], "html": build_html(c1), **c1},
            {"id": c2["_input_hash"], "html": build_html(c2), **c2},
        ],
    }


@prodigy.recipe(
    "content_compare",
    dataset=("Dataset to save answers to", "positional", None, str),
    examples=("Examples to load from disk", "positional", None, str),
)
def content_compare(dataset, examples):
    # set up stream and set hashes just on text key
    stream = (item for item in JSONL(examples))
    stream = (set_hashes(ex, input_keys=("text")) for ex in stream)
    stream = (make_example(c1, c2) for c1, c2 in stream_of_pairs(stream))
    print(next(stream))

    # delete html key in output data
    def before_db(examples):
        for ex in examples:
            for opt in ex["options"]:
                del opt["html"]
        return examples

    return {
        "dataset": dataset,
        "stream": stream,
        "before_db": before_db,
        "view_id": "choice",
        "config": {"choice_auto_accept": True},
    }
