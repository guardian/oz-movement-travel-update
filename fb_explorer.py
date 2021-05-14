import pandas as pd 
import os 
import geopandas as gpd 
import matplotlib.pyplot as plt 

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"

df = pd.read_csv(f"{data_path}oz-fb-movement-2021-04-28.csv")
# https://s3.us-east-1.amazonaws.com/hdx-production-filestore/resources/435ed157-6f7a-4e8f-a63a-2aa177b9bd05/readme.txt?AWSAccessKeyId=AKIAXYC32WNARK756OUG&Expires=1620606531&Signature=U2z0K073afQBGPM7tAYCz9Lu3iM%3D

# print(df.columns)
# print(df['polygon_name'])

latest = df.loc[df['ds'] == df['ds'].max()].copy()

latest['all_day_bing_tiles_visited_relative_change'] = round(latest['all_day_bing_tiles_visited_relative_change'] * 100,1)
latest['all_day_ratio_single_tile_users'] = round(latest['all_day_ratio_single_tile_users'] * 100,1)


# # victoria = latest.loc[latest['polygon_id'].str.contains('AUS.10.')]

# shp = gpd.read_file(f'{data_path}gadm36_AUS_shp/gadm36_AUS_2.shp')

# merged = shp.merge(latest, left_on = 'GID_2', right_on="polygon_id", how="left")

# # print(merged)

# merged.plot(column='all_day_ratio_single_tile_users', legend=True)
# plt.show()

with open(f"{data_path}fb_latest.csv", "w") as f:
    latest.to_csv(f, index=False, header=True)

with open(f"{here}/chloropleth/assets/fb_latest.csv", "w") as f:
    latest.to_csv(f, index=False, header=True)