import numpy as np
from converter.preprocess_ner import stanford_tree
from converter.preprocess_ner import structured_ne
import re
import json

def get_tags(conll):
    list_tags = []
    for tagged_sentence in conll:
        sentence, tags = zip(*tagged_sentence)
        list_tags.append(list(np.array(tags)))
    return list_tags

def get_structured(conll):
    structured = []
    for con in conll:
        structured.append(structured_ne(stanford_tree(con)))
    return structured

def get_tags_structured(structured_conll):
    list_tags = []
    for tagged_sentence in structured_conll:
        try:
            sentence, tags = zip(*tagged_sentence)
            list_tags.append(list(np.array(tags)))
        except:
            list_tags.append([])
    return list_tags

# Function to clean the BIO tag
def BIOCleaner(tag):
    tag = re.sub("B-","",tag)
    tag = re.sub("I-","",tag)
    return tag

# Function to get text list
def get_text_list(file_path):
    text_list = []
    with open(file_path, "r") as f:
        text_list = [json.loads(line).get("text") for line in f]
    return text_list