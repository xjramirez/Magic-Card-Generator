import textModels as tm
import DataWork as dw

class Card:
    def __init__(self, colors=None, legalities=None, setName=None) -> None:
        self.name = None
        self.typeLine = None
        self.textBody = None
        df = dw.DataWork(colors, legalities, setName)
        self.df = df.getIFDF()
    
    def generateCard(self):
        self.name = tm.BagOfWords('name', self.df).sample(2)
        self.typeLine = [tm.BagOfWords('super_type', self.df).sample(1), tm.BagOfWords('sub_type', self.df).sample(2)]
        self.textBody = tm.BagOfWords('oracle_text', self.df).sample(25)

    def printCard(self):
        print('---------------------------------')
        print(self.name)
        print()
        print(self.typeLine[0] + ' - ' + self.typeLine[1])
        print()
        self._printNicely(self.textBody, 5)
        print('---------------------------------')
    
    def _printNicely(self, input: str, wordsPerLine: int):
        ugh = input.split(' ')
        #print(ugh)
        i = 0
        while (i < len(input)/wordsPerLine):
            print(' '.join(ugh[i:i+wordsPerLine]))
            i += wordsPerLine