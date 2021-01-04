from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time

from packages.sub_packages import handling_errors as he

#Generate a list for dates of games
def generate_game_dates(soup):
	xeid_counter = soup.select('tr.center.nob-border, tr[xeid]')

	count = 0
	count_list = []

	for i in xeid_counter:
		if 'xeid' in str(i):
			count += 1

		else:
			count_list.append(count)
			count = 0

	count_list.append(count)

	dates = soup.select('tr.center.nob-border span.datet')

	dates_list = []

	for date, i in zip(dates, count_list[1:]):
		for j in range(i):
			dates_list.append(date.get_text())

	dates_upd = []

	for date in dates_list:
		if 'Tomorrow' in date:
			dates_upd.append(str(pd.to_datetime('now')+pd.DateOffset(1))[0:10])

		elif 'Today' in date:
			dates_upd.append(str(pd.to_datetime('now'))[0:10])

		else:
			dates_upd.append(str(pd.to_datetime(date))[0:10])

	return dates_upd

#Generate a LIST of links towards each league
def league_links_generator(browser):
	main_page_url = 'https://www.oddsportal.com/soccer/'
	domain = 'https://www.oddsportal.com'

	browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
	browser.get(main_page_url)

	#Give the selector 45 seconds to locate the table before refreshing
	try:
		WebDriverWait(browser, 45).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table-main.sportcount')))

	except:
		browser.refresh()
		time.sleep(30)

	if he.check_page_blank(browser, WebDriverWait(browser, 45).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 
            'table.table-main.sportcount')))):
		print('Error in Loading Page - Restarting Program')
		browser.close()
		he.restart_program()

	page_html = browser.page_source  #If the table did not exist initally, but did after refresh, get new page source
	soup = BeautifulSoup(page_html, 'html.parser')

	league_links = [domain+link.get('href') for link in 
	                soup.select('table.table-main a[foo="f"]')]

	browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

	return league_links

#Generate a LIST of lists of the needed data for LATESTodds;
#LIST generated will be used to generate the DataFrame later
def data_for_LATESTodds(link, browser):
	browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')

	browser.get(link)

	#Give the selector 45 seconds to locate the table before refreshing
	try:
		WebDriverWait(browser, 45).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table#tournamentTable.table-main')))

	except:
		browser.refresh()
		time.sleep(30)
		
	if he.check_internet(browser):
		print('No Internet Connection - Restarting Program')
		browser.close()
		he.restart_program()

	try:
		WebDriverWait(browser, 45).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table#tournamentTable.table-main')))

	except:
		return [[]]

	'''
	if he.check_page_blank(browser, WebDriverWait(browser, 45).until(
        	EC.presence_of_element_located((By.CSS_SELECTOR, 
        	'table#tournamentTable.table-main')))):
		print('NO DATA AVAILABLE or PAGE DID NOT LOAD CORRECTLY')
		return [[]]'''

	page_html = browser.page_source
	soup = BeautifulSoup(page_html, 'html.parser')

	odds = soup.select('table#tournamentTable.table-main tr[xeid] > td[xodd] > a')
	odds_list = [i.get_text() for i in odds]

	home_odds_list = odds_list[0::3]
	draw_odds_list = odds_list[1::3]
	away_odds_list = odds_list[2::3]

	home_away_teams = soup.select('table#tournamentTable.table-main tr[xeid] > td.name.table-participant > a[href*="/soccer"]')
	home_team_list = []
	away_team_list = []

	#Used a try and except due to possible error if game is live
	for i in home_away_teams:
		try:
			home_team_list.append(i.get_text().split(' - ')[0])
			away_team_list.append(i.get_text().split(' - ')[1])

		except:
			pass

	home_team_list = [i for i in home_team_list if i != '']

	nation = soup.select('a.bfl:nth-child(3)')	
	nation_list = [nation[0].get_text()[1:] for i in range(len(home_odds_list))]

	league = soup.select('tr.dark > th:nth-child(1) > a:nth-child(5)') 
	league_list = [league[0].get_text() for i in range(len(home_odds_list))]

	dos_list = [str(pd.to_datetime('now'))[0:10] for i in range(len(home_odds_list))]   #dos = Tate Of Scrape
	tos_list = [str(pd.to_datetime('now'))[11:16] for i in range(len(home_odds_list))]  #tos = time of scrape

	date_of_games = generate_game_dates(soup)

	complete_odds_list = [nation_list, league_list,
	                      date_of_games, dos_list,
	                      tos_list, home_team_list, 
	                      away_team_list, home_odds_list,
	                      away_odds_list, draw_odds_list]

	browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

	return complete_odds_list

