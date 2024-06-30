from typing import List, Dict

def is_valid_setup(setup: List, item_dict: Dict, line_lengths: tuple) -> bool:
	"""Checks for a valid setup. Some checks can be skipped for some items with the '*' option.

	Parameters:
		setup (list): The setup to be validated.
		item_dict (dict): A dictionary containing item information, sorted by MPU.
		line_lengths (tuple): A tuple containing the lengths of lines.
	
	Returns:
		bool: True if the setup is valid, False otherwise.
	"""
	return ([
		collision(setup, item_dict),
		line_lengths_check(setup, item_dict, line_lengths),
		corners(setup, item_dict),
		plat_possible(setup, item_dict),
		uniqueness(setup),
		xy_valid(setup, item_dict)
	])

def collision(setup: List, item_dict: Dict) -> bool:
	"""Returns the validity of the setup in terms of collision between upgraders. 
	Therefore, upgraders cannot collide with each other."""
	for i in range(len(setup)-1):
		if setup[i][3] != setup[i+1][3]:
			continue
		if setup[i][2] + item_dict[setup[i][0]]['Length'] > setup[i+1][1]:
			return False
	return True

def line_lengths_check(setup: List, item_dict: Dict, line_lengths: List) -> bool:
	"""Returns the validity of the setup in terms of line lengths. 
	Therefore, the total length of the setup must be equal to the sum of the line lengths."""
	length: int = 0
	lengths: List[int] = []
	for i in range(len(setup) - 1):
		length += item_dict[setup[i][0]]['Length']
		if setup[i][3] != setup[i+1][3]:
			lengths.append(length)
			length = 0
	lengths.append(length + item_dict[setup[-1][0]]['Length'])
	return lengths == line_lengths

def corners(setup: List, item_dict: Dict, depth=3) -> bool:
	"""Checks if there is collision between the upgraders in the corner, close to the dragon cannon.
	
	Items with '*' option for width will skip this check. Assumes that there are at least 3 upgraders before each dragon cannon if there are items after it.

	Parameters:
		setup (list): A list of platform items with their 'Name' and 'y' position.
		item_dict (dict): A dictionary mapping item names to their respective lengths.
		
	Returns:
		bool: True if the setup is valid, False otherwise.
	"""
	if len(setup) < 2:
		return True
	for i in range(len(setup)-1):
		if setup[i][3] != setup[i+1][3]:
			widthsA: List = [None] * depth #(widths // 2) of the 3 upgraders "a"fter the corner
			widthsB: List = [None] * depth #(widths // 2) of the 3 upgraders "b"efore the corner
			for j in range(0, depth):
				if i+1+j >= len(setup) or setup[i+1][3] != setup[i+1+j][3] or item_dict[setup[i+j][0]]['Width'] == '*': #<depth upgraders in line after corner
					widthsA[j] = 0
				else:
					widthsA[j] = item_dict[setup[i+j][0]]['Width'] // 2
				if i-j < 0 or setup[i][3] != setup[i-j][3] or item_dict[setup[i-j][0]]['Width'] == '*': #<depth upgraders in line before corner
					widthsB[j] = 0
				else:
					widthsB[j] = item_dict[setup[i-1-j][0]]['Width'] // 2
			
			for a in range(len(widthsA)):
				for b in range(len(widthsB)):
					if widthsA[0] > 2 + sum([item_dict[setup[i-1-c][0]]['Length'] for c in range(a)]) and \
						widthsB[1] > 3 + sum([item_dict[setup[i+c][0]]['Length'] for c in range(b)]):
						return False
	return True

def plat_possible(setup: List, item_dict: dict) -> bool:
	"""
	Determines if a given setup of platforms with hydraulic platforms is valid.

	A valid setup ensures that any 'peaks' of upgraders are consturctible with a conbination of length 8 and length 12 platforms.
	
	Parameters:
		setup (list): A list of platform items with their 'Name' and 'y' position.
		item_dict (dict): A dictionary mapping item names to their respective lengths.
		
	Returns:
		bool: True if the setup is valid, False otherwise.
	"""
	if len(setup) < 2:
		return True
	
	is_rising: bool = False  # True if the platforms are rising, False if falling
	length: int = 0

	for i in range(len(setup) - 1):
		item_name: str = setup[i][0]
		item_length: int = item_dict[item_name]['Length']
		length += item_length
		if (setup[i][3] != setup[i+1][3]): #last item is in the eval line, so it is not checked
			if (length < 8 or length % 4 != 0) and is_rising and setup[i][2] > 1:
				return False
			length = 0
			continue

		elif not is_rising:
			if setup[i][2] < setup[i+1][2]:
				is_rising = True
				length = 0
				
		else:
			if setup[i][2] > setup[i+1][2]:
				if length < 8 or length % 4 != 0:
					return False
				is_rising = False
				length = 0
			elif setup[i][2] != setup[i+1][2]:
				length = 0
	return True

def uniqueness(setup: List) -> bool:
	"""Checks if the setup is unique. Therefore, upgraders cannot be repeated."""
	return len([item[0] for item in setup]) == len(set([item[0] for item in setup]))

def xy_valid(setup: List, item_dict: dict) -> bool:
	"""Checks if the x/y coordinates of the setup are valid. Therefore, the x/y coordinates for each item must be in item_dict."""
	for item in setup: #item = [Name, x, y, line]
		if item[3] == 1:
			y_coords: List[int] = item_dict[item[0]]['Placements_1st_line'].get(item[1])
			if y_coords != None and item[2] in y_coords:
				return True
		y_coords: List[int] = item_dict[item[0]]['Placements_any_line'].get(item[1])
		if y_coords == None or item[2] not in y_coords:
			return False
	return True

if __name__ == '__main__':
	setup = [['Sideways Big Bertha', 1, 1, 1], ["Green Tea Latte + Reaper's Fortress", 3, 1, 1], ["Draedon's Gauntlet (instant)", 1, 1, 2], ['Eggcelent Upgrader', 5, 4, 2]]
	import Setup
	item_dict, portables_dict, line_lengths = Setup.load_csv()
	print(is_valid_setup(setup, item_dict, line_lengths)) #False