import pandas as pd 
import os 
import geopandas as gpd 
import matplotlib.pyplot as plt 

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"

df = pd.read_csv(f"{data_path}oz-fb-movement-2021-04-28.csv")

latest = df.loc[df['ds'] == df['ds'].max()]

# victoria = latest.loc[latest['polygon_id'].str.contains('AUS.10.')]

shp = gpd.read_file(f'{data_path}gadm36_AUS_shp/gadm36_AUS_2.shp')

merged = shp.merge(latest, left_on = 'GID_2', right_on="polygon_id", how="left")

# print(merged)

merged.plot(column='all_day_ratio_single_tile_users', legend=True)
plt.show()