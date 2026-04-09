import math
import pickle
from collections import Counter, defaultdict
from pathlib import Path

import util


class Inverted_index:

    def __init__(self):
        self.index: dict[str, set[int]] = {}
        self.docmap: dict[int, dict] = {}
        self.term_frequencies: defaultdict[int, Counter[str]] = defaultdict(Counter)

    def __add_document(self, doc_id, text):
        tokens = util.process_string(text)
        for token in tokens:
            self.index.setdefault(token, set()).add(doc_id)
            self.term_frequencies[doc_id][token] += 1

    def get_documents(self, term):
        ids = self.index.get(util.process_string(term)[0], set())
        return sorted(ids)

    def get_tf(self, doc_id, term):
        if self.term_frequencies[doc_id]:
            return self.term_frequencies[doc_id][term]
        return 0

    def get_idf(self, term):
        token = util.process_string(term)[0]
        if token in self.index:
            df = len(self.index[token])
            idf = math.log((len(self.docmap) + 1) / (df + 1))
            return idf
        return 0

    def build(self):
        docs = util.load_documents("movies.json")
        for doc in docs["movies"]:
            self.docmap[doc["id"]] = doc
            self.__add_document(doc["id"], f"{doc['title']} {doc['description']}")

    def save(self, cache_dir):
        cache_path = Path(cache_dir).expanduser()
        cache_path.mkdir(parents=True, exist_ok=True)

        idx_path = cache_path / "index.pkl"
        with idx_path.open("wb") as fd:
            pickle.dump(self.index, fd, pickle.HIGHEST_PROTOCOL)

        docmap_path = cache_path / "docmap.pkl"
        with docmap_path.open("wb") as fd:
            pickle.dump(self.docmap, fd, pickle.HIGHEST_PROTOCOL)

        term_frequencies_path = cache_path / "term_frequencies.pkl"
        with term_frequencies_path.open("wb") as fd:
            pickle.dump(self.term_frequencies, fd, pickle.HIGHEST_PROTOCOL)

    def load(self, cache_dir):
        cache_path = Path(cache_dir).expanduser()

        idx_path = cache_path / "index.pkl"
        if not idx_path.exists():
            raise FileNotFoundError(idx_path)

        docmap_path = cache_path / "docmap.pkl"
        if not docmap_path.exists():
            raise FileNotFoundError(docmap_path)

        term_frequencies_path = cache_path / "term_frequencies.pkl"
        if not term_frequencies_path.exists():
            raise FileNotFoundError(term_frequencies_path)

        with idx_path.open("rb") as fd:
            self.index = pickle.load(fd)

        with docmap_path.open("rb") as fd:
            self.docmap = pickle.load(fd)

        with term_frequencies_path.open("rb") as fd:
            self.term_frequencies = pickle.load(fd)
