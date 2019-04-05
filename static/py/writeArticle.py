import os
import re
import pandas as pd
from datetime import datetime
import  numpy as np
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
import random
# nltk.download('all') # only run first time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #points to static folder

def writeEssay():
    w_dictionary = {'different':['distinct', 'different'], 'dictate':['determine', 'define', 'dictate', ]\
                    , 'however':['yet', 'though', 'however'], 'serious':['fatal', 'serious', 'acute', 'deadly']\
                    , 'diseases':['illnesses', 'disorders', 'ailments', 'conditions'], 'in which':[ 'where', '. Here']}
    for i in range(1,42):
        para1_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para"+str(i)+".csv")
        essay_text = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\article.txt")
        df = pd.read_csv(para1_name)
        df_random = df.sample(len(df.index))
        column_names = list(df_random)
        df_random.fillna("na", inplace=True)
        article_list = df_random.values.tolist()
        article_list = [i for article in article_list for i in article if i != "na"]
        similarity_dict = {article_list.index(i):sentence_similarity(i\
                    , article_list[article_list.index(i)+1]) for i in article_list}
        text_file = open(essay_text, "a")
        text_file.write("\n\nParagraph"+str(i)+"\n")
        for i in article_list:
            for wrd, syn in w_dictionary.items():
                if wrd in i:
                    print(random.choice(syn))
                    i.replace(wrd, random.choice(syn))
            text_file.write("%s. " % i)
def detectFlow():
    '''find all the words in first line of the para, then slect subsequent lines
       based on the similr words frequency- read ntlk docs'''
    pass
def breakAtIsAndReverse():
    '''if there is an 'is' in the middle of a sentence it usaully can be reversed without
        changing the original meaning'''
    pass
def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith("N"):
        return 'n'
    if tag.startswith('V'):
        return 'v'
    if tag.startswith('J'):
        return 'j'
    if tag.startswith("R"):
        return 'r'
    return None
def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None

    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None

def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))

    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]

    score, count = 0.0, 0

    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        best_score = max([synset.path_similarity(ss) for ss in synsets2])

        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1

    # Average the values
    score /= count
    return score

# sentences = [
#     "Dogs are awesome.",
#     "Some gorgeous creatures are felines.",
#     "Dolphins are swimming mammals.",
#     "Cats are beautiful animals.",
# ]
#
# focus_sentence = "Cats are beautiful animals."
#
# for sentence in sentences:
#     print "Similarity(\"%s\", \"%s\") = %s" % (focus_sentence, sentence, sentence_similarity(focus_sentence, sentence))
#     print "Similarity(\"%s\", \"%s\") = %s" % (sentence, focus_sentence, sentence_similarity(sentence, focus_sentence))
#     print

# Similarity("Cats are beautiful animals.", "Dogs are awesome.") = 0.511111111111
# Similarity("Dogs are awesome.", "Cats are beautiful animals.") = 0.666666666667

# Similarity("Cats are beautiful animals.", "Some gorgeous creatures are felines.") = 0.833333333333
# Similarity("Some gorgeous creatures are felines.", "Cats are beautiful animals.") = 0.833333333333

# Similarity("Cats are beautiful animals.", "Dolphins are swimming mammals.") = 0.483333333333
# Similarity("Dolphins are swimming mammals.", "Cats are beautiful animals.") = 0.4

# Similarity("Cats are beautiful animals.", "Cats are beautiful animals.") = 1.0
# Similarity("Cats are beautiful animals.", "Cats are beautiful animals.") = 1.0

writeEssay()
