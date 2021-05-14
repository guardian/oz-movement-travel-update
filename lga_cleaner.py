import pandas as pd 
import geopandas as gpd 
import os 

here = os.path.dirname(__file__)

pathos = f'{here}/goog_chloro/assets/lga2020.geojson'

gdf = gpd.read_file(pathos)

gdf["LGA_NAME20"] = gdf["LGA_NAME20"].str.replace(r"\(.*\)","")
gdf["LGA_NAME20"] = gdf["LGA_NAME20"].str.strip()

gdf.to_file(pathos, driver="GeoJSON")

print(gdf)