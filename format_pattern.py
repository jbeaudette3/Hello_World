def format_pattern():
  # initial re-formatting from spreadsheet layout
  # into a list that this file can read.
  # ex: if next position is 'x', run script to update github
  #     if next position is '', do nothing
  
  import pandas as pd

  # read spreadsheet
  # Phrase: "HELLO WORLD"
  df = pd.read_csv('hello_world.csv')

  # Phrase: "HELLO"
  # df = pd.read_csv('hello.csv')

  # fill NaNs with blank
  df = df.fillna('')

  # get each value in each column and turn into a list
  # example:
  # number = position in list
  # value = how it appears in the spreadsheet 
  # 0 sun    3 X    6
  # 1 mon    4 X    7 X
  # 2 tue    5 X    8
  #
  working_list = []
  for c in df.columns:
    for val in df[c]:
      working_list.append(val)

  # cut out the first column: sun, mon, tue, etc.
  working_list = working_list[7:]

  # save values
  # simply exporting a list to a text file
  save_path = '/data/original_list.txt'
  with open(save_path, 'w') as f:
    json.dump(working_list, f)
