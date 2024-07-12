import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas_datareader.data as web
import pandas as pd

style.use('ggplot')

start = dt.datetime(2020,1,1)
end = dt.datetime(2021,1,1)


# df.to_csv('tsla.csv')
# df = web.DataReader('TSLA', 'stooq', start, end)

# df.to_csv('tsla.csv')

df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
df.plot()
plt.show()
# print(df.head())

