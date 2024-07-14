#v 1.0.1
import sys
import os
import csv
from time import sleep
from math import floor, log10
from typing import List, Dict

import Validator
import Generator

def clear_console() -> None:
	"""Cross-platform clear screen"""
	os.system('cls' if os.name == 'nt' else 'clear')

def build_setup(): #TODO: finish buildSetup
	item_dict, portables_dict, line_lengths = load_csv()

	sys.stdout.write(f"Line lengths: {line_lengths}\n\n")
	sys.stdout.write("Press Enter to continue\n")
	sys.stdin.readline()
	clear_console()

	sys.stdout.write("Generating...\n")
	setup = Generator.setup_generate(item_dict, line_lengths)
	clear_console()

	sys.stdout.write("\nGenerated setup:\n")
	for item in setup:
		sys.stdout.write(f"{item[0]} at line {item[3]} at ({item[1]}, {item[2]})\n")

	sys.stdout.write(f'Validator returns: {Validator.is_valid_setup(setup, item_dict, line_lengths)}\n')
	sys.stdout.write("\nPress Enter to return\n")
	sys.stdin.readline()
	return 0

def load_csv() -> List:
	"""Loads the csv files and returns a list of dicts."""
	with open("items.csv", "r", newline='') as upgraders:
		reader = csv.DictReader(upgraders, fieldnames=['Name', 'Multi', 'Length', 'Width', 'Placements_1st_line', 'Placements_any_line'])
		_ = {row["Name"]: parse_items_csv_row(row) for row in reader}
		sorted_items = sorted(_.items(), key=lambda kv: (kv[1]['Multi']**(1/kv[1]['Length'])), reverse=True)
		item_dict = {item[0]: item[1] for item in sorted_items} #item_dict is a dict of dicts

	with open('placements.csv', 'r', newline='') as placements:
		reader = csv.DictReader(placements, fieldnames=['Name', 'x', 'y', '1st_or_any_line'])
		while (row := next(reader, None)) is not None:
			if row['x'] == '*' and row['y'] == '*':
				if row['1st_or_any_line'] == '1st':
					for i in range(1,57):
						item_dict[row['Name']]['Placements_1st_line'][i] = [1,2,3,4]
				elif row['1st_or_any_line'] == 'Any':
					for i in range(1,57):
						item_dict[row['Name']]['Placements_any_line'][i] = [1,2,3,4]
				else:
					raise ValueError("Invalid placement type. Must be '1st' or 'Any'.")
				continue
			
			row['x'] = int(row['x'])
			row['y'] = int(row['y'])
			
			if row['1st_or_any_line'] == '1st':
				if row['x'] in item_dict[row['Name']]['Placements_1st_line']:
					item_dict[row['Name']]['Placements_1st_line'][row['x']].append(row['y'])
				else:
					item_dict[row['Name']]['Placements_1st_line'][row['x']] = [row['y']]
			elif row['1st_or_any_line'] == 'Any':
				if row['x'] in item_dict[row['Name']]['Placements_any_line']:
					item_dict[row['Name']]['Placements_any_line'][row['x']].append(row['y'])
				else:
					item_dict[row['Name']]['Placements_any_line'][row['x']] = [row['y']]
			else:
				raise ValueError("Invalid placement type. Must be '1st' or 'Any'.")

	with open("portables.csv", "r", newline='') as portables:
		reader = csv.DictReader(portables, fieldnames=['Name', 'Multi'])
		portables_dict: Dict = {row["Name"]: parse_portables_csv_row(row) for row in reader} #portables_dict is a dict of dicts
	
	with open("line_lengths.txt", "r") as file:
		line_lengths: tuple = list(map(int, file.readline().split(','))) #line_lengths is a tuple of integers
	
	return item_dict, portables_dict, line_lengths

def parse_items_csv_row(row: Dict) -> Dict: 
	"""Reads a row from items.csv and returns a dict with NAME: {NAME: <NAME>, MULTI: <MULTI>, LENGTH: <LENGTH>, ...}. 
	'*' is used to skip validation checks for some items."""
	row['Multi'] = float(row['Multi'])
	row['Length'] = int(row['Length'])
	row['Width'] = int(row['Width']) if row['Width'] != '*' else '*'
	row['Placements_1st_line'] = {} #Dict[int: list]
	row['Placements_any_line'] = {} #Dict[int: list]
	return row

def parse_portables_csv_row(row: Dict):
	"""Reads a row from portables.csv and returns a dict with NAME: {NAME: <NAME>, MULTI: <MULTI>}. """
	if any([row[['Name', 'Multi'][i]] == '*' for i in [0, 1]]):
		raise ValueError("'Name', 'Multi' cannot skip validation checks using '*' option.")
	row['Multi'] = float(row['Multi'])
	return row

def multi_calc(setup: List, item_dict: Dict, line_lengths: tuple, portables_dict: Dict) -> float:
	"""Calculates the total multiplier of the setup. Rng-based items' rng is handled in stdev_calc instead."""
	multi = 1
	for item in setup:
		multi *= item_dict[item['Name']]['Multi']
	return multi
	
def multi_calc2(setup: List, item_dict: Dict, line_lengths: tuple) -> float: #TODO: finish multiCheck2, may not be feasible
	"""Calculates the total multiplier of the setup. There are a few special cases. Rng-based items' rng is handled in stdev_calc."""
	raise NotImplementedError
	multi = 160e18
	specialCases = [] # ["Ooftopian Refiner", "Garden of Gaia", "Enchanted Library"]
	gaia = False
	for i, item in enumerate(setup):
		if item['Name'] in specialCases:
			if item['Name'] == "Ooftopian Refiner":
				multi *= 3/2*floor(log10(multi)/3)
			elif item['Name'] == "Garden of Gaia":
				multi *= 75
				gaia = True
			elif item['Name'] == "Enchanted Library":
				pass
			else:
				raise Exception("HOW DID YOU GET HERE?")
		else:
			multi *= item_dict[item['Name']]['Multi']
			if gaia:
				multi *= 1.02
	return multi

def adjust_settings() -> None:
	with open("line_lengths.txt", "r+") as file:
		line_lengths = file.read()
	sys.stdout.write(f"Line lengths: {line_lengths}\n\n")

	sys.stdout.write("Enter new line lengths or press Enter to return: \n")
	option = sys.stdin.readline()

	if option != "\n":
		with open("line_lengths.txt", "r+") as file:
			file.write(f"{option}")
		sys.stdout.write("\nSettings updated. Press Enter to return\n")
		sys.stdin.readline()
	
	clear_console()
	return 0
	
def instructions() -> None:
	with open("README.txt", "r+") as _:
		sys.stdout.write(_.read())
	sys.stdout.write("\n\nPress Enter to return\n")
	sys.stdin.readline()

def credit() -> None:
	with open("credits.txt", "r+") as _:
		sys.stdout.write(_.read())
	sys.stdout.write("\n\nPress Enter to return\n")
	sys.stdin.readline()

def main(args: List) -> int:
	'''Main menu for the setup generator.'''
	options = {
		'1': build_setup,
		'2': adjust_settings,
		'3': instructions,
		'4': credit,
		'5': lambda: None  # Exit option
	}

	while True:
		clear_console()
		print("Choose options:\n"
			  "1: Generate setup\n"
			  "2: Adjust Settings\n"
			  "3: Instructions\n"
			  "4: Credits\n"
			  "5: Exit"
		)

		option = input().strip()
		clear_console()

		if option in options:
			if option == '5':
				break
			options[option]()
		else:
			print("Invalid option. Try again.")
			sleep(1)
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
