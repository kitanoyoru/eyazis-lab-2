import functools
import json
import os
import string

from typing import List

import nltk
from nltk.corpus import stopwords

import pymorphy2

src_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data")

metadata = {
    "NOUN": "существительное",
    "ADJF": "прилагательное",
    "ADJS": "прилагательное",
    "COMP": "компаратив",
    "VERB": "глагол", "INFN": "глагол",
    "PRTF": "причастие",
    "PRTS": "причастие",
    "GRND": "деепричастие",
    "NUMR": "числительное",
    "ADVB": "наречие",
    "NPRO": "местоимение-существительное",
    "PRED": "предикатив",
    "PREP": "предлог",
    "CONJ": "союз",
    "PRCL": "частица",
    "INTJ": "междометие",
    "nomn": "именительный",
    "gent": "родительный",
    "datv": "дательный",
    "accs": "винительный",
    "ablt": "творительный",
    "loct": "предложный",
    "sing": "единственное",
    "plur": "множественное",
    "masc": "мужской",
    "femn": "женский",
    "neut": "средний",
}


@functools.cache
def get_file_paths(root_folder: str = src_folder, extension: str = ".txt") -> List[str]:
    file_paths = []
    for root_dir, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root_dir, file)
                file_paths.append(file_path)

    return file_paths


def read_and_tokenize(files: List[str], language: str = "russian") -> List[str]:
    tokens = []
    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                tokens.extend(nltk.word_tokenize(text, language=language))
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")
    return tokens


if __name__ == "__main__":
    corpus = dict()
    morph = pymorphy2.MorphAnalyzer()
    stop_words = set(stopwords.words("russian")).union(set(string.punctuation))

    frequency = nltk.FreqDist(read_and_tokenize(get_file_paths()))

    for key, value in frequency.items():
        if key in stop_words:
            continue

        parse = morph.parse(key)[0]
        pos_tag = parse.tag.POS
        additional_info = metadata.get(pos_tag, "UNKNOWN")

        try:
            corpus[key] = {
                "frequency": value,
                "additional_information": additional_info,
            }
        except KeyError:
            continue

    with open("animals_corpus.json", "w+") as file:
        json.dump(corpus, file, indent=4, ensure_ascii=False)
