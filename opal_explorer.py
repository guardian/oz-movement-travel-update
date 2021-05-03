import pandas as pd 
import os 

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"

# df = pd.read_csv(f"{data_path}opal_all_modes.csv",sep='\t', lineterminator='\r')

df = pd.read_excel(f"{data_path}opal_all_modes.xlsx")
print(df)
print(df.columns)

# print(f"{data_path}opal_all_modes.csv")