import pandas as pd 
import os 
import simplejson as json
from modules.yachtCharter import syncData

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"

df = pd.read_csv(f"{data_path}Oz_goog_Mobility_Report.csv")

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

latest = latest[['date', 'sub_region_2', 'workplaces_percent_change_from_baseline']]

latest['date'] = pd.to_datetime(latest['date'])
latest['date'] = latest['date'].dt.strftime('%Y-%m-%d')
latest = latest.to_dict('records')

finalJson = json.dumps(latest, indent=4)

# print(finalJson)

syncData(finalJson,"oz-google-workplace-change")

# with open(f"{data_path}Oz_goog_workplace_change.csv", "w") as f:
#     latest.to_csv(f, index=False, header=True)

