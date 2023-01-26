from pathlib import Path
from typing import Dict, Any

import srsly
import typer
import jinja2

def content_in_section(content: Dict[str, Any], section: Dict[str, Any]) -> bool:
    if all([content_tag in content['tags'] for content_tag in section['tags']]):
        if all([content_cls in content['classes'] for content_cls in section['classes']]):
            return True
    return False


def main(
    # fmt: off
    content_path: Path = typer.Argument(..., help="A content jsonl file"), 
    config_path: Path = typer.Argument(..., help="A config file"),
    template_path: Path = typer.Argument(..., help="A jinja2 tempalte"),
    file_out: Path = typer.Argument(..., help="Output html file that contains the html frontpage.")
    # fmt: on
):
    content_stream = srsly.read_jsonl(content_path)
    config = srsly.read_yaml(config_path)
    template = jinja2.Template(template_path.read_text())
    sections = config['sections']
    for content in content_stream:
        for section in sections:
            if "content" not in section:
                section["content"] = []
            if content_in_section(content=content, section=section):
                section["content"].append(content)
    
    rendered = template.render(name=config['name'], description=config['description'], sections=sections)
    Path(file_out).write_text(rendered)


if __name__ == "__main__":
    typer.run(main)
