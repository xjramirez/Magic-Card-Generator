# import libraries

import pandas as pd

class DataWork:
    def __init__(self) -> None:
        # read from the json file. Has a shitton of files but hey it works

        card_df = pd.read_json(path_or_buf='oracle-cards-20231211100140.json', orient='records')


        # trim down dataframe to the most Important Features

        IF_df = card_df[['oracle_id', 'name', 'type_line', 'keywords', 'oracle_text']]

        IF_df.loc[:,['super_type']] = IF_df['type_line'].apply(lambda x: x.split('—', 1)[0] if '—' in x else x)
        IF_df.loc[:,['sub_type']] = IF_df['type_line'].apply(lambda x: x.split('—', 1)[1] if '—' in x else '')

        self.IF_df = IF_df[['oracle_id', 'name', 'super_type', 'sub_type', 'keywords', 'oracle_text']]