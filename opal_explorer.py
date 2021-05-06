import pandas as pd 
import os 
import datetime
from modules.yachtCharter import yachtCharter

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"

# df = pd.read_csv(f"{data_path}opal_all_modes.csv",sep='\t', lineterminator='\r')

df = pd.read_excel(f"{data_path}opal_all_modes.xlsx")


# print(f"{data_path}opal_all_modes.csv")

# long = pd.wide_to_long(df, stubnames, i, j)

df = df.T
df.columns = df.iloc[0]
df = df[1:].reset_index()
df = df.loc[df['index'] !="Unnamed: 58"]

df['index'] = pd.to_datetime(df['index'])
df['index'] = df['index'].dt.strftime('%Y-%m-%d')

df = df.loc[df['index']> '2019-06-01'].copy()

listo = ['Bus', 'Ferry', 'Light rail', 'Metro', 'Train', 'Grand Total']


for thing in listo:
    df[thing] = pd.to_numeric(df[thing])
    first_feb = df.loc[df['index'] == '2020-02-01']
    init_val = first_feb[thing].values[0]
    df[thing] = (df[thing]/init_val)*100
    # print(first_feb[thing])
    # maxer = df[thing].max()
    # print(maxer)
    # index = thing

# print(df.columns)

print(df)

def makeTestingLine(df):

    template = [
            {
                "title": "Sydney transport patronage",
                "subtitle": f"Indexed at 100 in February 2020",
                "footnote": "",
                "source": "| New South Wales transport",
                "dateFormat": "%Y-%m-%d",
                "yScaleType":"",
                "xAxisLabel": "Date",
                "yAxisLabel": "People",
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
    options=[{"colorScheme":"guardian", "lineLabelling":"TRUE"}], chartName="sydtransport_patronage_covid")

makeTestingLine(df)