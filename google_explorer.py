import pandas as pd 
import os 
import simplejson as json
from modules.yachtCharter import syncData

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"

df = pd.read_csv(f"{data_path}Oz_goog_Mobility_Report.csv")
# https://interactive.guim.co.uk/gis/lga-2020.json

# ['country_region_code', 'country_region', 'sub_region_1', 'sub_region_2',
#        'metro_area', 'iso_3166_2_code', 'census_fips_code', 'place_id', 'date',
#        'retail_and_recreation_percent_change_from_baseline',
#        'grocery_and_pharmacy_percent_change_from_baseline',
#        'parks_percent_change_from_baseline',
#        'transit_stations_percent_change_from_baseline',
#        'workplaces_percent_change_from_baseline',
#        'residential_percent_change_from_baseline']


# Changes for each day are compared to a baseline value for that day of the week:

#     The baseline is the median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.
#     The datasets show trends over several months with the most recent data representing approximately 2-3 days ago—this is how long it takes to produce the datasets.



## sub_region_2 are Local Government Areas

# print(df['sub_region_2'].unique())
latest = df['date'].max()

# print(latest)

latest = df.loc[df['date'] == latest]

# latest = latest[['date', 'sub_region_2', 'workplaces_percent_change_from_baseline']]

latest['date'] = pd.to_datetime(latest['date'])
latest['date'] = latest['date'].dt.strftime('%Y-%m-%d')
latest = latest.dropna(subset=['sub_region_2'])

# with open(f"{data_path}Oz_goog_latest.csv", "w") as f:
#     latest.to_csv(f, index=False, header=True)

# print(latest.columns)

latest = latest[['sub_region_2',
       'retail_and_recreation_percent_change_from_baseline',
       'grocery_and_pharmacy_percent_change_from_baseline',
       'parks_percent_change_from_baseline',
       'transit_stations_percent_change_from_baseline',
       'workplaces_percent_change_from_baseline',
       'residential_percent_change_from_baseline']]

latest.columns = ['sub_region_2',
       'retail_and_recreation',
       'grocery_and_pharmacy',
       'parks',
       'transit_stations',
       'workplaces',
       'residential']


latest['sub_region_2'] = latest['sub_region_2'].str.replace("Town of", '')
latest['sub_region_2'] = latest['sub_region_2'].str.replace("Shire of", '')
latest['sub_region_2'] = latest['sub_region_2'].str.replace("City of", '')
latest['sub_region_2'] = latest['sub_region_2'].str.replace("District Council of", '')
latest['sub_region_2'] = latest['sub_region_2'].str.replace("Regional", '')
latest['sub_region_2'] = latest['sub_region_2'].str.replace("Region", '')
latest['sub_region_2'] = latest['sub_region_2'].str.replace(" Rural", '')


latest['sub_region_2'] = latest['sub_region_2'].str.replace("The Council of the Municipality", '')
latest['sub_region_2'] = latest['sub_region_2'].str.replace("Municipal Council", '')
latest['sub_region_2'] = latest['sub_region_2'].str.replace("Municipality", '')
latest['sub_region_2'] = latest['sub_region_2'].str.replace("Council of", '')

latest['sub_region_2'] = latest['sub_region_2'].str.replace("City Council", '')
latest['sub_region_2'] = latest['sub_region_2'].str.replace("Shire Council", '')

latest['sub_region_2'] = latest['sub_region_2'].str.replace("City", '')
latest['sub_region_2'] = latest['sub_region_2'].str.replace("Shire", '')

latest['sub_region_2'] = latest['sub_region_2'].str.replace("Council", '')
latest['sub_region_2'] = latest['sub_region_2'].str.replace(" Of ", '')
latest['sub_region_2'] = latest['sub_region_2'].str.replace("the ", '')
latest['sub_region_2'] = latest['sub_region_2'].str.replace("The ", '')
latest['sub_region_2'] = latest['sub_region_2'].str.replace(" of ", '')

latest['sub_region_2'] = latest['sub_region_2'].str.replace("Corporation ", '')


latest['sub_region_2'] = latest['sub_region_2'].str.strip()


