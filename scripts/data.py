import arxiv
import srsly

queries = {
    'ti:dataset OR ti:corpus OR ti:database OR abs:"a new dataset"': 400,
    "ti:data": 100
}

dataset = []
for query, n in queries.items():
    # Start the query
    items = arxiv.Search(
        query=query,
        max_results=n,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    # Add items to dataset
    for result in items.results():
        summary = str(result.summary).replace("\n", " ")
        dataset.append(
            {
                "title": result.title,
                "summary": summary,
                "link": result.entry_id,
            }
        )

# write file
srsly.write_jsonl("./assets/raw/raw_data.jsonl", dataset)