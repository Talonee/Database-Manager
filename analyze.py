from datetime import datetime
import pandas as pd

def stat_values():
    pass

def graph():
    pass

def convert_date():
    df = pd.read_csv("Output/Copy of 2013 DATA - ENCODED.csv")
    # print(type(df["Date"][1]))
    # for i in df["Date"]:
    #     df["Date"][i] = datetime.strptime(i, "%Y-%m-%d")
    # print(type(df["Date"][1]))

    d = {'model': 'ep', 
     'date': ('2017-02-02', '2017-02-04', '2017-03-01')}
    df1 = pd.DataFrame(d)

    d = {'model': 'rs',
        'date': ('2017-01-12', '2017-01-04', '2017-05-01')}
    df2 = pd.DataFrame(d)

    df = pd.concat([df1, df2])

    # Create a column containing the month
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')

    # Get the start and end months
    months = df['month'].sort_values()
    start_month = months.iloc[0]
    end_month = months.iloc[-1]

    index = pd.PeriodIndex(start=start_month, end=end_month)

    df.groupby('month')['model'].count().reindex(index).plot.bar()

if __name__ == "__main__":
    convert_date()
    # print(datetime.strptime("2013-01-16", "%Y-%m-%d"))