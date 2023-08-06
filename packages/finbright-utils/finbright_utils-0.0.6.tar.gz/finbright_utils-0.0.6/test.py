from finbright_utils.fin_statistics import correlation, resample
from finbright_utils.constants.interval import Interval
import pandas as pd
import yfinance as yf
import datetime 
import numpy as np

min1_data_aapl = yf.download("AAPL", start="2023-01-31", end="2023-02-01", interval = "1m")["Adj Close"]
min1_data_msf = yf.download("MSFT", start="2023-01-31", end="2023-02-01", interval = "1m")["Adj Close"]
corr = correlation(min1_data_aapl, min1_data_msf)
print(corr)
# min1_data.index = pd.to_datetime(min1_data.index)
# min1_data.drop(["Adj Close"], axis=1, inplace=True)
# min1_data.rename(columns={'Open': 'open',
#                 'High': 'high',
#                 'Low': 'low',
#                 'Close': 'close',
#                 'Volume': 'volume',
#                     },
#         inplace=True, errors='raise')
# min1_data["timestamp"] = min1_data.index
# min1_data.reset_index(drop=True, inplace=True)
# # min1_data.index = pd.to_datetime(min1_data.index)
# # print(min1_data["Datetime"])
# min1_data['timestamp'] = min1_data["timestamp"].values.astype(np.int64) // 10 ** 9

# day1_data = resample.resampling_based_on_time_frame(min1_data,  Interval.MIN1, Interval.MIN5)

# print(day1_data)