import pandas as pd

class DataWork:
    def __init__(self, colors: list=None, legalities: list=None, setName: str=None) -> None:
        """Class to contain and modify pandas.DataFrame objects spcifically containing data on MTG
        cards.
        Initialize DataWork object. Loads the data from the json of card data into a 
        pandas.DataFrame object. Cleans the data, then filters the card according to the arguments.

        Args:
            colors (list, optional): List of colors represented as strings of single uppercase letters
            (ex: ['G'], ['G', 'R']). Defaults to None.
            legalities (list, optional): List of ruleset legalities represented by strings
            (ex: ['Modern', 'Pauper']). Defaults to None.
            setName (str, optional): String that represents the set that a card is released in. Defaults to None.
        """
        # read from the json file. Has a shitton of files but hey it works
        self.card_df = pd.read_json(path_or_buf='oracle-cards-20231211100140.json', orient='records')
        self._cleanData()
        self._filterSampleCards(colors, legalities, setName)
    
    def _cleanData(self) -> None:
        """Modifies the DataFrame. Specifically:
        - changes the 'legalities' column to contain a list
        of strings instead of a dictionary representing which rulesets the card is legal in.
        """
        # turn the legalities column from dictionaries to lists
        legalArraySeries = self.card_df['legalities'].apply(lambda x: [ruleset for ruleset in x if x[ruleset] == 'legal'])
        self.card_df.loc[:,'legalities'] = legalArraySeries

    def getIFDF(self) -> pd.DataFrame:
        """Trims down the DataFrame to the important fields (IF), which are the fields that
        the language models will eventually train on.

        Returns:
            pd.DataFrame: The finalized DataFrame with a reduced number of fields.
        """
        # trim down dataframe to the most Important Features

        IF_df = self.card_df[['oracle_id', 'name', 'type_line', 'keywords', 'oracle_text']]

        IF_df.loc[:,['super_type']] = IF_df['type_line'].apply(lambda x: x.split('—', 1)[0] if '—' in x else x)
        IF_df.loc[:,['sub_type']] = IF_df['type_line'].apply(lambda x: x.split('—', 1)[1] if '—' in x else '')

        return IF_df[['oracle_id', 'name', 'super_type', 'sub_type', 'keywords', 'oracle_text']]
    
    def _filterSampleCards(self, colors: list=None, legalities: list=None, setName=None):
        """Filters the DataFrame to contain only rows that have the same conditions as specified
        by the arguments. Currently only filters by exactness with the specified arguments 
        (i.e. if you tell it for a green card, it will only give back a df with exactly green cards
        no green-red cards, no green-blue, only exactly green)

        Args:
            colors (list, optional): List of colors represented as strings of single uppercase letters
            (ex: ['G'], ['G', 'R']). Defaults to None.
            legalities (list, optional): List of ruleset legalities represented by strings
            (ex: ['Modern', 'Pauper']). Defaults to None.
            setName (str, optional): String that represents the set that a card is released in. Defaults to None.
        """
        if colors:
            # limit to the given colors
            # rn it only works for cards of the exact colors that you pass in
            # TODO: make this work for non-exact inclusion
            #   maybe try a lamda with .apply() that turns it into None/NaN if its not
            #   in it, then just remove all the .isna()s
            self.card_df = self.card_df[self.card_df['colors'].isin([colors])]
        if legalities:
            self.card_df = self.card_df[self.card_df['legalities'].isin([legalities])]
        if setName:
            self.card_df = self.card_df[self.card_df['set_name'] == setName]
        