import json
import string
from pathlib import Path

from nltk.stem import PorterStemmer

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


def process_string(s):
    path = DATA_DIR / "stopwords.txt"
    with path.open(encoding="utf-8") as fp:
        stopwords = fp.read().splitlines()

    s = s.lower()
    no_punct = s.translate(str.maketrans("", "", string.punctuation))
    tokens = [t for t in no_punct.split() if t not in stopwords]

    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    return tokens


def load_documents(filename):
    path = DATA_DIR / filename
    with path.open(encoding="utf-8") as fp:
        data = json.load(fp)
    return data
