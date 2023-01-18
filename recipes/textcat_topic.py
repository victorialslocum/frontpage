import prodigy
import spacy
import srsly
from prodigy import set_hashes
from prodigy.components.loaders import JSONL
from spacy.matcher import Matcher


@prodigy.recipe(
    "textcat_topic",
    dataset=("Dataset to save answers to", "positional", None, str),
    examples=("Examples to load from disk", "positional", None, str),
    model=("spaCy model to load", "positional", None, str),
    patterns=("Patterns to match from json file", "positional", None, str),
    tag=("Tag to filter", "positional", None, str)
)
def textcat_topic(dataset, examples, model, patterns, tag):
    # import spaCy and initialize matcher
    nlp = spacy.load(model)
    matcher = Matcher(nlp.vocab)

    # set up stream and set hashes just on text key
    stream = (item for item in JSONL(examples) if tag in item["tags"])
    stream = (set_hashes(ex, input_keys=("title")) for ex in stream)

    # add matcher pattern to underline
    patterns = srsly.read_json(patterns)
    matcher.add(tag, patterns)

    # Render title and description in HTML format for Prodigy as a generator object
    def add_html(examples):
        for ex in examples:
            doc = nlp(ex["description"])
            matches = matcher(doc)

            summary_highlight = ex["description"]
            for match_id, start, end in matches:
                span = doc[start:end]  # The matched span
                summary_highlight = summary_highlight.replace(
                    span.text, f"<b style='background-color: yellow;'>{span.text}</b>"
                )
            ex[
                "html"
            ] = f"<h3>{ex['title']}</h3><p><font size='3'>{summary_highlight}</font></p><a href='{ex['link']}'>LINK</a>"
            yield ex

    # delete html key in output data and add label key
    def before_db(examples):
        for ex in examples:
            ex["label"] = tag
            ex["text"] = ex["title"] + "\n" + ex["description"]
            del ex["html"]
            del ex["title"]
            del ex["description"]
        return examples

    return {
        "before_db": before_db,
        "dataset": dataset,
        "stream": add_html(stream),
        "view_id": "html",
    }
