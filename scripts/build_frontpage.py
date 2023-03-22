import datetime as dt 
from pathlib import Path
from typing import Dict, Any

import srsly
import typer
import jinja2

def content_in_section(content: Dict[str, Any], section: Dict[str, Any]) -> bool:
    # Check for matching tags, otherwise it's another section
    if any([content_tag not in content['tags'] for content_tag in section['tags']]):
        return False
    section_req_class_names = [_['name'] for _ in section['classes']]
    section_req_class_conf = {_['name']:_['threshold'] for _ in section['classes']}

    # Is a relevant class missing? If so, skip.
    for cls_name in section_req_class_names:
        if cls_name not in content['classes']:
            return False
    
    # Is a relevant class predicted with low confidence? If so, skip.
    for pred_cls, pred_conf in content['classes'].items():
        if pred_cls in section_req_class_names:
            if pred_conf < section_req_class_conf[pred_cls]:
                return False
    return True


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
    for section in sections:
        section["content"] = sorted(section["content"], key=lambda d: d['created'], reverse=True)
        section["content"] = section["content"][:section.get("n", 20)]
    rendered = template.render(name=config['name'], description=config['description'], sections=sections, today=dt.date.today())
    Path(file_out).write_text(rendered)


if __name__ == "__main__":
    typer.run(main)
