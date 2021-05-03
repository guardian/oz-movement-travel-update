import pandas as pd 
import os 

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"

df = pd.read_csv(f"{data_path}oz-fb-movement-2021-04-28.csv")

latest = df.loc[df['ds'] == df['ds'].max()]

victoria = latest.loc[latest['polygon_id'].str.contains('AUS.10.')]

