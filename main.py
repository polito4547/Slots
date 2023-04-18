import random
import pickle
import os

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3


symbol_count = {
    "A": 3,
    "B": 6,
    "C": 9,
    "D": 12
}


symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance


def save_player(player):
    with open("player_data.pickle", "wb") as f:
        pickle.dump(player, f)
        f.close()


def load_player():
    with open("player_data.pickle", "rb") as f:
        player = pickle.load(f)
    
    return player


def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []

    for line in range(lines):
        symbol = columns[0][line]

        for column in columns:
            symbol_to_check = column[line]

            if symbol != symbol_to_check:
                break

            else:
                winnings += values[symbol] * bet
                winning_lines.append(lines + 1)
    return winnings, winning_lines


def get_slot_machine_spim(rows, cols, symbols):
    all_symbols = []

    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns =[]

    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]

        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns


def print_slot_maching(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], "|", end=" | ")
            else:
                print(column[row], end="")

        print()


def deposit():
    while True:
        amount = input("How much would you like to deposit? $")

        if amount.isdigit():
            amount = int(amount)

            if amount >= 0:
                break
                
            else:
                print("Amount must be at least 0.")

        else:
            print("Please enter a number.")
    
    return amount


def get_number_of_lines():
    while True:
        lines = input("Enter the number of lines on (1- " + str(MAX_LINES) + ")? ")

        if lines.isdigit():
            lines = int(lines)

            if 1 <= lines <= MAX_LINES:
                break
                
            else:
                print("Enter a valid number of lines.")

        else:
            print("Please enter a number.")
    
    return lines    


def get_bet():
    while True:
        bet_amount = input("How much would you like to bet on each line? (Press [D] to deposit more money) $")

        if bet_amount.isdigit():
            bet_amount = int(bet_amount)

            if bet_amount > 0:
                break
                
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}")

        elif bet_amount.lower() == "d":
            deposit()
        
        else:
            print("Please input a valid option.")
    
    return bet_amount    


def spin(balance):
    lines = get_number_of_lines()
    
    while True:
        bet = get_bet()
        total_bet = lines * bet

        if total_bet > balance:
            print(f"You do not have enough money to bet that amount. Please specify a different amount.")
        
        else: break

    print(f"You are betting ${bet} on {lines}. Total bet is equal to : ${total_bet}")

    slots = get_slot_machine_spim(ROWS, COLS, symbol_count)
    print_slot_maching(slots)

    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won {winnings}")
    print(f"You won on", *winning_lines)

    return winnings - total_bet


def Game():
    answer = 0
    play_again = 'y'

    if os.path.exists("player_data.pickle"):
        saved_player = load_player()
    
    else:
        print("Creating new player profile:")
        name = input("Please Enter Your Name: ")
        balance = deposit()
        player = Player(name, balance)
        save_player(player)
        saved_player = load_player()

    

    print(f"Current Name: {saved_player.name}")
    print(f"Current Balance: ${saved_player.balance}")


    while answer not in (1, 2):

        print(f"Current balance is ${saved_player.balance}")

        try:
            answer = int(input("Press [1] To Play.\nPress [2] to Quit: "))
        except ValueError:
            print ("Please use [1] or [2] as your response")
            answer = 0
        
        if answer == 2:
            quit()
        elif answer == 1:
            saved_player.balance += spin(saved_player.balance)
            print(f"Your final balance is ${saved_player.balance}")

        
        play_again = None

        while play_again not in('y', 'n'):
            play_again = input("Would you like to play again? Y/N?")

            if play_again.lower() == "y":
                save_player(saved_player)
                Game()
            elif play_again.lower() == "n":
                save_player(saved_player)
                quit()
            else:
                print("Invalid input. Please enter [Y] or [N].")


if __name__ == '__main__':
    try:
        while True:
            Game()
    except:
        quit()