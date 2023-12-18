import numpy as np
import string
import pandas as pd
from nltk import word_tokenize
from abc import ABC, abstractmethod

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
    def __init__(self, textCategory: str, df: pd.DataFrame) -> None:
        pass
    @abstractmethod
    def _tokenize(self):
        pass

    @abstractmethod
    def sample(self):
        pass


# consider including categorical distrubution superclass in order to
# make it possible to use it to generate which text fields will appear
class BagOfWords(TextModel):
    """Language Model to generate batches of text based
    upon each word's frequency in the corpus.

    Args:
        TextModel (_type_): _description_
    """

    def __init__(self, textCategory, df) -> None:
        """_summary_

        Args:
            textCategory (str): string corresponding to the
            features of the dataframe argument to be train 
            the model on
            df (pandas.DataFrame): dataframe with data from
            all cards
        """
        self.textCategory = textCategory
        self.df = df
        self.textTokenized = self._tokenize()
        self.probs = self._generateProbs()
    

    def _tokenize(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        # Turn all the text from one category (pandas column) into a string
        textList = list(self.df[self.textCategory].dropna().values)
        textListFiltered = [currText.replace('\n', ' ').lower() for currText in textList]
        #print(sum([len(line) for line in textListFiltered])/len(textListFiltered))
        textStr = ' '.join(textListFiltered)
        return word_tokenize(textStr)
    
    def _generateProbs(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
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
        """generate a string of n tokens, chosen with
        the tokens' individual frequency probability

        Args:
            numOfWords (int): number of tokens in the generated sample

        Returns:
            str: ' ' joined list of a specified number of possible tokens
        """
        generated = np.random.choice(list(self.probs.keys()), size=numOfWords, p=list(self.probs.values()))
        result = ' '.join(generated)
        return result
    
    
class BigramModel(TextModel):
    def __init__(self, textCategory: str, df: pd.DataFrame) -> None:
        self.textCategory = textCategory
        self.df = df

    
    def _tokenize(self):
        pass

    def sample(self):
        pass
    
