import arxiv
import srsly

search = arxiv.Search(
  query = "ti:dataset",
  max_results = 200,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

dataset = []

for result in search.results():
  dataset.append({"text": result.title, "meta": {"link": result.entry_id}})

srsly.write_jsonl('./data/data.jsonl', dataset)