from datetime import date, timedelta

import arxiv
import srsly

today = date.today()
yesterday = today - timedelta(days=1)

queries = {
    'ti:dataset OR ti:corpus OR ti:database OR abs:"a new dataset"': 30,
    "ti:data": 20,
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
        if str(result.updated)[0:10] == str(yesterday):
            summary = str(result.summary).replace("\n", " ")
            dataset.append(
                {
                    "title": result.title,
                    "summary": summary,
                    "link": result.entry_id,
                }
            )

# write file
srsly.write_jsonl(f"./assets/raw/raw_data_{str(yesterday)}.jsonl", dataset)
