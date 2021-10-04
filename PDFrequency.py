import os
import json
from string import punctuation
from pdfminer.high_level import extract_text
from nltk.stem.cistem import Cistem

def get_pdf_file():
    script_dir = os.path.dirname(os.path.realpath('__file__'))
    input_path = os.path.join(script_dir, "Input")

    input_files = os.listdir(input_path)

    pdfs = [file for file in input_files if ".pdf" in file]
    wanted = os.path.join(input_path, pdfs[0])
    
    return wanted

def fix_characters(page):
    umlautDictionary = {u'Ä': 'Ae',
                    u'Ö': 'Oe',
                    u'Ü': 'Ue',
                    u'ä': 'ae',
                    u'ö': 'oe',
                    u'ü': 'ue',
                    u'ß': 'ss'}
    umlautDictionary = {ord(key):unicode(val) for key, val in umlautDictionary.items()}
    return page.translate(umlautDictionary)

filepath = get_pdf_file()
#with open('percy.txt', w) as file:

def get_all_words(page_text):
    all_words = page_text.split("\n")
    all_words = " ".join(all_words)
    all_words = all_words.split(" ")
    return all_words

def clean_quotes(word):
    quoteDict = {u'»': '\"',
                u'«': '\"'}
    word = word.translate(str.maketrans(quoteDict))
    return word

def clean_punctuation(word):
    PUNCTUATION = punctuation + "…"
    word = clean_quotes(word)
    word = word.translate(str.maketrans('', '', PUNCTUATION))
    return word.strip()

def clean_all_words(all_words):
    all_words = [clean_punctuation(word) for word in all_words if word]
    all_words = [word for word in all_words if word]
    return all_words

def all_stemmed_words(clean_words):
    stemmer = Cistem()
    all_stemmed_words = [stemmer.stem(word) for word in clean_words]
    return sorted(set(all_stemmed_words))

all_words = []
for page in range (30):
    if page > 6:
        page_text = extract_text(filepath, page_numbers=[page])
        all_words = all_words + get_all_words(page_text)
all_words = clean_all_words(all_words)
all_words = all_stemmed_words(all_words)
print(all_words)

