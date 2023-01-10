<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: FrontPage: An Prodigy project to make a personal front-page.

Using Prodigy, spaCy, and friends ... this project allows you to make your own frontpage of the internet.

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
| `download` | Download data from sources. |
| `preprocess` | Process data into Prodigy format. |
| `annotate` | Annotate prodigy with custom recipe. |
| `db_out` | Export Prodigy annotations to a jsonl file. |
| `train` | Train a spaCy textcat model with Prodigy annotations. |
| `build` | Builds your frontpage. |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `fetch` | `download` &rarr; `preprocess` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| [``]() | Local |  |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->
