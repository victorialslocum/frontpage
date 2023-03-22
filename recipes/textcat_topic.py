import prodigy
import spacy
import srsly
import random 

from prodigy import set_hashes
from prodigy.components.loaders import JSONL
from prodigy.components.sorters import prefer_high_scores
from prodigy.components.filters import filter_duplicates, filter_tasks
from prodigy.components.db import connect



@prodigy.recipe(
    "textcat_topic",
    # fmt: off
    dataset=("Dataset to save answers to", "positional", None, str),
    examples=("Examples to load from disk", "positional", None, str),
    model=("spaCy model to load", "positional", None, str),
    patterns=("Patterns to match from json file", "positional", None, str),
    tags=("Comma-separated list of tags to filter items from the dataset", "positional", None, lambda d: d.split(",")),
    label=("Label for annotated data", "positional", None, str),
    more_positives=("Adapt the feed to show more pattern matched examples", "flag", None, bool),
    # fmt: on
)
def textcat_topic(
    dataset, examples, model, patterns, tags, label, more_positives=False
):
    # import spaCy and initialize matcher
    nlp = spacy.load(model)

    # set up stream and set hashes
    stream = (
        item for item in JSONL(examples) if all(tag in item["tags"] for tag in tags)
    )
    stream = ({**d, "label": label} for d in stream)
    stream = (set_hashes(ex, input_keys=("title"), task_keys=("label")) for ex in stream)
    stream = filter_duplicates(stream)

    # remove duplicates, if any
    db = connect()
    stream = filter_tasks(stream, db.get_task_hashes(dataset))

    # add matcher pattern to underline
    patterns = srsly.read_jsonl(patterns)
    ruler = nlp.add_pipe("span_ruler")
    ruler.add_patterns(patterns)

    # Render title and description in HTML format for Prodigy as a generator object
    def prep_examples(examples):
        for ex in examples:
            doc = nlp(ex["description"])

            summary_highlight = ex["description"]
            for span in doc.spans["ruler"]:
                summary_highlight = summary_highlight.replace(
                    span.text, f"<b style='background-color: yellow;'>{span.text}</b>"
                )

            ex[
                "html"
            ] = f"<h3>{ex['title']}</h3><p><font size='3'>{summary_highlight}</font></p><a href='{ex['link']}'>LINK</a>"
            ex["label"] = label

            if more_positives:
                yield float(len(doc.spans["ruler"])), ex
            else:
                yield ex

    # delete html key in output data and add label key
    def before_db(examples):
        for ex in examples:
            ex["text"] = ex["title"] + "\n" + ex["description"]
            del ex["html"]
            del ex["title"]
            del ex["description"]
        return examples

    stream = prep_examples(stream)
    if more_positives:
        stream = prefer_high_scores(stream)

    return {
        "before_db": before_db,
        "dataset": dataset,
        "stream": stream,
        "view_id": "classification",
    }
