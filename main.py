# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
import random
import time
import os
import re
from telethon import *

# Seps For Stripe
seps = "\n\r "

# Clients Array
telegram_clients = {}


def spin(spintax):
	word, n = re.subn('{([^{}]*)}', lambda m: random.choice(m.group(1).split("|")), spintax)
	return word.strip()


async def connect_accounts():
	group_name = input('Please input group name: ')
	min_interval = input('Please input a minimum interval in second: ')
	max_interval = input('Please input a maximum interval in second: ')
	min_interval = int(min_interval)

	max_interval = int(max_interval)

	# Sync Accounts
	account_file = open("accounts.txt", "r")
	accounts_data = account_file.readlines()

	for i in range(0, len(accounts_data), 3):
		phone_number = accounts_data[i].strip(seps)
		api_id = accounts_data[i + 1].strip(seps)
		api_hash = accounts_data[i + 2].strip(seps)

		# print("{}, {}, {}".format(phone_number, api_id, api_hash))

		telegram_clients[phone_number] = TelegramClient(phone_number, api_id, api_hash)

		try:
			await telegram_clients[phone_number].connect()
		except Exception as e:
			print('Failed to connect', e)

		await telegram_clients[phone_number].sign_in(phone_number)

		while not await telegram_clients[phone_number].is_user_authorized():
			print(telegram_clients[phone_number])
			input_code = input("{}\nPlease enter the received code: ".format(phone_number))
			try:
				await telegram_clients[phone_number].sign_in(phone_number, input_code)
				break
			except Exception as e:
				print("Sign In Exception", e)

		await telegram_clients[phone_number].get_dialogs()

	comment_file = open("comments.txt", "r",encoding ="utf8")
	comments = comment_file.readlines()
	random.shuffle(comments)
	for i in range(0, len(comments)):
		# Stripe Whitespace And Newline
		comment = comments[i].strip("\n")


		# Select Random Client
		random_client = random.choice(list(telegram_clients.values()))
		if comment == "gif":
			file = random.choice(os.listdir("gifs"))
			await random_client.send_file(group_name, "gifs/{}".format(file))
		elif comment != "gif":
			comment = spin(comment)
			try:
				await random_client.send_message(group_name, comment)
				# await random_client.send_file('BotTest_Group', random.choice(stickers.documents))

			except Exception as e:
				print("Send Message Exception", e)
				time.sleep(random.randint(min_interval, max_interval))
	   


if __name__ == '__main__':
	aio_loop = asyncio.get_event_loop()
	aio_loop.run_until_complete(connect_accounts())
