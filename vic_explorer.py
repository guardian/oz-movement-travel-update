import pandas as pd 
import os 
import datetime
from modules.yachtCharter import yachtCharter

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"

df = pd.read_csv(f"{data_path}victransport.csv", names=['Category', 'Percentage', 'Month'])

df['Category'] = df['Category'].str.strip()

df['Percentage'] = df['Percentage'].str.replace("%", "")
df['Percentage'] = df['Percentage'].str.strip()

df['Percentage'] = pd.to_numeric(df['Percentage'])
# df['Percentage'] = df['Percentage']/100

df['Month'] = df['Month'].str.replace(r"\(.*\)","")
df['Month'] = df['Month'].str.strip()

df['Month'] = pd.to_datetime(df['Month'])

df = df.sort_values(by="Month", ascending=False)
df['Month'] = df['Month'].dt.strftime('%Y-%m-%d')

pivoted = df.pivot(index='Month', columns='Category')['Percentage'].reset_index()

# pivoted = pivoted[['Metro Train', 'Metropolitan bus', 'Regional train',
#        'Tram', 'Total network']]



print(pivoted)

def makeTestingLine(df):

    template = [
            {
                "title": "Victoria transport patronage",
                "subtitle": f"The network is seeing barely half as many patrons as pre Covid",
                "footnote": "",
                "source": "Victoria Transport",
                "dateFormat": "%Y-%m-%d",
                "yScaleType":"",
                "xAxisLabel": "Date",
                "yAxisLabel": "Percent of February 2020 levels",
                "minY": "0",
                "maxY": "",
                "x_axis_cross_y":"",
                "periodDateFormat":"",
                "margin-left": "50",
                "margin-top": "30",
                "margin-bottom": "20",
                "margin-right": "10"
            }
        ]
    key = []
    periods = []
    labels = []
    df.fillna("", inplace=True)
    chartData = df.to_dict('records')
    # labels = [{"x":f"{last_date}", "y":f"{middle_gap}", "offset":50,
    # "text":f"Current gap is {numberFormat(latest_gap)}",
    #  "align":"right", "direction":"right"}]

    yachtCharter(template=template, labels=labels, data=chartData, chartId=[{"type":"linechart"}],
    options=[{"colorScheme":"guardian", "lineLabelling":"FALSE"}], chartName="victransport_patronage_covid_line")

makeTestingLine(pivoted)

# def makeGroupedBar(df):
   
#     template = [
#             {
#                 "title": "Victoria Public Transport patronage as a % of February 2020",
#                 "subtitle": f"Public transport usage is not predicted to recover for years",
#                 "footnote": "",
#                 "source": "New South Wales Health COVID-19 weekly surveillance reports",
#                 "dateFormat": "%Y-%m-%d",
#                 "yScaleType":"",
#                 "xAxisLabel": "Month",
#                 "yAxisLabel": "Percentage",
#                 "minY": "",
#                 "maxY": "",
#                 "periodDateFormat":"",
#                 "margin-left": "100",
#                 "margin-top": "15",
#                 "margin-bottom": "20",
#                 "margin-right": "20",
#                 "breaks":"no"
#             }
#         ]
#     key = [{"key": "Metro Train", "colour":	"#c70000"},
#         {"key": "Metropolitan bus", "colour":	"#ed6300"},
#         {"key": "Regional train","colour": "#0084c6"},
#         {"key": "Tram","colour": "#0084c6"},
#         {"key": "Total network","colour": "#0084c6"}]
#     periods = []
#     labels = []
#     # chartId = [{"type":"linechart"}]
#     df.fillna('', inplace=True)
#     df = df.reset_index()
#     chartData = df.to_dict('records')
#     # print(since100.head())
#     # print(chartData)
#     yachtCharter(template=template, key=key, data=chartData, chartId=[{"type":"groupedbar"}], options=[{"enableShowMore":"1"}], chartName="victransport_patronage_covid")
    


# makeGroupedBar(pivoted)

# pivoted = pivoted.reset_index()
# with open(f"{data_path}overseas_source_grouped_bar.csv", "w") as f:
#     pivoted.to_csv(f, index=False, header=True)