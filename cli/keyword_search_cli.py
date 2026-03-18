#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            result = exec_search(args.query)
            print(f"Searching for: {args.query}")
            for i, movie in enumerate(result, start=1):
                print(f"{i}. {movie["title"]}")
            pass
        case _:
            parser.print_help()


def exec_search(query):

    path = Path("~/dev/rag-search-engine/data/movies.json").expanduser()
    with path.open() as fp:
        data = json.load(fp)
    result = []
    for movie in data["movies"]:
        if query in movie["title"]:
            result.append(movie)
    result.sort(key=lambda movie: movie["id"])
    return result[:5]


if __name__ == "__main__":
    main()
