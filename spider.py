#!/usr/bin/python3

import requests
import re
import os
import colors as c
from concurrent.futures import ThreadPoolExecutor

class Spider:
    def __init__(self):
        self.url_list = []
        self.num_threads = 5  # Default

    def get_links_from(self):
        while True:
            try:
                print(f"{c.GREEN}[+] Please enter the Domain Name (e.g., example.com)")
                url = input(f"{c.GREEN}[+] Enter Domain Name{c.RED}(only!){c.GREEN}: ")
                response = requests.get(f"https://{url}/", timeout=2)
                if response.status_code == 404 or not response.content:
                    print(f"\n{c.RED}[-] Error: No such domain name exists.\n[-] Please try again...")
                    continue
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"\n{c.RED}[-] Error: {e}\n[-] Please try again...")
            else:
                break

        self.url_list = re.findall('(?:href=")(.*?)"', str(response.content))
        return self.url_list


    def display(self):
        count = 0
        url_result = []  # URLs
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = [executor.submit(self.get_domain_name, url) for url in self.url_list]

        for future in futures:
            url_f = future.result()
            if url_f:
                url_result.extend(url_f)  # Extend URLs
                count += len(url_f)
                for y in url_f:
                    print(f"{c.MAGENTA}[-] {y}")

        print(f"\n\n{c.RED}[+] Total number of links: {count}\n\n")
        print(f"{c.GREEN}[+] Saving links in a {c.RED}.txt {c.GREEN}file\n")
        self.save_in_disk(url_result)  # Save the URLs
        print(f"{c.GREEN}[+] Links stored successfully in {c.RED}{os.getcwd()}/url.txt\n\n{c.WHITE}")

    def save_in_disk(self, url_result):
        with open("url.txt", 'w') as f:
            for x in url_result:
                f.write(f"{x}\n")

    def get_domain_name(self, url):
        return re.findall('(?:.*://)(.*)', str(url))


def main():
    try:
        spider = Spider()
        url_result = spider.get_links_from()

        while True:
            try:
                num_threads = int(input(f"{c.GREEN}[+] How many threads do you want to use? (Default: 5): "))
                if num_threads > 0:
                    spider.num_threads = num_threads
                break
            except ValueError:
                print(f"{c.RED}[-] Invalid input. Please enter a valid number.")

        spider.display()
    except KeyboardInterrupt:
        print(f"\n{c.RED}[-] Operation interrupted by user.\n")
    except Exception as e:
        print(f"{c.RED}[-] An error occurred: {e}\n")

if __name__ == "__main__":
    main()
