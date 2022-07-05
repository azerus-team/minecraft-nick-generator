import stringtools
import colorama
import json
from urllib.request import urlopen
from typing import List

# On Windows, calling init() will filter ANSI escape sequences out of any text sent to stdout or stderr, and replace 
# them with equivalent Win32 calls.
colorama.init(True)

# Generating json file, to cache nicks
try:
	cache_nicks = json.load(open("cache_nicks.json"))
except FileNotFoundError:
	example = {"Example": False}
	json.dump(example, open("cache_nicks.json", "w"))
	cache_nicks = json.load(open("cache_nicks.json", "r"))

def generate_minecraft_nick(length=4, attempts = 600) -> List:

	if length > 16:
		raise ValueError("The length of the nickname can't be bigger than 16 characters")
	if length <= 2:
		raise ValueError("The length of the nickname can't be less than 2 characters")

	valid_list = []
	name_list = []

	# Generating nicknames
	for i in range(attempts):
		name = stringtools.generate_nick(length=length)
		# Checking if nickname is already cached
		if name in cache_nicks:
			print(f"Name: {name}, was already checked, and it's", cache_nicks[name])
		else:
			name_list.append(name)


	for name in name_list:
		# Storing the URL in url as parameter for urlopen

		url = f"https://api.mojang.com/users/profiles/minecraft/{name}"

		# Storing the response of URL
		response = urlopen(url)

		# Trying to store the JSON response
		try:

			data_json = json.loads(response.read())
			print(f"{colorama.Fore.LIGHTBLACK_EX + 'Name:'} {colorama.Fore.RED + name}")

			# Caching the nickname
			cache_nicks[name] = False
			json.dump(cache_nicks, open("cache_nicks.json", "w+"), indent=4, sort_keys=True)
		
		# If there is nothing to store, than the nickname is available
		except json.JSONDecodeError:
			valid_list.append(name)
			print(f"{colorama.Fore.LIGHTWHITE_EX + 'Name:'} {colorama.Fore.GREEN + name}")

			# Caching the nickname
			cache_nicks[name] = True
			json.dump(cache_nicks, open("cache_nicks.json", "w+"), indent=4, sort_keys=True)

	return valid_list

print(" ".join(generate_minecraft_nick(length=4, attempts=50)))