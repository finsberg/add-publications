from textwrap import dedent
from pathlib import Path
import argparse
import datetime
import json

template = dedent(
    """---
title: {title}
collection: publications
permalink: /publication/{slug}
excerpt: '{short_description}'
date: {date}
venue: '{journal}'
paperurl: '{url}'
authors: '{authors}'
---

{abstract}
    """
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Converts a JSON to markdown files.")
    parser.add_argument("json_file", type=Path, help="The JSON file to convert.")
    parser.add_argument("outdir", type=Path, help="Output directory for the bibitem files.")

    args = parser.parse_args()
    if not args.json_file.exists():
        print("The JSON file does not exist.")
        return 1

    if not args.outdir.exists():
        print("The output directory does not exist.")
        return 1

    data = json.loads(args.json_file.read_text())
    if len(data) == 0:
        print("The JSON file is empty.")
        return 1

    # Loop through ALL publications
    for item in data:
        title = item.get("title", "")
        date = item.get("date", "")
        if date == "":
            # If the date is not provided, use the current date
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        date = date.replace("/", "-")
        journal = item.get("journal", "")
        url = item.get("pdf_url", "")
        authors = item.get("authors", "")
        abstract = item.get("abstract", "")
        short_description = abstract.split(".")[0] if abstract else ""
        slug = "-".join(title.lower().replace(" ", "-")[:30].split("-")[:-1])

        # Fallback slug if the title is very short
        if not slug:
            slug = title.lower().replace(" ", "-")[:30]

        content = template.format(
            title=title,
            date=date,
            journal=journal,
            url=url,
            authors=authors,
            abstract=abstract,
            short_description=short_description,
            slug=slug,
        )
        out_file = args.outdir / f"{date}-{slug}.md"
        out_file.write_text(content)
        print(f"File written to {out_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
