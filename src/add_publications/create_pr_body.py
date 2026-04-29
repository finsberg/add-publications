from pathlib import Path
import argparse
import datetime
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Converts a JSON to a PR body markdown.")
    parser.add_argument("json_file", type=Path, help="The JSON file to convert.")

    args = parser.parse_args()
    if not args.json_file.exists():
        print("The JSON file does not exist.")
        return 1

    data = json.loads(args.json_file.read_text())
    if len(data) == 0:
        print("The JSON file is empty.")
        return 1

    content = ["## Add new publication(s)\n"]

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

        content.extend(
            [
                f"### {title}",
                f"- **Authors:** {authors}",
                f"- **Date:** {date}",
                f"- **Journal:** {journal}",
                f"- **URL:** {url}\n",
                f"*Abstract*\n {abstract}\n",
                "---\n",
            ]
        )

    sys.stdout.write("\n".join(content))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
