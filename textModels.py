import numpy as np
import string
import pandas as pd
from nltk import word_tokenize
from abc import ABC, abstractmethod

# categorical distribution will be used:
# -for now, to determine what words go on the card (in the bag of words model)
# -even in the future, to determine the text fields of the card
class CategoricalDistribution:
    pass

# each model will do the following things:
# -massage the input data (tokenize [some might want sentence end chars
# while some wont])
# build the model
# sample from the model
class TextModel(ABC):
    """Abstract Base Class for text models to make them conform to 
    process of taking from a dataframe, tokenizing, and sampling

    Args:
        ABC (_type_): _description_
    """    
    @abstractmethod
    def _tokenize(self):
        pass

    @abstractmethod
    def sample(self):
        pass



class BagOfWords(TextModel):

    def __init__(self, textCategory, df) -> None:
        self.textCategory = textCategory
        self.df = df.IF_df
        self.textTokenized = self._tokenize()
        self.probs = self._generateProbs()
    

    def _tokenize(self) -> str:
        # Turn all the text from one category (pandas column) into a string
        textList = list(self.df[self.textCategory].dropna().values)
        textListFiltered = [currText.replace('\n', ' ').lower() for currText in textList]
        #print(sum([len(line) for line in textListFiltered])/len(textListFiltered))
        textStr = ' '.join(textListFiltered)
        return word_tokenize(textStr)
    
    def _generateProbs(self) -> dict:
        # now have a list of every word in every card
        # create a set of all possible words
        possibleWords = list(set(self.textTokenized))
        totalWords = len(self.textTokenized)
        # initialize counts of words to be zero
        # then count all of them up
        # (to be used for probabilities)
        counts = {word : 0 for word in possibleWords}
        for word in self.textTokenized:
            counts[word] += 1
        
        # create probability dictionary where the key is a word
        # and the value is (# instances of the word) / (# all words)
        return {word : counts[word]/totalWords for word in possibleWords} 

    def sample(self, numOfWords) -> str:
        generated = np.random.choice(list(self.probs.keys()), size=numOfWords, p=list(self.probs.values()))
        result = ' '.join(generated)
        return result
    
    
    
    
