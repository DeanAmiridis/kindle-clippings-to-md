#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import re

ENV_FILE = Path(__file__).parent / "kindle.env"

def load_env():
    env = {}

    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip().strip('"')

    return env

def save_env(clippings_path, output_path):
    ENV_FILE.write_text(
        f'CLIPPINGS_PATH="{clippings_path}"\n'
        f'OUTPUT_PATH="{output_path}"\n',
        encoding="utf-8"
    )

def get_path(prompt, current=None):
    if current:
        value = input(f"{prompt} [{current}]: ").strip()
        return Path(value.strip('"').strip("'")).expanduser() if value else Path(current).expanduser()

    value = input(f"{prompt}: ").strip()
    return Path(value.strip('"').strip("'")).expanduser()

def parse_clipping(block):
    lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
    if len(lines) < 2:
        return None

    title_line = lines[0]
    meta_line = lines[1]
    text = "\n".join(lines[2:]).strip()

    author = ""
    title = title_line

    m = re.match(r"^(.*?)\s+\((.*?)\)$", title_line)
    if m:
        title = m.group(1).strip()
        author = m.group(2).strip()

    item_type = ""
    page = ""
    location = ""
    added = ""

    type_match = re.search(r"Your\s+(.+?)\s+on", meta_line, re.I)
    if type_match:
        item_type = type_match.group(1).strip()

    page_match = re.search(r"page\s+([\d\-]+)", meta_line, re.I)
    if page_match:
        page = page_match.group(1)

    loc_match = re.search(r"location\s+([\d\-]+)", meta_line, re.I)
    if loc_match:
        location = loc_match.group(1)

    added_match = re.search(r"Added on\s+(.+)$", meta_line, re.I)
    if added_match:
        added = added_match.group(1).strip()

    return {
        "title": title,
        "author": author,
        "type": item_type,
        "page": page,
        "location": location,
        "added": added,
        "text": text,
    }

def to_markdown(clippings):
    grouped = {}
    for c in clippings:
        grouped.setdefault(c["title"], []).append(c)

    md = ["# Kindle My Clippings Export", ""]

    for title, items in grouped.items():
        author = items[0].get("author", "")
        heading = f"## {title}"
        if author:
            heading += f" — {author}"

        md.extend([heading, ""])

        for c in items:
            details = []

            if c["type"]:
                details.append(c["type"])
            if c["page"]:
                details.append(f"page {c['page']}")
            if c["location"]:
                details.append(f"location {c['location']}")
            if c["added"]:
                details.append(f"added {c['added']}")

            if details:
                md.append(f"*{' | '.join(details)}*")
                md.append("")

            if c["text"]:
                md.append(f"> {c['text'].replace(chr(10), chr(10) + '> ')}")
                md.append("")

            md.append("---")
            md.append("")

    return "\n".join(md)

def main():
    env = load_env()

    clippings_path = get_path("Path to My Clippings.txt", env.get("CLIPPINGS_PATH"))
    output_dir = get_path("Output folder path", env.get("OUTPUT_PATH"))

    if not clippings_path.exists():
        raise FileNotFoundError(f"File not found: {clippings_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    date_prefix = datetime.now().strftime("%m%d%Y")
    output_file = output_dir / f"{date_prefix}-My Clippings.md"

    content = clippings_path.read_text(encoding="utf-8-sig", errors="replace")
    blocks = content.split("==========")

    clippings = []
    for block in blocks:
        parsed = parse_clipping(block)
        if parsed:
            clippings.append(parsed)

    output_file.write_text(to_markdown(clippings), encoding="utf-8")

    save_env(clippings_path, output_dir)

    print(f"Exported {len(clippings)} clippings to:")
    print(output_file)

if __name__ == "__main__":
    main()