import pandas as pd

# read from the json file. Has a shitton of files but hey it works
card_df = pd.read_json(path_or_buf='oracle-cards-20231211100140.json', orient='records')
print(card_df)

# This has tons of data we don't need for these purposes, so we'll remove... most of it
# 'language', 'layout', 
#card_df = card_df[['oracle_id', 'color_identity', 'colors', 'keywords', 'legalities', 'mana_cost', 'name', 'oracle_text', 'power', 'produced_mana', 'toughness', 'type_line']]
#print(card_df)

# actually im now realizing that I just want to split the dataframes up into certain related parts
# will keep the oracle_id to keep them all connected

text_df = card_df[['oracle_id', 'name', 'type_line', 'keywords', 'oracle_text']]

mana_df = card_df[[]]
print(text_df)