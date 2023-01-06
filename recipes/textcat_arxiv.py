import prodigy
from prodigy.components.loaders import JSONL
from prodigy import set_hashes
import spacy
from spacy.matcher import Matcher
import srsly


@prodigy.recipe(
    "textcat_arxiv",
    dataset=("Dataset to save answers to", "positional", None, str),
    examples=("Examples to load from disk", "positional", None, str),
    model=("spaCy model to load", "positional", None, str),
    patterns=("Patterns to match from json file", "positional", None, str)
)
def textcat_arxiv(dataset, examples, model, patterns):
    # import spaCy and initialize matcher
    nlp = spacy.load(model)
    matcher = Matcher(nlp.vocab)

    # set up stream and set hashes just on text key
    stream = JSONL(examples)
    stream = (set_hashes(ex, input_keys=("text")) for ex in stream)

    # add matcher pattern to underline
    patterns = srsly.read_json(patterns)
    matcher.add("Dataset", patterns)

    # Render title and description in HTML format for Prodigy as a generator object
    def add_html(examples):
        for ex in examples:
            doc = nlp(ex["summary"])
            matches = matcher(doc)

            summary_highlight = ex["summary"]
            for match_id, start, end in matches:
                span = doc[start:end]  # The matched span
                summary_highlight = summary_highlight.replace(
                    span.text, f"<u>{span.text}</u>"
                )
            ex[
                "html"
            ] = f"<h3>{ex['title']}</h3><p><font size='3'>{summary_highlight}</font></p>"
            yield ex

    # delete html key in output data and add label key
    def before_db(examples):
        for ex in examples:
            ex["label"] = "dataset"
            del ex["html"]
        return examples

    return {
        "before_db": before_db,
        "dataset": dataset,
        "stream": add_html(stream),
        "view_id": "html",
    }
