import textModels as tm
import DataWork as dw

class Card:
    def __init__(self) -> None:
        self.name = None
        self.typeLine = None
        self.textBody = None
        self.df = dw.DataWork()
    
    def generateCard(self):
        self.name = tm.BagOfWords('name', self.df).sample(2)
        self.typeLine = [tm.BagOfWords('super_type', self.df).sample(1), tm.BagOfWords('sub_type', self.df).sample(2)]
        self.textBody = tm.BagOfWords('oracle_text', self.df).sample(25)

    def printCard(self):
        print(self.name)
        print()
        print(self.typeLine[0] + ' - ' + self.typeLine[1])
        print()
        self._printNicely(self.textBody, 5)
    
    def _printNicely(self, input: str, wordsPerLine: int):
        ugh = input.split(' ')
        #print(ugh)
        i = 0
        while (i < len(input)/wordsPerLine):
            print(' '.join(ugh[i:i+wordsPerLine]))
            i += wordsPerLine