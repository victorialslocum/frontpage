from pathlib import Path

import srsly
import typer
from jinja2 import Environment

env = Environment()

template = env.from_string(
    """
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <div class="relative mx-auto h-full max-w-prose text-md">
    <h1 class="text-6xl pt-4 font-bold"><span class="underline">Your</span> FrontPage</h1>
    <br>
    {{links}}
    </div>
</body>
</html>
"""
)


def main(
    # fmt: off
    content: Path = typer.Argument(..., help="A content jsonl file"), 
    file_out: Path = typer.Argument(..., "Output html file that contains the html frontpage.")
    # fmt: on
):
    content_stream = srsly.read_jsonl(content)

    def make_elem(item):
        result = f"""<a class="hover:underline decoration-2 decoration-green-600" href='{item['link']}'>{item['title']}"""
        for tag in item["tags"]:
            result += f"<span class='px-2 mx-2 bg-gray-200'>{tag}</span>"
        return f"{result}</a>"

    elems = "<br>".join([make_elem(e) for e in content_stream])
    rendered = template.render(links=elems)
    Path(file_out).write_text(rendered)


if __name__ == "__main__":
    typer.run(main)
