from pathlib import Path
import argparse
import datetime
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Converts a JSON to a markdown file.")
    parser.add_argument("json_file", type=Path, help="The JSON file to convert.")

    args = parser.parse_args()
    if not args.json_file.exists():
        print("The JSON file does not exist.")
        return 1

    data = json.loads(args.json_file.read_text())
    if len(data) == 0:
        print("The JSON file is empty.")
        return 1

    data = data[0]

    title = data.get("title", "")
    date = data.get("date", "")
    if date == "":
        # If the date is not provided, use the current date
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    date = date.replace("/", "-")
    journal = data.get("journal", "")
    url = data.get("pdf_url", "")
    authors = data.get("authors", "")
    abstract = data.get("abstract", "")

    content = [
        "## Add new publication\n",
        f"- Title: {title}",
        f"- Authors: {authors}",
        f"- Date: {date}",
        f"- Journal: {journal}",
        f"- URL: {url}\n",
        f"*Abstract*\n {abstract}",
    ]

    sys.stdout.write("\n".join(content))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
