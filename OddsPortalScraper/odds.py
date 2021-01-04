from packages import soccer_odds5 as gather_data
from packages import to_excel_functions as process_data
from packages import handling_errors as he
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium
import pandas as pd
import os
import sys
import sched, time

dirname = os.path.dirname(os.path.abspath(__file__))

print(dirname)

def main():
	odds_col_names = ['Nation of League', 'League', 'Date of Game', 
	                  'Date of Data Collection', 'Time of Scrape', 
	                  'Home Team', 'Away Team', 'Home Team Average Odds', 
	                  'Away Team Average Odds', 'Draw Odds']

	stds_col_names = ['Country of League', 'League', 
	                  'Date of Collection', 'Team', 
	                  'Standing']

	

	global browser

	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])

	chromeDriverDir = dirname + '/chromedriver.exe'

	browser = webdriver.Chrome(executable_path=chromeDriverDir, options=options)
	browser.get('https://www.oddsportal.com/soccer/')
	
	#Give the selector 45 seconds to locate the table before refreshing
	try:
		WebDriverWait(browser, 45).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table-main.sportcount')))

		link_to_leagues = gather_data.league_links_generator(browser)

		#Added because for some reason it always crashes due to unreferenced link_to_leagues
		#Put the program to restart in here instead of stopping
		try:
			print(link_to_leagues)

		except:
			print('Some Error Occurred')
			browser.close()
			he.restart_program()

	except:
		browser.refresh()
		time.sleep(30)
		link_to_leagues = gather_data.league_links_generator(browser)

	if he.check_internet(browser):
		print('No Internet Connection - Restarting Program')
		browser.close()
		he.restart_program()

	df1 = pd.DataFrame({col:[] for col in odds_col_names})
	df1.to_csv(os.path.join(dirname, 'output_files', 'LATESTodds.csv'), index=False)

	#Remove duplicates in the link_to_leagues list
	link_to_leagues = list(dict.fromkeys(link_to_leagues))

	count = 0

	for link in link_to_leagues:
		print(link)
		count += 1
		percent_extracted = (count/float(len(link_to_leagues)))*100

		odds_list = gather_data.data_for_LATESTodds(link, browser)
		#stds_list = gather_data.data_for_STANDINGSlatest(link, browser)

		if len(odds_list[0]) != 0:
			LATESTodds_df = process_data.odds_to_csv(dirname, odds_list)

		else:
			print('The page may not have loaded properly-No odds collected from: ', link)
		'''
		if len(stds_list[0]) != 0:
			if gather_data.check_presence_of_subleagues(stds_list):
				for stds_ith_list in stds_list:
					if len(stds_ith_list) != 0:
						STANDINGSlist_df = process_data.standings_to_csv(dirname, stds_ith_list)

					else:
						print('NO STANDINGS DATA COLLECTED FOR: ', link)
						break

			else:
				STANDINGSlist_df = process_data.standings_to_csv(dirname, stds_list)

		else:
			print('NO STANDINGS DATA COLLECTED FOR: ', link)
		'''
		print('Percent Extracted: %.2f' %percent_extracted)

	process_data.odds_to_archive_csv(dirname)
	#process_data.standings_to_archive_csv(dirname)
		
	print('Program Complete')
	browser.close()

while True:
	starttime = time.time()

	if __name__ == '__main__':
		try:
			main()
			try:
				rest_time = (600 - ((time.time() - starttime)))
				print('Resting for ', rest_time)
				time.sleep(rest_time)

			except:
				print('Resting Time is Exceeded')
				he.restart_program()

		except:
			try:
				print('Closing Browser')
				browser.close()
				he.restart_program()

			except:
				print('Browser is Already Closed')
				he.restart_program()