#!/usr/bin/env python3

from pathlib import Path
import re
import xml.etree.ElementTree as ET


README_MARKER_START = "<!-- TEMPLATES:START -->"
README_MARKER_END = "<!-- TEMPLATES:END -->"


def text(parent: ET.Element, tag: str) -> str:
    element = parent.find(tag)
    return (element.text or "").strip() if element is not None else ""


def generate_templates_section(repo_root: Path) -> str:
    templates_dir = repo_root / "templates"
    template_files = sorted(templates_dir.glob("*.xml"))

    lines = [
        README_MARKER_START,
        "This repository provides Unraid Docker templates and matching icons for self-hosted apps.",
        "",
    ]

    for template_path in template_files:
        root = ET.parse(template_path).getroot()
        name = text(root, "Name")
        repository = text(root, "Repository")
        overview = text(root, "Overview")
        icon_url = text(root, "Icon")

        lines.append(f"### `{name}`")
        if icon_url:
            lines.append(f'<img src="{icon_url}" alt="{name} icon" width="64">')
        lines.append("")
        lines.append(f"- Template: `{template_path.as_posix().removeprefix(f'{repo_root.as_posix()}/')}`")
        if repository:
            lines.append(f"- Container image: `{repository}`")
        if overview:
            lines.append(f"- {overview}")
        lines.append("")

    lines.append(README_MARKER_END)
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    readme_path = repo_root / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    generated_section = generate_templates_section(repo_root)

    if README_MARKER_START not in readme or README_MARKER_END not in readme:
        raise RuntimeError("README template markers are missing.")

    pattern = re.compile(
        rf"{re.escape(README_MARKER_START)}.*?{re.escape(README_MARKER_END)}\n*",
        re.DOTALL,
    )
    updated = pattern.sub(generated_section + "\n", readme, count=1)
    readme_path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
