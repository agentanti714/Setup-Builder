import math
import sys

def is_split():
    while True:
        split = input("Split? (Yes or No): ").lower().strip()
        if split == "yes":
            return True
        elif split == "no":
            return False
        else:
            print("Invalid input. Please enter yes or no.")

def eval_length(loops) -> int:
    '''Returns the length of the eval line. Needs loops argument for some reason?!?'''
    while loops == 4: #if loops != 4, then it is already finished?
        evallength = int(input("Enter eval line length (34, 29): "))
        if evallength in {34, 29}: # checks evallength's validity: 34 or 29
            return evallength
        else:
            print("Invalid input. Please enter a valid length.")
    return 0

def turn_lengths() -> float:
    '''Gets the turn length from the user.'''
    valid_numbers = {0.95, 0.9, 0.8, 0.7, 0.6}
    while True:
        try:
            length = float(input("Enter turn length: "))
            if length in valid_numbers:
                return length
            else:
                print("Invalid input. Please enter one of the listed turn lengths.")
        except ValueError:
            print("Invalid input. Please enter a valid length.")

def get_turn() -> str:
    '''Gets the turn used from the user.'''
    turns = ["darkseed", "ethereal"]
    while True:
        turn = input("Enter turn used (darkseed or ethereal): ").strip().lower()
        if turn in turns:
            return turn
        else:
            print("Invalid input. Please enter one of the listed turns.")

def rb_time_calc(loadtime: float, loops: int, evallinelength: int, lineamount: int, firstlength: float, firstturn: str, secondlength: float, secondturn: str) -> float:
    '''Calculates the time it takes to rebirth, excluding button presses.'''
    if (firstlength == 0.7 and secondlength == 0.7) or (firstlength + secondlength == 1.8): #this is scuffed af, for some reason this works with .7 but if i do =0.9 it doesnt work, so i do addition and it works????
        raise Exception("Untested, don't use. (Can't use burgor twice)")
    else:
        time = loadtime #time to load in setup

        firstlengthtotime = {
            0.6: {"darkseed": 0.566, "ethereal": 0.633}, 
            0.7: 0.683,
            0.8: {"darkseed": 0.8, "ethereal": 0.73},
            0.9: 0.85, 
            0.95: 0.816
        }
        
        secondlengthtotime = {
            0.6: {"darkseed": 0.533, "ethereal": 0.516},
            0.7: 0.716,
            0.8: 0.666, #dark and eth are the EXACT SAME SPEED for secondlength == 0.8 !
            0.9: 0.85, 
            0.95: 0.816
        }
        
        evaltotime = {
            3: [1.08, 0.86, 1.15], #2 reset longest, which is needed
            4: {29: [0.96, 1.1, 0.85, 1.06], 34: [1.16, 1.25, 0.966, 1.116]}, #3 reset best and longest respectively
            5: [0.933, 0.966, 1.116, 0.85, 1.113] #4 reset 19 (longest)
        }

        for i in range(1, loops+1):
            #this is actually efficient i wana keep myself safe!!!
            
            #time to travel from tp to cannon
            time += 0.75 

            #first turn
            if type(firstlengthtotime[firstlength]) == dict: #checks if firstlength is a special case
                time += firstlengthtotime[firstlength][firstturn]
            else:
                time += firstlengthtotime[firstlength]
            
            #second turn
            if lineamount >= 2:
                if type(secondlengthtotime[secondlength]) == dict: #checks if secondlength is a special case
                    time += secondlengthtotime[secondlength][secondturn]
                else:
                    time += secondlengthtotime[secondlength]

            #eval line
            if type(evaltotime[loops]) == dict: #checks if loops is a special case
                time += evaltotime[loops][evallinelength][i-1]
            else:
                time += evaltotime[loops][i-1]
        
        return time

def main(args: list) -> int:
    '''Main function for the rebirth time calculator.'''
    if is_split():
        loadtime: float = 0.7898 #split time 
    else:
        loadtime: float = 0.864 #time for ore drop @ average 70 ping w/ 3 reset .8 .6 29 eval
    loops: int = int(input("Enter amount of loops (resetters + 1): "))
    lineamount: int = int(input("Enter amount of lines (not counting eval line; 1 or 2 lines): "))
    evallinelength: int = eval_length(loops)
    
    firstlength: float = 0.0
    firstturn: str = ""
    secondlength: float = 0.0
    secondturn: str = ""

    firstlength = turn_lengths()
    if firstlength == 0.8 or firstlength == 0.6:
        firstturn = get_turn()
    
    if lineamount >= 2:
        secondlength = turn_lengths()
        if firstlength == 0.8 or firstlength == 0.6:
            secondturn = get_turn()
    
    time = rb_time_calc(loadtime, loops, evallinelength, lineamount, firstlength, firstturn, secondlength, secondturn)

    print(f"Estimated time: {round(time, 3)}s")
    print(f"Estimated in-game time: {math.floor(time)}s")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

# Credits: stax1547 (discord), agentanti714 (discord)
