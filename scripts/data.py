import arxiv
import srsly

search_1 = arxiv.Search(
    query='ti:dataset OR ti:corpus OR ti:database OR abs:"a new dataset"',
    max_results=200,
    sort_by=arxiv.SortCriterion.SubmittedDate,
)
search_2 = arxiv.Search(
    query="ti:data",
    max_results=50,
    sort_by=arxiv.SortCriterion.SubmittedDate,
)

dataset = []

for search in [search_1, search_2]:
    for result in search.results():
        summary = str(result.summary).replace("\n", " ")
        dataset.append(
            {
                "title": result.title, "summary": summary,
                "link": result.entry_id,
            }
        )

srsly.write_jsonl("./assets/raw/raw_data.jsonl", dataset)

## add new things to file
# add new things to one file for each day and then consolodate
# I think we'll be able to filter by date