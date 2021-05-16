import pandas as pd
import os
import simplejson as json
from modules.yachtCharter import syncData
from modules.yachtCharter import yachtCharter

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"

listo = []

for file in os.listdir(f"{here}/data/ti_AUS_2020-01-01-2021-05-03-DAILY/"):
    name = file.split('_')
    # print(file[2])
    # print(name[2])
    init_df = pd.read_csv(f"{here}/data/ti_AUS_2020-01-01-2021-05-03-DAILY/{file}")
    init_df['City'] = name[2].title()
    # print(init_df.columns)
    listo.append(init_df)
    init_df['Smoothed congestion level'] = round(init_df['Average Congestion Level [%]'].rolling(7).mean(), 1)

df = pd.concat(listo)
# df = df[['Date', 'Average Congestion Level [%]', 'City']]

# pivoted = df.pivot(index="Date", columns=["City"])['Average Congestion Level [%]'].reset_index()
# pivoted.columns.name = None

# exclude = ["Newcastle", "Wollongong", 'Gold-Coast']
exclude = ["Wollongong"]
# print(df['City'].unique())
df = df[['Date', 'City', 'Smoothed congestion level']]



df.loc[df['City'] == 'Gold-Coast', 'City'] = "Gold Coast"

# print(df['Date'].unique())
# df = df.loc[~df['City'].isin(exclude)]

def makeDailyCountryChart(df):

	# lastUpdatedInt = df.date.iloc[-1]

	template = [
			{
				"title": "Road congestion has largely recovered",
				"subtitle": "Showing the 7 day rolling average of traffic congestion, where congestion is measured as as how much longer it takes to do a 30 minutes trip, based on Tom Tom location data",
				"footnote": "7 day rolling average of traffic congestion.",
				"source": " | Source: TomTom Traffic Index congestion level",
				"dateFormat": "%Y-%m-%d",
				"xAxisLabel": "",
				"yAxisLabel": "% extra time to complete 30 min trip",
				"timeInterval":"day",
				"tooltip":"<strong>Date: </strong>{{#nicedate}}Date{{/nicedate}}<br/><strong>Congestion: </strong>{{Smoothed congestion level}}",
				"periodDateFormat":"",
				"margin-left": "50",
				"margin-top": "5",
				"margin-bottom": "20",
				"margin-right": "25",
				"xAxisDateFormat": "%m/%Y"
			}
		]
	key = []
	periods = []
	labels = []
	chartId = [{"type":"smallmultiples"}]
	df.fillna('', inplace=True)
	chartData = df.to_dict('records')

	# yachtCharter(template=template, options=[{"chartType":"area"}], data=chartData, chartId=chartId, chartName="australia-road-traffic-by-city")
	yachtCharter(template=template, options=[{"chartType":"line"}], data=chartData, chartId=chartId, chartName="australia-road-traffic-by-city")




makeDailyCountryChart(df)


# pivoted = df.pivot(index="Date", columns=["City"])['Smoothed congestion level'].reset_index()
# pivoted.columns.name = None
# print(df)
# print(pivoted)

# def makeTestingLine(df):

#     template = [
#             {
#                 "title": "Road traffic has largely recovered",
#                 "subtitle": f"7 day rolling average of traffic congestion",
#                 "footnote": "",
#                 "source": "| TomTom Traffic Index congestion level",
#                 "dateFormat": "%Y-%m-%d",
#                 "yScaleType":"",
#                 "xAxisLabel": "Date",
#                 "yAxisLabel": "% extra time to complete 30 min trip",
#                 "minY": "0",
#                 "maxY": "",
#                 "x_axis_cross_y":"",
#                 "periodDateFormat":"",
#                 "margin-left": "50",
#                 "margin-top": "30",
#                 "margin-bottom": "20",
#                 "margin-right": "10"
#             }
#         ]
#     key = []
#     periods = []
#     labels = []
#     df.fillna("", inplace=True)
#     chartData = df.to_dict('records')
#     # labels = [{"x":f"{last_date}", "y":f"{middle_gap}", "offset":50,
#     # "text":f"Current gap is {numberFormat(latest_gap)}",
#     #  "align":"right", "direction":"right"}]

#     yachtCharter(template=template, labels=labels, data=chartData, chartId=[{"type":"linechart"}],
#     options=[{"colorScheme":"guardian", "lineLabelling":"TRUE"}], chartName="tomtom_traffic")

# # makeTestingLine(pivoted)
