# Setup-Builder
Setup builder (v1.1.0) for Miner's Haven, by agentanti714. WIP

CURRENTLY DOING: website for this thing

>[!NOTE]
>**To use, open Setup.py**

>[!WARNING]
>DO NOT USE COMMAS AS ANYTHING OTHER THAN SEPARATORS/DELIMITERS BETWEEN ENTRIES FOR .csv FILES

--------------------------------------------------
**items.csv**
- items.csv follows format: NAME, MULTI, LENGTH, WIDTH

- Width can use * to assume best case with fitting it around railgun corners

- Example entry:

  Quantum Clockwork,120,4,8

**placements.csv**
- placements.csv follows format: NAME, X, Y, 1st_OR_Any

- X, Y are relative to 1st dragon cannon, starting with 1.
- For example, a valid placement directly after a draogn cannon, on the same platform as the dragon cannon has X = 1, Y = 0.

- Example entry:
  
  Alien Relic,1,-1,Any

**portables.csv**
- portables.csv follows format: NAME, MULTI, LENGTH (optional)
- Example entry:
  
  Past+Present+Future,360,6

--------------------------------------------------
WIP:

Making Setup.setup_generate run faster

Portables items in general (All portable items are assumed to fit ideally (e.g. angel's always gets x150))

Built setups assumes that the for items with random multiplier, that the overall setup multiplier follows a normal distribution by the central limit theorem.

Some items should have a custom expression for their multi, mainly ooftopian.

INCLUDES:

- TBC

DOES NOT INCLUDE:

- The Death Cap (please just put the value you actually get)

Also, try to help me populate items.csv and placements.csv 🙏
