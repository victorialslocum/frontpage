import arxiv
import srsly

# search 1: key words in title, key phrase in abstract
search_1 = arxiv.Search(
    query='ti:dataset OR ti:corpus OR ti:database OR abs:"a new dataset"',
    max_results=400,
    sort_by=arxiv.SortCriterion.SubmittedDate,
)

# search 2: more broad search to get more outliers
search_2 = arxiv.Search(
    query="ti:data",
    max_results=100,
    sort_by=arxiv.SortCriterion.SubmittedDate,
)

# initialize dataset
dataset = []

# iterate through results and append title, summary and link to the dataset
for search in [search_1, search_2]:
    for result in search.results():
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
