import MetaTrader5 as mt5

import pandas as pd
import numpy as np
import datetime as dt
import pytz

import mplfinance as mpf
import matplotlib.pyplot as plt

#Purpose: Collect forex data
#Input: Timeframe = 'H1', 'D1', 'W1'
#Output: Pandas Dataframe of OHLC data
def data_collection(timeframe, n):
	
	if not mt5.initialize():
		print('failed to connect')
		quit()

	timeframe_dict = {
                      'H1':mt5.TIMEFRAME_H1, 
					  'D1':mt5.TIMEFRAME_D1, 
					  'W1':mt5.TIMEFRAME_W1
					 }

	currs = ['EUR', 'GBP', 'AUD', 'NZD',
             'USD', 'CAD', 'CHF', 'JPY']

	ohlc_dict = {}

	for curr_no, curr1 in enumerate(currs):
		for curr2 in currs[curr_no+1:]:
			curr_pair = curr1 + curr2

			#Get candles from the past 3 weeks (exclusive of current week)
			time_now = pd.Timestamp.now(tz='Etc/UTC')
			#four_wks_ago = time_now - dt.timedelta(weeks=3)
			#day_of_wk = dt.timedelta(days=four_wks_ago.isoweekday()%7)
			#past_4_wks = dt.date(four_wks_ago.year, four_wks_ago.month, four_wks_ago.day) - day_of_wk

			#ohlc_arr = mt5.copy_rates_range(curr_pair, timeframe_dict[timeframe], 
			#	                            pd.to_datetime(past_4_wks), time_now)
			ohlc_arr = mt5.copy_rates_from(curr_pair, timeframe_dict[timeframe], 
				                           time_now, n)

			column_names = {
			                'open':'Open',
			                'high':'High',
			                'low':'Low',
			                'close':'Close'
						   }

			try:
				ohlc_df = pd.DataFrame(ohlc_arr)
				ohlc_df.index = pd.to_datetime(ohlc_df.iloc[:, 0], unit='s')
				ohlc_df = ohlc_df.drop(columns=['time'])
				ohlc_df = ohlc_df.rename(columns=column_names)

				ohlc_dict[curr_pair+'_ohlc_df'] = ohlc_df

			except:
				print('ERROR OCCURRED IN: ', curr_pair)

	mt5.shutdown()

	return ohlc_dict

#Purpose: Calculate percent change of the given dataframes of different currency pairs
#Input: Dictionary containing the dataframes of OHLC of different currency pairs
#Output: Tuple (1, 2) where 1 is a dictionary of OHLC dataframe of currency pairs
#					        2 is a dictionary of currency pairs with a difference of >= 8
def percent_change(all_ohlc_dict):
	currs = ['EUR', 'GBP', 'AUD', 'NZD',
             'USD', 'CAD', 'CHF', 'JPY']

	keys_list = all_ohlc_dict.keys()
	pc_change_dict = {}

	for key in keys_list:
		if not (key[0:3] in pc_change_dict):
			pc_change_dict[key[0:3]] = []
		
		if not (key[3:6] in pc_change_dict):
			pc_change_dict[key[3:6]] = []

		else:
			pass

		for curr in currs:
			if curr == key[0:3]:
				initial = all_ohlc_dict[key].iloc[0, 3]
				final = all_ohlc_dict[key].iloc[-1, 3]
				percent_change = (final - initial)*100/final
				pc_change_dict[key[0:3]].append(percent_change)

			if curr == key[3:6]:
				initial = all_ohlc_dict[key].iloc[0, 3]
				final = all_ohlc_dict[key].iloc[-1, 3]
				percent_change = -(final - initial)*100/final
				pc_change_dict[key[3:6]].append(percent_change)

	for curr in currs:
		pc_change_dict[curr] = np.array(pc_change_dict[curr]).sum()

	diffs_dict = {}

	for curr_no, curr1 in enumerate(currs):
		for curr2 in currs[curr_no+1:]:
			diff = abs((pc_change_dict[curr1]) - (pc_change_dict[curr2]))

			if diff >= 8:
				diffs_dict[curr1+curr2] = diff

	return (pc_change_dict, diffs_dict)