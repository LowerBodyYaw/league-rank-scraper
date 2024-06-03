import requests
import re

from bs4 import BeautifulSoup
from json import loads, dump
from itertools import cycle

class RankChecker:

	def __init__(self) -> None:
		self.session: requests.Session = requests.Session()
		self.results: list = []

	def save_results(self) -> None:

		with open("results.json", "w") as f:
			dump(self.results, f, indent=4)

	def check_rank(self, username: str) -> str:

		username_c: str = username.replace("#", "-")
		proxy: str = next(proxies_iter)
		proxies: dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}

		try:
			request = self.session.get(f"https://www.op.gg/summoners/na/{username_c}", proxies=proxies, timeout=7)
			pattern = re.compile(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.DOTALL)
			match = re.search(pattern, request.text)

			if match:
				json: dict = loads(match.group(1))
				previous: list = json['props']['pageProps']['data']['previous_seasons']
				ranks: list = [season['tier_info']['tier'] for season in previous]

				if ranks:

					print(f"[+] {username}:" + ",".join(ranks))

					result: dict = {
						"username": username,
						"ranks": ranks
					}

					self.results.append(result)
		except requests.exceptions.ProxyError:
			print("[-] a proxy error has occurred.")
		except requests.exceptions.Timeout:
			print("[-] a proxy timeout error has occurred, probably due to slow proxies!")
		except:
			#error handling is useless because we dont care if it doesnt have past ranks / it isnt found, unless it's proxy error
			pass

	def main(self) -> None:

		for username in usernames:
			self.check_rank(username)

		self.save_results()

def load_usernames() -> list:

	with open("usernames.txt") as f:
		usernames = f.read().splitlines()

	return usernames

def load_proxies() -> list:

	with open("proxies.txt") as f:
		proxies = f.read().splitlines()

	return proxies

if __name__ == "__main__":

	usernames: list = load_usernames()
	proxies: list = load_proxies()
	proxies_iter: cycle = cycle(proxies)
	rankchecker = RankChecker()
	rankchecker.main()