import pandas as pd 
import os 
import datetime
import geopandas as gpd 

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"



## Facebook

gadm = gpd.read_file(f"{data_path}gadm36_AUS_shp/gadm36_AUS_2.shp")
# print(gadm['GID_2'])
# print(gadm.columns)
fb = pd.read_csv(f"{data_path}oz-fb-movement-2021-04-28.csv")

fbm = pd.merge(fb, gadm, left_on="polygon_id", right_on="GID_2", how="left")
fbm = fbm[['ds', 'country','polygon_name',
       'all_day_bing_tiles_visited_relative_change',
       'all_day_ratio_single_tile_users', 'baseline_name','NAME_1', 'NL_NAME_1', 'GID_2', 'NAME_2']]

# https://s3.us-east-1.amazonaws.com/hdx-production-filestore/resources/435ed157-6f7a-4e8f-a63a-2aa177b9bd05/readme.txt?AWSAccessKeyId=AKIAXYC32WNARK756OUG&Expires=1620606531&Signature=U2z0K073afQBGPM7tAYCz9Lu3iM%3D


latest = fbm.loc[fbm['ds'] == fbm['ds'].max()].copy()

latest['all_day_bing_tiles_visited_relative_change'] = round(latest['all_day_bing_tiles_visited_relative_change'] * 100,1)
latest['all_day_ratio_single_tile_users'] = round(latest['all_day_ratio_single_tile_users'] * 100,1)

grouped = latest.groupby(by=["NAME_1"])["all_day_bing_tiles_visited_relative_change", "all_day_ratio_single_tile_users"].mean()
print(grouped)


# print(latest.loc[latest['all_day_bing_tiles_visited_relative_change'] == latest['all_day_bing_tiles_visited_relative_change'].max()])
# print(latest.loc[latest['all_day_bing_tiles_visited_relative_change'] == latest['all_day_bing_tiles_visited_relative_change'].min()])

# ### TOMTOM
# tom_listo = []
# for file in os.listdir(f"{here}/data/ti_AUS_2020-01-01-2021-05-03-DAILY/"):
#     name = file.split('_')
#     # print(file[2])
#     # print(name[2])
#     init_df = pd.read_csv(f"{here}/data/ti_AUS_2020-01-01-2021-05-03-DAILY/{file}")
#     init_df['City'] = name[2].title()
#     # print(init_df.columns)
#     tom_listo.append(init_df)
#     init_df['Smoothed congestion level'] = round(init_df['Average Congestion Level [%]'].rolling(7).mean(), 1)

# tomtom = pd.concat(tom_listo)

# print(tomtom)


# ### NSW TRANSPORT


# nsw = pd.read_excel(f"{data_path}opal_all_modes.xlsx")

# nsw = nsw.T
# nsw.columns = nsw.iloc[0]
# nsw = nsw[1:].reset_index()
# nsw = nsw.loc[nsw['index'] !="Unnamed: 58"]

# nsw['index'] = pd.to_datetime(nsw['index'])
# nsw['index'] = nsw['index'].dt.strftime('%Y-%m-%d')

# nsw = nsw.loc[nsw['index']> '2019-06-01'].copy()

# nsw_listo = ['Bus', 'Ferry', 'Light rail', 'Metro', 'Train', 'Grand Total']

# print(nsw)
# # for thing in nsw_listo:
# #     nsw[thing] = pd.to_numeric(nsw[thing])
# #     first_feb = nsw.loc[nsw['index'] == '2020-02-01']
# #     init_val = first_feb[thing].values[0]
# #     nsw[thing] = (nsw[thing]/init_val)*100

# # print(nsw)