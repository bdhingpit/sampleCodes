import pandas as pd
import os.path
import os

odds_col_names = ['Nation of League', 'League', 'Date of Game', 
                  'Date of Data Collection', 'Time of Scrape', 
                  'Home Team', 'Away Team', 'Home Team Average Odds', 
                  'Away Team Average Odds', 'Draw Odds']

stds_col_names = ['Country of League', 'League', 
                  'Date of Collection', 'Team', 
                  'Standing']
#
def reformat_csv_files(df):
	try:
		switches = df['League'].ne(df['League'].shift(-1))
		idx = switches[switches].index
		df_new = pd.DataFrame(index=idx + 0.5)
		df_upd = pd.concat([df, df_new]).sort_index()

	except:
		print('Error in Reformating')

	return df_upd

#Generate blank csv files for LATESTodds and STANDINGSlist
def recreate_new_csv(path):
	df1 = pd.DataFrame({col:[] for col in odds_col_names})
	df1.to_csv(os.path.join(path, 'output_files', 'LATESTodds.csv'), index=False)

	df2 = pd.DataFrame({col:[] for col in stds_col_names})
	df2.to_csv(os.path.join(path, 'output_files', 'STANDINGSlist.csv'), index=False)

#Append the extracted data to the blank LATESTodds csv; Returns a DataFrame object
def odds_to_csv(path, odds_list):
	odds_dict = {}
	
	for col, data in zip(odds_col_names, odds_list):
		odds_dict[col] = data

	odds_df = pd.DataFrame(odds_dict)
	odds_df_upd = reformat_csv_files(odds_df)

	odds_df_upd.to_csv(os.path.join(path, 'output_files', 'LATESTodds.csv'), 
					mode='a', header=False, columns=odds_col_names, index=False)

	return pd.read_csv(os.path.join(path, 'output_files', 'LATESTodds.csv'), usecols=odds_col_names)

#Append the extracted data to the blank STANDINGSlists csv; Returns a DataFrame object
def standings_to_csv(path, std_list):
	stds_dict = {}

	for col, data in zip(stds_col_names, std_list):
		stds_dict[col] = data

	stds_df = pd.DataFrame(stds_dict)
	stds_df_upd = reformat_csv_files(stds_df)

	stds_df_upd.to_csv(os.path.join(path, 'output_files', 'STANDINGSlist.csv'), 
					mode='a', header=False, columns=stds_col_names, index=False)

	return pd.read_csv(os.path.join(path, 'output_files', 'STANDINGSlist.csv'), usecols=stds_col_names)

#Create a file for archiving odds if non-existing and append if the file is existing; Also removes duplicates
#Time basis for naming is GMT 0', 'UTC 0
def odds_to_archive_csv(path):
	date_today = str(pd.to_datetime('now').strftime('%d-%m-%Y'))[0:10]

	if os.path.exists(os.path.join(path, 'output_files', 'odds_archive', 'odds_archive_{}.csv').format(date_today)):
		odds_latest_df = pd.read_csv(os.path.join(path, 'output_files', 'LATESTodds.csv')).dropna(axis=0, how='all').reset_index(drop=True)
		odds_arch_df = pd.read_csv(os.path.join(path, 'output_files', 'odds_archive', 'odds_archive_{}.csv').format(date_today))

		odds_arch_upd = odds_arch_df.dropna(axis=0, how='all').reset_index(drop=True)
		#odds_arch_upd_app = odds_arch_upd.append(odds_latest_df, ignore_index=True).drop_duplicates(keep='first').reset_index(drop=True)
		odds_arch_upd_app = odds_arch_upd.append(odds_latest_df, ignore_index=True).reset_index(drop=True)

		final_arch_odds = reformat_csv_files(odds_arch_upd_app)

		final_arch_odds.to_csv(os.path.join(path, 'output_files', 'odds_archive', 'odds_archive_{}.csv')
				.format(date_today), index=False, mode='w', header=odds_col_names)

	else:
		odds_latest_df = pd.read_csv(os.path.join(path, 'output_files', 'LATESTodds.csv'))

		odds_upd = reformat_csv_files(odds_latest_df.dropna(axis=0, how='all').reset_index(drop=True))

		odds_upd.to_csv(os.path.join(path, 'output_files', 'odds_archive', 'odds_archive_{}.csv')
						.format(date_today), mode='w', header=odds_col_names, index=False)
																										
#Create a file for archiving standings if non-existing and append if the file is existing; Also removes duplicates
#Time basis for naming is GMT 0/UTC 0
def standings_to_archive_csv(path):
	date_today = str(pd.to_datetime('now').strftime('%d-%m-%Y'))[0:10]

	if os.path.exists(os.path.join(path, 'output_files', 'standings_archive', 'standings_archive_{}.csv').format(date_today)):
		stds_latest_df = pd.read_csv(os.path.join(path, 'output_files', 'STANDINGSlist.csv')).dropna(axis=0, how='all').reset_index(drop=True)
		stds_arch_df = pd.read_csv(os.path.join(path, 'output_files', 'standings_archive', 'standings_archive_{}.csv').format(date_today))

		stds_arch_upd = stds_arch_df.dropna(axis=0, how='all').reset_index(drop=True)
		#stds_arch_upd_app = stds_arch_upd.append(stds_latest_df, ignore_index=True).reset_index(drop=True).drop_duplicates(keep='first').reset_index(drop=True)
		stds_arch_upd_app = stds_arch_upd.append(stds_latest_df, ignore_index=True).reset_index(drop=True)

		final_arch_stds = reformat_csv_files(stds_arch_upd_app)

		final_arch_stds.to_csv(os.path.join(path, 'output_files', 'standings_archive', 'standings_archive_{}.csv')
				.format(date_today), index=False, mode='w', header=stds_col_names)

	else:
		stds_latest_df = pd.read_csv(os.path.join(path, 'output_files', 'STANDINGSlist.csv'))

		stds_upd = reformat_csv_files(stds_latest_df.dropna(axis=0, how='all').reset_index(drop=True))

		stds_upd.to_csv(os.path.join(path, 'output_files', 'standings_archive', 'standings_archive_{}.csv')
		          .format(date_today), mode='a', header=stds_col_names, index=False)

#Create a copy of the file that can be accessed
def create_copy_of_csv(path, df1, df2):
	try:
		df1.to_csv(os.path.join(path, 'output_files', 'copies', 'LATESTodds_copy.csv'), 
			header=odds_col_names, index=False)

		df2.to_csv(os.path.join(path, 'output_files', 'copies', 'STANDINGSlist_copy.csv'), 
			header=stds_col_names, index=False)

	except:
		print('FILES ARE CURRENTLY OPEN')