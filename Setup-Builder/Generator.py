import csv
from typing import List, Dict
from functools import wraps
from time import time

def timing(f): #taken from stackoverflow
	"""Decorator to time a function."""
	@wraps(f)
	def wrap(*args, **kw):
		ts = time()
		result = f(*args, **kw)
		te = time()
		#print('func:%r args:[%r, %r] took: %2.4f sec' % \
		#  (f.__name__, args, kw, te-ts))
		print('func:%r took: %2.4f sec' % \
		  (f.__name__, te-ts))
		return result
	return wrap

@timing
def setup_generate(item_dict: Dict, line_lengths: List[int]) -> List[List]: #List of [name, x, y, line_no]
	'''Recursively generates a setup of upgraders with the highest possible multiplier.

	Parameters:
		item_dict (Dict[str: dict[str: str, str: int, str: dict[int: [list[int]]]]]): A dictionary mapping item names to their respective lengths, multipliers, widths and possible placements.
		line_lengths (list): A list of integers representing the lengths of each line.
	
	Returns:
		list: A list of lists, each containing the name of the item, its x and y coordinates and the line number.
	'''
	def permutational_sum(item_dict, line_lengths, path, x_coord, product, length, is_rising):
		nonlocal result
		nonlocal result_multi
		line_no = 1 if path == [] else path[-1][3]
		
		if line_lengths[-1] == 0: #case: end of all lines
			result_multi = product
			result = path[:]
			return
		
		elif line_lengths[line_no - 1] == 0: #case: end of a line, not end of all lines
			for item in [v for k, v in item_dict.items() if is_valid_placement(item_dict, v, 1, line_lengths, line_no + 1, product, result_multi)]:
				if not corner_check(path[-6:], static_item_dict):
					continue
				if (length < 8 or length % 4 != 0) and is_rising and path[-1][2] > 1:
					continue
				available_placements = item['Placements_any_line']
				new_line_lengths = line_lengths[:]
				new_line_lengths[line_no] -= item['Length']
				new_item_dict = item_dict.copy()
				new_item_dict.pop(item['Name'])
				for i in available_placements[1]:

					path.append([item['Name'], 1, i, line_no + 1])
					permutational_sum(new_item_dict, new_line_lengths, path, item['Length'] + 1, product * item['Multi'], 0, False)
					path.pop()

		else:
			y_coord = -24 if (path == [] or line_no != path[-1][3]) else path[-1][2]

			for item in [v for v in item_dict.values() if is_valid_placement(item_dict, v, x_coord, line_lengths, line_no, product, result_multi)]:
				if len(path) > 5 and path[-4][3] != path[-1][3] and not corner_check(path[-6:], static_item_dict):
					continue
				if line_no == 1:
					available_placements = union_dicts(item['Placements_1st_line'], item['Placements_any_line'])
				else:
					available_placements = item['Placements_any_line']
				new_line_lengths = line_lengths[:]
				new_line_lengths[line_no - 1] -= item['Length']
				new_item_dict = item_dict.copy()
				new_item_dict.pop(item['Name'])

				for i in available_placements[x_coord]:
					if i > y_coord: #check if y_coord is now rising
						path.append([item['Name'], x_coord, i, line_no])
						permutational_sum(new_item_dict, new_line_lengths, path, x_coord + item['Length'], product * item['Multi'], item['Length'], True)
						path.pop()
					elif i < y_coord: #check if y_coord is now falling
						if is_rising and (length % 4 != 0 or length == 4):
							continue
						else: #basically a midplat
							path.append([item['Name'], x_coord, i, line_no])
							permutational_sum(new_item_dict, new_line_lengths, path, x_coord + item['Length'], product * item['Multi'], item['Length'], False)
							path.pop()
					else: #y_coord is the same
						path.append([item['Name'], x_coord, i, line_no])
						permutational_sum(new_item_dict, new_line_lengths, path, x_coord + item['Length'], product * item['Multi'], length + item['Length'], is_rising)
						path.pop()

	#Driver code
	global static_item_dict
	static_item_dict = item_dict.copy()
	result: list = []
	result_multi: float = 1.0
	permutational_sum(item_dict, line_lengths, [], 1, 1, 0, False)

	return result[:]

