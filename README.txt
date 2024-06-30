Setup v.1.0.0

To use, open Setup.py
TBC: Built setups assumes that the for items with random multiplier, that the overall setup multiplier follows a normal distribution by the central limit theorem.

All portable items are assumed to fit ideally (e.g. angel's always gets x150)
DO NOT USE COMMAS AS ANYTHING OTHER THAN SEPARATORS/DELIMITERS BETWEEN ENTRIES
--------------------------------------------------
items.csv follows format: NAME, MULTI, LENGTH, WIDTH

Width can use * to assume best case with fitting it around railgun corners

Example entry: 
Quantum Clockwork,120,4,8
--------------------------------------------------
placements.csv follows format: NAME, X, Y, 1st_OR_Any

X, Y are relative to 1st dragon cannon, starting with 1.
For example, a valid placement directly after a railgun, on the same platform as the  has X = 1.

Example entry: 
Alien Relic,1,-1,Any
--------------------------------------------------
portables.csv follows format: NAME, MULTI, LENGTH (optional)

Example entry:
Past+Present+Future,360,6
--------------------------------------------------
TBC
Some items have a custom expression for their multi, mainly condition-based upgraders.
INCLUDES:
-TBC
DOES NOT INCLUDE:
-The Death Cap (please just put the value you actually get)