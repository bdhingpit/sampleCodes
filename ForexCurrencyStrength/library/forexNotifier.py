import telebot 
from telethon.sync import TelegramClient 
from telethon.tl.types import InputPeerUser, InputPeerChannel 
from telethon.tl.functions.messages import SendMessageRequest
from telethon import TelegramClient, sync, events

import pandas as pd
import datetime as dt

#Purpose: Send message containing the currency strength meter bars and datetime
#Input: fname = filename of curr strength meter image
#Output: None
def message_curr_strength(fname):
	api_id = 1433030
	api_hash = '33fa8cdfd1b35e902e6118b6abbf3726'
	token = '1315998116:AAF8A-WBdojAJMtp75o_zb3xcIykIX9bh_g'

	phone_num = '+639267415427'

	client = TelegramClient('session_name', api_id, api_hash)
	   
	client.connect() 
	  
	if not client.is_user_authorized(): 
	    client.send_code_request(phone_num) 
	    client.sign_in(phone_num, input('Enter the code: ')) 
	   
	destination_group = 'https://t.me/joinchat/TwIbzlVqFT986_g0-Dai_A'
	peer = client.get_entity(destination_group)

	time = pd.to_datetime('now').strftime('%Y-%m-%d %H:%M')

	client.send_message(entity=peer, 
		                message='Currency Strength Bar {}'.format(time), 
		                parse_mode='html') 
	client.send_file(entity=peer, file=fname)

	strength_values = ''
	with open('currStrengthOutputs/currStrengthValues.txt', 'r') as f:
		for line in f:
			strength_values += line

	tradable_pairs = ''
	with open('currStrengthOutputs/tradeableCurrPair.txt', 'r') as f:
		for line in f:
			tradable_pairs += line

	client.send_message(entity=peer,
		                message='Currency Strength Values',
	                    parse_mode='html')
	client.send_message(entity=peer,
		                message=strength_values,
		                parse_mode='html')
	
	client.send_message(entity=peer,
		                message='Tradable Pairs and Difference',
		                parse_mode='html')
	client.send_message(entity=peer,
		                message=tradable_pairs,
		                parse_mode='html')

	client.disconnect()

	return None

