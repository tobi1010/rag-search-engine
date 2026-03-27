import util
import pickle
from pathlib import Path


class Inverted_index:
    def __init__(self):
        self.index: dict[str, set[int]] = {}
        self.docmap: dict[int, dict] = {}

    def __add_document(self, doc_id, text):
        tokens = util.process_string(text)
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)

    def get_documents(self, token):
        ids = self.index.get(token.lower(), set())
        return sorted(ids)

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

    def load(self, cache_dir):
        cache_path = Path(cache_dir).expanduser()
        idx_path = cache_path / "index.pkl"
        if not idx_path.exists():
            raise FileNotFoundError(idx_path)
        docmap_path = cache_path / "docmap.pkl"
        if not docmap_path.exists():
            raise FileNotFoundError(docmap_path)

        with idx_path.open("rb") as fd:
            self.index = pickle.load(fd)

        with docmap_path.open("rb") as fd:
            self.docmap = pickle.load(fd)
