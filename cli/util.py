import string
import json
from pathlib import Path
from nltk.stem import PorterStemmer


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


def load_documents(filename):
    path = "~/dev/rag-search-engine/data/" + filename
    path = Path(path).expanduser()
    with path.open() as fp:
        data = json.load(fp)
    return data
