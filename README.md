<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Databot: An automatic recommender for papers about new datasets

Using Prodigy, spaCy, and arxiv to automatically detect new papers about datasets.

## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[spaCy projects documentation](https://spacy.io/usage/projects).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `data` | Create the dataset from arxiv query. |
| `preprocess` | Process data into Prodigy format. |
| `annotate` | Annotate prodigy with custom recipe. |
| `db_out` | Export Prodigy annotations to a jsonl file. |
| `train` | Train a spaCy textcat model with Prodigy annotations. |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| [``]() | Local |  |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->