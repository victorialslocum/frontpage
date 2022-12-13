import srsly

# import raw arxiv data
raw_dataset = srsly.read_jsonl("assets/raw/raw_data.jsonl")

# initialize dataset
process_data = []

# iterate through papers and refactor data into correct form
for paper in raw_dataset:
    process_data.append(
        {
            "text": f"{paper['title']}\n{paper['summary']}",
            "title": paper["title"],
            "summary": paper["summary"],
            "meta": {"link": paper["link"]},
        }
    )

# write data
srsly.write_jsonl("assets/data.jsonl", process_data)
