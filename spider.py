#!/usr/bin/python3

import requests as r
import re
import colors as c
from time import sleep


def get_links_from(url):
	try:
		response = r.get(f"https://{url}/", timeout=2)
		if response.status_code == 200:
			return re.findall('(?:href=")(.*?)"', str(response.content))
		else:
			print(f"\n\n{c.RED}[-] URL invalid!\n\n")
			exit(0)
	except EXCEPTION:
		print(f"\n\n{c.RED}[-] Error!\n\n")


def main():
	url_list = []
	url_result = get_links_from(url)
	print()
	for ur in url_result:
		url_f = re.findall('(?:.*://)(.*)', str(ur))
		url_list.append(url_f)
	display(url_list)


def display(url_list):
	count = 0
	url_result = []
	print(f"\n{c.GREEN}[-] URL: {url}\n")
	for x in url_list:
		if x:
			for y in x:
				url_result.append(y)
				print(f"{c.MAGENTA}[-] {y}")
				count += 1
	print(f"\n\n{c.RED}[-] Total number of links: {count}\n\n")
	print(f"{c.GREEN}[-] Saving links in a {c.RED}.txt {c.GREEN}file\n")
	save_in_disk(url_result)
	if count > 50:
		sleep(10)
	else:
		sleep(5)
	print(f"{c.GREEN}[-] Links stored successfully in {c.RED}url.txt\n\n{c.WHITE}")


def save_in_disk(url_result):
	with open("url.txt",'w') as f:
		for x in url_result:
		   		f.write(f"{x}\n")


url = input(f"{c.GREEN}[-] Enter URL: ")
main()
