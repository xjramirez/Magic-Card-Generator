import numpy as np
from collections import defaultdict
import pandas as pd
from nltk import word_tokenize, sent_tokenize
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

    def sample(self, numOfWords=25) -> str:
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
        self.textTokenized = self._tokenize()
        self.probs = self._generateProbs()

    def _tokenize(self) -> list:
        tokens = []
        textList = list(self.df[self.textCategory].dropna().values)
        textListFiltered = [currText.replace('\n', ' \n ').lower() for currText in textList]
        #make every card end with CARDEND so that when it gets squished together we get
        # [CARDSTART <s> Whenever a b c d e . </s> <s> f g h i . </s> CARDEND CARDSTART <s> j k l m . </s> CARDEND] 
        for card in textListFiltered:
            card_tokens = ['CARDSTART']
            sentences = sent_tokenize(card)
            for sentence in sentences:
                sent_tokens = ['<s>']
                sent_tokens += word_tokenize(sentence)
                sent_tokens.append('</s>')
                card_tokens += sent_tokens
            card_tokens.append('CARDEND')
            tokens += card_tokens
        return tokens
    
    def _generateProbs(self):
        # create vocab of all possible words once
        vocabulary = set(self.textTokenized)
        vocabulary.discard('CARDSTART')
        # create a counts nested dictionary
        # making each outer key be a potential starting word
        # and each inner key a potential following word
        # default count (the value of the nested dict) 1 to create smoothing [edit: smoothing sucked]
        counts = defaultdict(lambda: defaultdict(int))
        #defaultdict(lambda: defaultdict(lambda: 0))
        #for context in vocabulary.union({'CARDSTART'}):
        #    for current in vocabulary:
        #        _ = counts[context][current]
        # start counting
        # for each word in the TOKENIZED TEXT
        # walk down the words and look with the one following it
        # increment the val in the dictionary where the outer key is the word
        # we're at, and the inner key is the word coming next
        # i.e. {context(/this word) : {current(/word that follows) : val(/no. times current comes after context in the corpus) += 1}}
        for context, current in zip(self.textTokenized, self.textTokenized[1:]):
            if current != 'CARDSTART':
                counts[context][current] += 1
        
        # now do some math
        # create the same-ish default dict
        probabilities = defaultdict(lambda: defaultdict(float))
        # iterate over the key-value pairs
        # for each possible starting word...
        for context, context_counts in counts.items():
            # do a little baby probability
            # total number of times words show up (AFTER A GIVEN CONTEXT WORD)
            context_total = sum(context_counts.values())
            # divide each time a word shows up (AFTER A GIVEN CONTEXT WORD) by the total number of times words show up (AAGCW)
            # save that value as the value to its word's key (IN THE SUPERDICT THAT IS AAGCW)
            probabilities[context] = {current: current_count / context_total for current, current_count in context_counts.items()}

        return probabilities


    def _conditionalSample(self, word):
        generated = np.random.choice(list(self.probs[word].keys()), p=list(self.probs[word].values()))
        return generated
    
    def sample(self, numOfWords=None):
        seq = ['CARDSTART']
        for i in range(0, numOfWords):
            if seq[i] == 'CARDEND':
                break
            else:
                seq.append(self._conditionalSample(seq[i]))
        result = ' '.join(seq)
        # TODO: figure out some regexes for this
        result = result.replace('<s>', '')
        result = result.replace('</s>', '')
        result = result.replace('CARDSTART', '')
        result = result.replace('CARDEND', '')
        result = result.replace(' }', '}')
        result = result.replace('{ ', '{')
        result = result.replace(' .', '.')
        result = result.replace(' ,', ',')
        result = result.replace(' n\'t', 'n\'t')
        return result
