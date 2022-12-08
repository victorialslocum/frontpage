import srsly

raw_dataset = srsly.read_jsonl("assets/raw/raw_data.jsonl")

print(raw_dataset)

process_data = []

for paper in raw_dataset:
    process_data.append(
        {
            "text": f"{paper['title']}\n{paper['summary']}",
            "title": paper["title"],
            "summary": paper["summary"],
            "meta": {"link": paper["link"]},
        }
    )

srsly.write_jsonl("assets/data.jsonl", process_data)
