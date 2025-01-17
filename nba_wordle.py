from random import randint

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_instructions():
    print(f"\n{bcolors.HEADER}=== NBA PLAYER GUESSING GAME ==={bcolors.ENDC}")
    print("\nTry to guess the NBA player in 6 attempts!")
    print("\nAfter each guess, you'll get feedback on five attributes:")
    print("- Name")
    print("- Team")
    print("- Position")
    print("- Height")
    print("- Weight")
    
    print(f"\n{bcolors.BOLD}Color Coding:{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}Green{bcolors.ENDC}: Exact match")
    print(f"{bcolors.WARNING}Yellow{bcolors.ENDC}: Close match")
    print("No color: Not a match")
    
    print(f"\n{bcolors.BOLD}Feedback Guide:{bcolors.ENDC}")
    print("Position:")
    print(f"- {bcolors.OKGREEN}Green{bcolors.ENDC}: Same position (e.g., both PG)")
    print(f"- {bcolors.WARNING}Yellow{bcolors.ENDC}: Similar position (PG/SG or SF/PF)")
    
    print("\nHeight:")
    print(f"- {bcolors.OKGREEN}Green{bcolors.ENDC}: Exact same height")
    print(f"- {bcolors.WARNING}Yellow{bcolors.ENDC}: Within 2 inches")
    
    print("\nWeight:")
    print(f"- {bcolors.OKGREEN}Green{bcolors.ENDC}: Exact same weight")
    print(f"- {bcolors.WARNING}Yellow{bcolors.ENDC}: Within 15 pounds")
    
    print("\nPress Enter to start the game...")
    input()

maxTries = 6
players = []

# Display instructions at start
print_instructions()

with open('players.txt') as f:
    for line in f:
        name, team, position, height, weight = line.strip().split(',')
        players.append({
            'name': name,
            'team': team,
            'position': position,
            'height': height,
            'weight': int(weight)
        })

target = players[randint(0, len(players)-1)]
# if __debug__:
#     print('debug:', target['name'])

def compare_attributes(guess_attr, target_attr, attr_type):
    if guess_attr == target_attr:
        return bcolors.OKGREEN + str(guess_attr) + bcolors.ENDC
    
    if attr_type == 'weight':
        diff = abs(int(guess_attr) - int(target_attr))
        if diff <= 15:
            return bcolors.WARNING + str(guess_attr) + bcolors.ENDC
    elif attr_type == 'height':
        def height_to_inches(h):
            ft, inch = map(int, h.split('-'))
            return ft * 12 + inch
        diff = abs(height_to_inches(guess_attr) - height_to_inches(target_attr))
        if diff <= 2:
            return bcolors.WARNING + str(guess_attr) + bcolors.ENDC
    elif attr_type == 'position':
        guards = ['PG', 'SG']
        forwards = ['SF', 'PF']
        if (guess_attr in guards and target_attr in guards) or \
           (guess_attr in forwards and target_attr in forwards):
            return bcolors.WARNING + str(guess_attr) + bcolors.ENDC
    
    return str(guess_attr)

t = 0
while t < maxTries:
    guess_name = input("\nEnter player name: ")
    guess = None
    
    for player in players:
        if player['name'].lower() == guess_name.lower():
            guess = player
            break
    
    if not guess:
        print("Invalid player name. Try again.")
        continue

    print(f"Name: {'✓' if guess['name'] == target['name'] else '✗'}")
    print(f"Team: {compare_attributes(guess['team'], target['team'], 'team')}")
    print(f"Position: {compare_attributes(guess['position'], target['position'], 'position')}")
    print(f"Height: {compare_attributes(guess['height'], target['height'], 'height')}")
    print(f"Weight: {compare_attributes(guess['weight'], target['weight'], 'weight')}")

    if guess['name'] == target['name']:
        print(f"\n{bcolors.OKGREEN}Congratulations! You guessed the player correctly!{bcolors.ENDC}")
        break
    
    t += 1
    print(f"Attempts remaining: {maxTries - t}")
else:
    print(f"\n{bcolors.FAIL}Game Over! The player was {target['name']}{bcolors.ENDC}")