#!/usr/bin/env python3

import argparse
import sys

import util
from inverted_index import Inverted_index


def main() -> None:
    CACHE_DIR = "./cache"

    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    subparsers.add_parser("build", help="'Build the search index")

    tf_parser = subparsers.add_parser("tf", help="get term frequency for doc and term")
    tf_parser.add_argument("doc_id", type=int)
    tf_parser.add_argument("term", type=str)

    idf_parser = subparsers.add_parser(
        "idf", help="get the inverse document frequency for term"
    )
    idf_parser.add_argument("term", type=str)

    args = parser.parse_args()

    match args.command:

        case "tf":
            idx = Inverted_index()
            try:
                idx.load(CACHE_DIR)
            except FileNotFoundError:
                print("no cached index found. Run build first")
                sys.exit(1)
            print(f"{idx.get_tf(args.doc_id, args.term)}")
            pass

        case "idf":
            idx = Inverted_index()
            try:
                idx.load(CACHE_DIR)
            except FileNotFoundError:
                print("no cached index found. Run build first")
                sys.exit(1)
            print(
                f"Inverse document frequency of '{args.term}': {idx.get_idf(args.term):.2f}"
            )
            pass

        case "build":
            idx = Inverted_index()
            idx.build()
            idx.save(CACHE_DIR)
            pass

        case "search":
            idx = Inverted_index()
            try:
                idx.load(CACHE_DIR)
            except FileNotFoundError:
                print("no cached index found. run build first")
                sys.exit(1)
            result = exec_search(args.query, idx)
            print(f"searching for: {args.query}")
            for i, doc in enumerate(result, start=1):
                movie = idx.docmap[doc]
                print(f"{i}. id: {movie['id']} title: {movie['title']}")
            pass

        case _:
            parser.print_help()


def exec_search(query, idx):

    q = util.process_string(query)
    result = set()

    for query_token in q:
        result.update(idx.get_documents(query_token))
        if len(result) >= 5:
            break

    return sorted(result)[:5]


if __name__ == "__main__":
    main()
