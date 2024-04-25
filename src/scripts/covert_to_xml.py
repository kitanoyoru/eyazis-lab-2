import logging
import os
import string
import xml.dom.minidom
import xml.etree.ElementTree as ET

import pymorphy2
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

metadata = {
    "NOUN": "существительное",
    "ADJF": "прилагательное",
    "ADJS": "прилагательное",
    "COMP": "компаратив",
    "VERB": "глагол",
    "INFN": "глагол",
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


def text_to_xml(text: str, root_name: str) -> str:
    morph = pymorphy2.MorphAnalyzer()

    root = ET.Element(root_name)

    sentences = sent_tokenize(text)

    stop_words = set(stopwords.words("russian")).union(string.punctuation)

    sentence_counter = 0
    for sentence in sentences:
        if len(sentence) == 0:
            continue

        sentence_element = ET.SubElement(root, "sentence", id=str(sentence_counter + 1))
        words = word_tokenize(sentence)

        words_counter = 0
        for word in words:
            if word not in stop_words:
                try:
                    parse = morph.parse(word)[0]
                    pos_tag = parse.tag.POS
                    metadata_info = metadata.get(pos_tag, "UNKNOWN")
                    word_element = ET.SubElement(
                        sentence_element,
                        "word",
                        id=str(words_counter + 1),
                        info=metadata_info,
                    )
                    word_element.text = word
                    words_counter += 1
                except KeyError as e:
                    logging.warning(f"Key error: {e} for word: {word}")
            else:
                logging.debug(f"Skipping stopword/punctuation: {word}")

        if words_counter == 0:
            root.remove(sentence_element)
        else:
            sentence_counter += 1

    xml_str = ET.tostring(root, encoding="utf-8")
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml_str = dom.toprettyxml(indent="  ")

    return pretty_xml_str


if __name__ == "__main__":
    src_folder = os.path.join(CURRENT_DIR, "..", "data")
    dst_folder = os.path.join(CURRENT_DIR, "..", "parsed_data")

    os.makedirs(dst_folder, exist_ok=True)
    logging.info("Starting processing files...")

    for root_dir, dirs, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root_dir, file)
                logging.info(f"Processing {file_path}")

                with open(file_path, "r") as f:
                    text = f.read()

                xml_text = text_to_xml(text, root_name="document")
                new_dir = root_dir.replace(src_folder, dst_folder)

                os.makedirs(new_dir, exist_ok=True)

                new_file = os.path.join(new_dir, file.replace(".txt", ".xml"))
                logging.info(f"Saving XML to {new_file}")

                with open(new_file, "w") as f:
                    f.write(xml_text)

    logging.info("Processing completed.")