#Generate a LIST of lists of the needed data for STANDINGSlist;
#LIST generated will be used to generate the DataFrame later														
def data_for_STANDINGSlatest(link, browser):
	link = link + '/standings/'

	browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')

	browser.get(link)
	
	#Give the selector 45 seconds to locate the table before refreshing
	try:
		WebDriverWait(browser, 45).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div#glib-stats-data.glib-stats-data')))

	except:
		browser.refresh()
		time.sleep(30)
		
	if he.check_internet(browser):
		print('No Internet Connection - Restarting Program')
		browser.close()
		he.restart_program()

	try:
		WebDriverWait(browser, 45).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div#glib-stats-data.glib-stats-data')))

	except:
		return [[]]

	'''
	if he.check_page_blank(browser, WebDriverWait(browser, 45).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 
        	'div#glib-stats-data.glib-stats-data')))):
		print('NO DATA AVAILABLE or PAGE DID NOT LOAD CORRECTLY')
		return [[]]'''

	page_html = browser.page_source
	soup = BeautifulSoup(page_html, 'html.parser')

	sub_leagues = soup.select('ul.bubble.stages-menu li.bubble')
	sub_leagues_text = [i.get_text() for i in sub_leagues]

	#Proceed here if there are no subleagues. I.E. League A, League B, League C...
	if len(sub_leagues) == 0:
		teams = soup.select('#table-type-1.stats-table > tbody > tr > td.participant_name > span.team_name_span')
		team_name = [i.get_text() for i in teams]

		stds = soup.select('td.rank.col_rank.no')
		std_list = [i.get_text() for i in stds]

		nation = soup.select('#breadcrumb > a:nth-child(4)')[0].get_text()
		nation_list = [nation for i in range(len(std_list))]

		league = soup.select('#breadcrumb > a:nth-child(4), #breadcrumb > a:nth-child(5)')
		league_name = ' '.join([i.get_text() for i in league])
		league_list = [league_name for i in range(len(std_list))]

		date_of_scrape = str(pd.to_datetime('now'))[0:10]
		dos_list = [date_of_scrape for i in range(len(std_list))]

		complete_std_list = [nation_list, league_list,
		                     dos_list, team_name,
		                     std_list]

		browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

		return(complete_std_list)

	#Proceed Here if there are subleagues
	else:
		sub_league_links = soup.select('li.bubble a')

		list_for_sub_leagues = []

		for link in sub_league_links:
			link = 'https://www.oddsportal.com' + link.get('href')

			if '/soccer/' in link:
				try:
					browser.get(link)
					page_html = browser.page_source

				except:
					internet_error = he.check_internet(browser)

					if internet_error:
						print('No Internet Connection - Restarting Program')
						browser.close()
						he.restart_program()

			soup = BeautifulSoup(page_html, 'html.parser')

			teams = soup.select('#table-type-1.stats-table > tbody > tr > td.participant_name > span.team_name_span')
			team_name = [i.get_text() for i in teams]

			stds = soup.select('td.rank.col_rank.no')
			std_list = [i.get_text() for i in stds]

			nation = soup.select('#breadcrumb > a:nth-child(4)')[0].get_text()
			nation_list = [nation for i in range(len(std_list))]

			league = soup.select('#breadcrumb > a:nth-child(4), #breadcrumb > a:nth-child(5)')
			league_name = ' '.join([i.get_text() for i in league])
			league_list = [league_name for i in range(len(std_list))]

			date_of_scrape = str(pd.to_datetime('now'))[0:10]
			dos_list = [date_of_scrape for i in range(len(std_list))]

			complete_std_list = [nation_list, league_list,
			                     dos_list, team_name,
			                     std_list]

			list_for_sub_leagues.append(complete_std_list)

			browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

		return list_for_sub_leagues

def check_presence_of_subleagues(std_list):
	for i in std_list:
		for j in i:
			if isinstance(j, list):
				return True

			else:
				return False