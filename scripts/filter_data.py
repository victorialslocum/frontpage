import spacy 
import typer
import srsly

def filter_data(content_in, spacy_model, tag, expected_class, file_out):
    nlp = spacy.load(spacy_model)
    stream = srsly.read_jsonl(content_in)
    stream = (ex for ex in stream if tag in ex['tags'])
    stream = ({**d, 'text': f"{d['title']} {d['description']}"} for d in stream)
    text_stream = (ex['text'] for ex in stream)
    together = zip(text_stream, stream)
    stream = (ex for doc, ex in nlp.pipe(together, as_tuples=True) if doc.cats[expected_class] > 0.5)
    srsly.write_jsonl(file_out, stream, append=True, append_new_line=False)

if __name__ == "__main__":
    typer.run(filter_data)
