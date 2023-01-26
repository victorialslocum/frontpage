import datetime as dt
from pathlib import Path


def download_path(assets_folder="assets", *names):
    write_path = Path(assets_folder) / f"{dt.date.today()}"
    for name in names:
        if name == names[-1]:
            name = f"{name}.jsonl"
            write_path.mkdir(exist_ok=True, parents=True)
        print(write_path)
        write_path = write_path / name
    return write_path