# Read in disaster map to get the LGA id's
import geopandas as gpd 
# dis = pd.read_csv(f"{data_path}Map_of_disasters.csv")
# lgas = gpd.read_file("https://interactive.guim.co.uk/gis/lga-2020.json")
lgas = pd.read_excel(f"{data_path}CG_LGA_2011_LGA_2016_Update.xls", sheet_name="Table 3", skiprows=5)
lgas = lgas[1:601]



from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 
def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=1):
    """
    :param df_1: the left table to join
    :param df_2: the right table to join
    :param key1: key column of the left table
    :param key2: key column of the right table
    :param threshold: how close the matches should be to return a match, based on Levenshtein distance
    :param limit: the amount of matches that will get returned, these are sorted high to low
    :return: dataframe with boths keys and matches
    """
    s = df_2[key2].tolist()
    
    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))    
    df_1['matches'] = m
    
    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2
    
    return df_1

latest_m = fuzzy_merge(latest, lgas, "sub_region_2", "LGA_NAME_2011", threshold=90, limit=1)

latest_m = pd.merge(latest_m, lgas, left_on="matches", right_on="LGA_NAME_2011", how="left")

latest_m = latest_m[['LGA_CODE_2011','sub_region_2', 'retail_and_recreation', 'grocery_and_pharmacy',
       'parks', 'transit_stations', 'workplaces', 'residential']]

latest_m = latest_m.drop_duplicates(subset='sub_region_2', keep='first')

with open(f"{data_path}Oz_goog_latest_2011lgas.csv", "w") as f:
    latest_m.to_csv(f, index=False, header=True)



# latest_m = fuzzy_merge(latest, dis, "sub_region_2", "name", threshold=90, limit=2)
# latest_m = pd.merge(latest_m, dis, left_on="matches", right_on="name", how="left")

# # latest_m = pd.merge(latest, dis, left_on="sub_region_2", right_on="name", how="left")

# latest_m = latest_m[['sub_region_2', 'retail_and_recreation', 'grocery_and_pharmacy',
#        'parks', 'transit_stations', 'workplaces', 'residential', 'id', 'name']]

# # print(latest_m.loc[latest_m['name'].isna()])
# # print(latest_m.columns)

# # print(latest)
# print(latest_m)




### FOLLOWING WAS ORIGINAL PIVOTED DATASET FOR D3 MAP

# melted = pd.melt(latest, id_vars=['sub_region_2'],
#  value_vars=['retail_and_recreation',
#        'grocery_and_pharmacy',
#        'parks',
#        'transit_stations',
#        'workplaces',
#        'residential'])

# melted['sub_region_2'] = melted['sub_region_2'].str.replace("Town of", '')
# melted['sub_region_2'] = melted['sub_region_2'].str.replace("Shire of", '')
# melted['sub_region_2'] = melted['sub_region_2'].str.replace("City of", '')
# melted['sub_region_2'] = melted['sub_region_2'].str.replace("District Council of", '')


# melted['sub_region_2'] = melted['sub_region_2'].str.replace("The Council of the Municipality", '')
# melted['sub_region_2'] = melted['sub_region_2'].str.replace("Municipal Council", '')
# melted['sub_region_2'] = melted['sub_region_2'].str.replace("Municipality", '')
# melted['sub_region_2'] = melted['sub_region_2'].str.replace("Council of", '')

# melted['sub_region_2'] = melted['sub_region_2'].str.replace("City Council", '')
# melted['sub_region_2'] = melted['sub_region_2'].str.replace("Shire Council", '')

# melted['sub_region_2'] = melted['sub_region_2'].str.replace("City", '')
# melted['sub_region_2'] = melted['sub_region_2'].str.replace("Shire", '')

# melted['sub_region_2'] = melted['sub_region_2'].str.replace("Council", '')
# melted['sub_region_2'] = melted['sub_region_2'].str.replace("Of", '')
# melted['sub_region_2'] = melted['sub_region_2'].str.replace("the", '')
# melted['sub_region_2'] = melted['sub_region_2'].str.replace("The", '')
# melted['sub_region_2'] = melted['sub_region_2'].str.replace("of", '')

# melted['sub_region_2'] = melted['sub_region_2'].str.strip()
# with open(f"{here}/goog_chloro/assets/Oz_goog_latest_melted.csv", "w") as f:
#     melted.to_csv(f, index=False, header=True)



# print(melted)