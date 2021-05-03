import pandas as pd 
import os 

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

print(df)
print(df.columns)



latest = df['date'].max()

print(latest)
