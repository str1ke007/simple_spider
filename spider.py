#!/usr/bin/python3

from requests.exceptions import ConnectionError, HTTPError
from urllib3.exceptions import NewConnectionError, LocationParseError
import requests
import re
import colors as c
from time import sleep
import os


def get_links_from():
	flag = 0
	while True:
		try:
			url = input(f"{c.GREEN}[+] Enter URL{c.RED}(only!){c.GREEN}: ")
			flag = 1
			response = requests.get(f"https://{url}/", timeout=2)
			response.raise_for_status()
		except (ConnectionError, NewConnectionError, LocationParseError, HTTPError):
			print(f"\n{c.RED}[-] URL invalid!\n[-] Please wait...")
			flag = 0
			sleep(2)
			os.system('clear')
		if flag == 1:
			break

	return re.findall('(?:href=")(.*?)"', str(response.content))


def main():
	url_list = []
	url_result = get_links_from()
	print()
	for ur in url_result:
		url_f = re.findall('(?:.*://)(.*)', str(ur))
		url_list.append(url_f)
	display(url_list)


def display(url_list):
	count = 0
	url_result = []
	for x in url_list:
		if x:
			for y in x:
				url_result.append(y)
				print(f"{c.MAGENTA}[-] {y}")
				count += 1
	print(f"\n\n{c.RED}[+] Total number of links: {count}\n\n")
	print(f"{c.GREEN}[+] Saving links in a {c.RED}.txt {c.GREEN}file\n")
	save_in_disk(url_result)
	if count > 50:
		sleep(10)
	else:
		sleep(5)
	print(f"{c.GREEN}[+] Links stored successfully in {c.RED}{os.getcwd()}/url.txt\n\n{c.WHITE}")


def save_in_disk(url_result):
	with open("url.txt",'w') as f:
		for x in url_result:
		   		f.write(f"{x}\n")


main()
