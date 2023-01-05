import srsly

# import raw arxiv data
raw_dataset = srsly.read_jsonl("assets/raw/raw_data.jsonl")

def process(paper):
    return {
        "text": f"{paper['title']}\n{paper['summary']}",
        "title": paper["title"],
        "summary": paper["summary"],
        "meta": {"link": paper["link"]},
    }

# write data
processed_data = [process(p) for p in process_data]
srsly.write_jsonl("assets/data.jsonl", processed_data)
