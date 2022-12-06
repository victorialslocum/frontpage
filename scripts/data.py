import arxiv
import srsly

search = arxiv.Search(
  query = "ti:dataset",
  max_results = 200,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

dataset = []
dataset_titles = []

for result in search.results():
  dataset.append({"title": result.title, "summary": result.summary, "published": result.published, "id": result.entry_id})
  dataset_titles.append({"text": result.title})

srsly.write_json('./data/articles_200.json', dataset)
srsly.write_jsonl('./data/data.jsonl', dataset_titles)