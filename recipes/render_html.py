import prodigy 
from prodigy.components.loaders import JSONL
from prodigy import set_hashes

@prodigy.recipe(
    "render_html",
    dataset=("Dataset to save answers to", "positional", None, str),
    examples=("Examples to load from disk", "positional", None, str),
)
def render_html(dataset, examples):
    stream = JSONL(examples)
    stream = (set_hashes(ex, input_keys=("text")) for ex in stream)

    def add_html(examples):
        for ex in examples:
            ex["html"] = f"<h3>{ex['title']}</h3><p><font size='3'>{ex['summary']}</font></p>"
            yield ex

    return {
        "dataset": dataset,
        "stream": add_html(stream),
        "view_id": "html",
    }