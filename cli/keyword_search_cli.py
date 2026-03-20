#!/usr/bin/env python3

import argparse
import string
import json
from pathlib import Path
from nltk.stem import PorterStemmer


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
                print(f"{i}. {movie['title']}")
            pass
        case _:
            parser.print_help()


def exec_search(query):

    s = process_string(query)
    path = Path("~/dev/rag-search-engine/data/movies.json").expanduser()
    with path.open() as fp:
        data = json.load(fp)
    result = []
    for movie in data["movies"]:
        title_tokens = process_string(movie["title"])
        if any(
            query_token in title_token
            for title_token in title_tokens
            for query_token in s
        ):
            result.append(movie)
    result.sort(key=lambda movie: movie["id"])
    return result[:5]


def process_string(s):
    path = Path("~/dev/rag-search-engine/data/stopwords.txt").expanduser()
    with path.open() as fp:
        STOPWORDS = fp.read().splitlines()
    s = s.lower()
    no_punct = s.translate(str.maketrans("", "", string.punctuation))
    tokens = [t for t in no_punct.split() if t not in STOPWORDS]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    return tokens


if __name__ == "__main__":
    main()
