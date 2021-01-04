import os
import sys
import psutil
import logging
import time

from bs4 import BeautifulSoup

#Restarts the current program, with file objects and descriptors cleanup
def restart_program():
    print('Restarting the program in 5...')

    ticker = 5
    for i in range(4):
    	ticker -= 1
    	print(ticker)
    	time.sleep(1)

    os.execl(sys.executable, sys.executable, *sys.argv)

#Check if the internet is up - Returns True if it's down and vice versa
def check_internet(browser):
	try:
		try:
			browser.find_element_by_class_name('offline')

		except:
			browser.find_element_by_id('reload-button')

		return True

	except:
		return False

def check_page_blank(browser, main_content):
	try:
		print('it is false')
		main_content
		return False

	except:
		print('It is True')
		return True
