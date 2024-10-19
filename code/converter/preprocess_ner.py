# Import library
from nltk.tree import Tree
from nltk import pos_tag
import nltk
from nltk.chunk import conlltags2tree
from itertools import groupby

# Function to create tree from the tagged sentence       
def stanford_tree(tagged_sentence):
    tokens, ne_tags = zip(*tagged_sentence)
    pos_tags = [pos for token, pos in pos_tag(tokens)]
    conlltags = [(token, pos, ne) for token, pos, ne in zip(tokens, pos_tags, ne_tags)]
    ne_tree = conlltags2tree(conlltags)
    return ne_tree

# Function to parse named entities from tree
def structured_ne(ne_tree):
    ne = []
    for subtree in ne_tree:
        if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
            ne_label = subtree.label()
            ne_string = " ".join([token for token, pos in subtree.leaves()])
            ne.append((ne_string, ne_label))
    return ne

# Function to check if all collected information in the container is the same
def all_equal(container):
    g = groupby(container)
    return next(g, True) and not next(g, False)

# Function to listing unique element that need to be keeped
def to_keep(container):
    container = list(set(container))
    for i, el in enumerate(reversed(container)):
        for k, el2 in enumerate(container):
            if el != el2 and el in el2:
                try:
                    container.remove(el)
                except:
                    pass
    return container

# Function to clean element that a subset of the other element in the container
def clean_subset(container):
    if len(container) != 0:
        container_keep = to_keep(container)
        new_container = [x for x in container if x in container_keep]
        container = new_container
        if all_equal(container) == True:
            container = [container[0]]
        container = list(dict.fromkeys(container))
    return container