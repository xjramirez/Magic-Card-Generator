# import libraries

import numpy as np
import string
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords

# read from the json file. Has a shitton of files but hey it works
card_df = pd.read_json(path_or_buf='oracle-cards-20231211100140.json', orient='records')

# This has tons of data we don't need for these purposes, so we'll remove... most of it
# 'language', 'layout', 
#card_df = card_df[['oracle_id', 'color_identity', 'colors', 'keywords', 'legalities', 'mana_cost', 'name', 'oracle_text', 'power', 'produced_mana', 'toughness', 'type_line']]
#print(card_df)

# actually im now realizing that I just want to split the dataframes up into certain related parts
# will keep the oracle_id to keep them all connected

text_df = card_df[['oracle_id', 'name', 'type_line', 'keywords', 'oracle_text']]
mana_df = card_df[['color_identity', 'colors', 'mana_cost', 'cmc', 'produced_mana', 'loyalty']]
meta_df = card_df[['legalities', 'layout', 'edhrec_rank', 'penny_rank', 'reserved', 'set_name']]

# Start creating BoW model
#text_tk_df = text_df
#text_tk_df['oracle_text'] = text_df['oracle_text'].dropna().apply(word_tokenize)
#text_tk_df
# 154 is apparently the average number of words per card
def generateBOW(textCategory='oracle_text', numberOfWords=154):

    # Turn all the text from one category (pandas column) into a string
    textList = list(text_df[textCategory].dropna().values)
    textListFiltered = [currText.replace('\n', ' ').lower() for currText in textList]
    #print(sum([len(line) for line in textListFiltered])/len(textListFiltered))
    textStr = ' '.join(textListFiltered)
    textTokenized = word_tokenize(textStr)

    # now have a list of every word in every card

    # create a set of all possible words
    possibleWords = list(set(textTokenized))
    totalWords = len(textTokenized)
    # initialize counts of words to be zero
    # then count all of them up
    # (to be used for probabilities)
    counts = {word : 0 for word in possibleWords}
    for word in textTokenized:
        counts[word] += 1
    
    # create probability dictionary where the key is a word
    # and the value is (# instances of the word) / (# all words)
    probs = {word : counts[word]/totalWords for word in possibleWords}
    
    generated = np.random.choice(list(probs.keys()), size=numberOfWords, p=list(probs.values()))
    result = ' '.join(generated)
    return result
# Idea: remove the name from each of them and replace it with the newly generated name for the generated card

def printNicely(input, wordsPerLine):
    ugh = input.split(' ')
    #print(ugh)
    i = 0
    while (i < len(input)/wordsPerLine):
        print(' '.join(ugh[i:i+wordsPerLine]))
        i += wordsPerLine

generatedName = generateBOW('name', 2)
generatedText = generateBOW('oracle_text', 50)
#test = "the text on this card reads word1 word2 word3 word4 blah blah enchant target creature until its owner pays 3 life (can only be paid as a sorcery) enchanted creature is stupid and silly"
printNicely(generatedName, 2)
printNicely(generatedText, 5)