def corner_check(setup: List, item_dict, depth=3) -> bool:
	"""Checks if the setup has a valid corner configuration, ensuring the width of upgraders do not collide with each other.
	
	Parameters:
		setup (list): A list of upgraders.
		item_dict (dict): A dictionary mapping item names to their respective lengths.
		depth (int): The number of upgraders to check before and after the corner.
	
	Returns:
		bool: True if the setup has a valid corner configuration, False otherwise.
		
	"""
	if len(setup) < 2:
		return True
	for i in range(len(setup)-1):
		if setup[i][3] != setup[i+1][3]:
			widthsA: List = [None] * depth #(widths // 2) of the 3 upgraders "a"fter the corner
			widthsB: List = [None] * depth #(widths // 2) of the 3 upgraders "b"efore the corner
			for j in range(0, depth):
				if i+1+j >= len(setup) or setup[i+1][3] != setup[i+1+j][3] or item_dict[setup[i+1+j][0]]['Width'] == '*': 
					widthsA[j] = 0 #<depth upgraders in line after corner
				else:
					widthsA[j] = item_dict[setup[i+1+j][0]]['Width'] // 2
				
				if i-j < 0: #<depth upgraders in line before corner
					widthsB[j] = 0
				elif setup[i][3] != setup[i-j][3]:
					widthsB[j] = 0
				elif item_dict[setup[i-j][0]]['Width'] == '*':
					widthsB[j] = 0
				else:
					widthsB[j] = item_dict[setup[i-j][0]]['Width'] // 2
			
			for a in range(len(widthsA)):
				for b in range(len(widthsB)):
					if widthsA[0] > 2 + sum([item_dict[setup[i-1-c][0]]['Length'] for c in range(a)]) and \
						widthsB[1] > 3 + sum([item_dict[setup[i+c][0]]['Length'] for c in range(b)]):
						return False
	return True

def is_valid_placement(item_dict: Dict, item: Dict, x_coord: int, line_lengths: List[int], line_no: int, product: float, result_multi: float) -> bool:
	"""Validates an item's placement in that position in terms of length, existence of placement, multipliers and knapsack algorithm.
	
	Parameters:
		item_dict (dict): A dictionary mapping item names to their respective names, multipliers, lengths and possible placements.
		item (dict): A dictionary representing the item to be placed.
		x_coord (int): The x-coordinate of the item.
		line_lengths (list): A list of integers representing the lengths of each line.
		line_no (int): The line number of the item.
		product (int): The product of the multipliers of the items placed so far.
		result_multi (int): The highest product of multipliers obtained so far.

	Returns:
		bool: True if the item placement is valid and worth checking, False otherwise.
	"""
	line_length = line_lengths[line_no - 1]
	if item['Length'] > line_length: #item too long for line
		return False
	elif (x_coord) not in item['Placements_any_line'] and line_no != 1: #item has no valid placement on line
		return False
	elif (x_coord not in item['Placements_1st_line']) and \
		(x_coord not in item['Placements_any_line']): #item has no valid placement on line 
		return False
	else:
		# Fast, cheap check if item is worth placing
		over_best = 1 #higher bound of the best case scenario
		length = sum(line_lengths) - item['Length']
		for i in item_dict.values():
			over_best *= i['Multi']
			length -= i['Length']
			if length <= 0:
				break
		
		# If the product of the item's multiplier and the best case scenario is less than the current best, skip
		if product * item['Multi'] * over_best <= result_multi:
			return False
		elif length == 0:
			return True
		
		# Knapsack algorithm to determine if item is worth placing
		def knapsack(W, wt, val, n):
			
			# Making the dp array
			dp = [1 for i in range(W+1)]

			# Taking first i elements
			for i in range(1, n+1):
				for w in range(W, 0, -1):
					if wt[i-1] <= w:
						dp[w] = max(dp[w], dp[w-wt[i-1]]*val[i-1])
			return dp[W]
		
		# Driver code
		item_list = sorted([item for item in item_dict.values()], key=lambda x: x['Length'])
		item_lengths = [item['Length'] for item in item_list]
		item_multis = [item['Multi'] for item in item_list]
		best_case = knapsack(sum(line_lengths) - item['Length'], item_lengths, item_multis, len(item_dict))

		if (product * item['Multi'] * best_case ) > result_multi:
			pass
		return (product * item['Multi'] * best_case ) > result_multi
	
def union_dicts(dict1, dict2) -> Dict:
	"""Returns a dictionary that is the union of two dictionaries.\n
	If they both have a list under the same key, the union of the lists is taken.
	"""

	result = {}
	
	# Process all keys from both dictionaries
	all_keys = set(dict1.keys()).union(dict2.keys())
	
	for key in all_keys:
		# Get values from both dictionaries, use an empty list if key is missing
		values1 = dict1.get(key, [])
		values2 = dict2.get(key, [])
		
		# Take the union of both lists
		union_values = list(set(values1).union(values2))
		
		# Store in result dictionary
		result[key] = union_values
	
	return result

def main():
	import Setup
	item_dict, portables_dict, line_lengths = Setup.load_csv()
	line_lengths = [10,10]
	result = setup_generate(item_dict, line_lengths)
	print(result)

if __name__ == "__main__":
	main()
