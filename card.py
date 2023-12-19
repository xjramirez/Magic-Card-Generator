import textModels as tm
import DataWork as dw

class Card:
    def __init__(self, colors=None, legalities=None, setName=None) -> None:
        self.name = None
        self.typeLine = None
        self.textBody = None
        
        df = dw.DataWork(colors, legalities, setName)
        self.df = df.getIFDF()

        self.nameModel = tm.BagOfWords('name', self.df)
        self.superTypeModel = tm.BagOfWords('super_type', self.df)
        self.subTypeModel = tm.BagOfWords('sub_type', self.df)
        self.textBodyModel = tm.BigramModel('oracle_text', self.df)
    
    def generateCard(self):
        self.name = self.nameModel.sample(2)
        self.typeLine = [self.superTypeModel.sample(1), self.subTypeModel.sample(2)]
        self.textBody = self.textBodyModel.sample(50)

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