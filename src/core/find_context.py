import functools
import os
from typing import List

import nltk
from nltk.text import Text

src_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data")


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


def find_context(tokens: List[str], word: str, length: int, count: int) -> str:
    text_obj = Text(tokens)
    con_list = text_obj.concordance_list(word, width=length, lines=count)
    context_lines = "\n".join(
        [f"{i + 1}. {item.line.strip()}" for i, item in enumerate(con_list)]
    )
    return context_lines if context_lines else f"No occurrences of {word} found."
