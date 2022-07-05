import stringtools
import colorama
import json
import argparse
from urllib.request import urlopen
from typing import List

class Generate_minecraft_nick():
	json_name = "cache_nicks.json"
	def __init__(self, length, attempts) -> List:
		'''Generate O.G minecraft nicknames'''
		# On Windows, calling init() will filter ANSI escape sequences out of any text sent to stdout or stderr, and replace 
		# them with equivalent Win32 calls.
		colorama.init(True)

		self.__raise_errors(length)

		self.cache_nicks = self.config_json(self.json_name)
		self.name_list = self.generate_nicks(attempts=attempts, length=length, check_json=self.cache_nicks)

		self.attempts = attempts
		self.length = length
		self.response = self.request_api(self.name_list)


	def __str__(self) -> str:
		return str(self.response)

	def __iter__(self) -> List:
		return iter(self.response)


	def generate_nicks(self, attempts, length, check_json):
		name_list = [] # Storing nicknames here

		# Generating nicknames using stringtools
		for i in range(attempts):
			name = stringtools.generate_nick(length=length)

			# Checking if nickname is already cached, and if so repicking it
			if name in check_json:
				while name in check_json:
					name = stringtools.generate_nick(length=length)
				name_list.append(name)

			# If it's not cached, adding to name_list
			else:
				name_list.append(name)
		return name_list

	def config_json(self, json_name):
		'''Generate json file, to cache nicks'''
		try:
			cache_nicks = json.load(open(json_name))
		except FileNotFoundError:
			example = {"Example": False}
			json.dump(example, open(json_name, "w"))
			cache_nicks = json.load(open(json_name, "r"))
		finally:
			return cache_nicks

	def __raise_errors(self, length):
		if length > 16:
			raise ValueError("The length of the nickname can't be bigger than 16 characters")
		elif length <= 2:
			raise ValueError("The length of the nickname can't be less than 2 characters")
	
	def __write_to_json(self, name, _bool, json_name):
		self.cache_nicks[name] = _bool
		json.dump(self.cache_nicks, open(json_name, "w+"), indent=4, sort_keys=True)

	def request_api(self, names: List) -> List:
		'''Returns available nicknames.'''
		# Requesting information from https://api.mojang.com/users/profiles/minecraft/name

		valid_list = [] # Storing available nicknames in here
		
		for name in names:
			# Storing the URL in url as parameter for urlopen
			url = f"https://api.mojang.com/users/profiles/minecraft/{name}"

			# Storing the response of URL
			response = urlopen(url)

			# Trying to store the JSON response
			try:
				data_json = json.loads(response.read())
				print(f"{colorama.Fore.LIGHTBLACK_EX + 'Name:'} {colorama.Fore.RED + name}")

				# Caching the nickname
				self.__write_to_json(name, False, self.json_name)
			
			# If there is nothing to store, than the nickname is available
			except json.JSONDecodeError:
				valid_list.append(name)
				print(f"{colorama.Fore.LIGHTWHITE_EX + 'Name:'} {colorama.Fore.GREEN + name}")

				# Caching the nickname
				self.__write_to_json(name, True, self.json_name)

		return valid_list

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Generate minecraft o.g names. Creates json file, with nicknames, and their aviability.')
	parser.add_argument('-l','--length', help='Choose the length of the nickname e.g: 4', required=True, type=int)
	parser.add_argument('-a','--attempts', help='Choose how many attempts to find vaild nickname will be made, e.g: 600', required=True, type=int)
	args = vars(parser.parse_args())
	Generate_minecraft_nick(length=args["length"], attempts=args["attempts"])
