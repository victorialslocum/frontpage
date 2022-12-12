import prodigy
from prodigy.components.loaders import JSONL
from prodigy import set_hashes
import spacy
from spacy.matcher import Matcher


@prodigy.recipe(
    "render_html",
    dataset=("Dataset to save answers to", "positional", None, str),
    examples=("Examples to load from disk", "positional", None, str),
)
def render_html(dataset, examples):
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)

    stream = JSONL(examples)
    stream = (set_hashes(ex, input_keys=("text")) for ex in stream)

    patterns = [
        [
            {
                "LEMMA": {
                    "IN": [
                        "present",
                        "introduce",
                        "propose",
                        "publish",
                        "provide",
                        "derive",
                        "construct",
                    ]
                }
            },
            {"OP": "{,6}"},
            {"POS": "DET"},
            {"OP": "{,6}"},
            {"LOWER": {"IN": ["database", "dataset", "corpus"]}},
        ],
    ]
    matcher.add("Dataset", patterns)

    def add_html(examples):
        for ex in examples:
            doc = nlp(ex["summary"])
            matches = matcher(doc)

            summary_highlight = ex["summary"]
            for match_id, start, end in matches:
                string_id = nlp.vocab.strings[match_id]  # Get string representation
                span = doc[start:end]  # The matched span
                print(match_id, string_id, start, end, span.text)
                summary_highlight = summary_highlight.replace(
                    span.text, f"<u>{span.text}</u>"
                )
            ex[
                "html"
            ] = f"<h3>{ex['title']}</h3><p><font size='3'>{summary_highlight}</font></p>"
            yield ex

    def before_db(examples):
        for ex in examples:
            del ex["html"]
        return examples

    return {
        "before_db": before_db,
        "dataset": dataset,
        "stream": add_html(stream),
        "view_id": "html",
    }
