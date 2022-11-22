import json
import os
from random import randint, choices
from datetime import datetime


class Battleship():
    """Class for simple battleship game."""

    def __init__(self):
        # Variables.
        self.debug = False
        self.turns = 4  # If can change in options, then starting from 3
        self.board_size = 5  # If can change in options, then starting from 3
        self.ships = 1  # Default number of ships is 1.
        self.timestamp = datetime.now(tz=None).isoformat()
        self.stats = self.prepare_statistics()

        # Game board.
        self.board = []

        # Battleship locations on the gameboard.
        self.battleships = []

    def battleship(self):
        """Main method for the game."""
        self.game_begin()
        self.game_actions()

    def game_begin(self):
        """Method for the game's begin."""
        print("Welcome to battleship!")
        games_played = self.stats["games played"]
        if games_played == 0:
            print("This is your first game!")
            self.print_rules()
        else:
            print(f"You have played {games_played} games of battleship so far.")
        self.choose_options()
        self.prepare_board()
        self.create_ships()

    def game_actions(self):
        """Method for hadling the game's actions."""
        hits = 0
        missed_shots = 0
        ships_left = self.ships

        self.print_board(self.board)

        for turn in range(self.turns):
            print(f"This is turn {turn + 1}")

            # Column and row inputs.
            guess_col = self.get_guess("column")
            guess_row = self.get_guess("row")

            # Handle guesses.
            shot_hit = self.check_ship_location(guess_col, guess_row)
            if shot_hit:
                print("Congratulations! You sunk my battleship!")
                self.board[guess_row][guess_col] = "B"
                hits += 1
                ships_left -= 1
                if ships_left < 1:
                    self.print_board(self.board)
                    break
            else:
                if (
                    (guess_row < 0 or guess_row > (self.board_size - 1))
                    or
                    (guess_col < 0 or guess_col > (self.board_size - 1))
                        ):
                    print("Oops, that's not even in the ocean.")
                elif (self.board[guess_row][guess_col] == "X"):
                    print("You guessed that one already.")
                else:
                    print("You missed my battleship!")
                    self.board[guess_row][guess_col] = "X"
                    missed_shots += 1
                if turn == self.turns - 1:
                    print("That was the last guess. Game Over!")

            self.print_board(self.board)

        # Update statistics with played game's events.
        self.stats.update(
            {
                "games played": self.stats["games played"] + 1,
                "hits": self.stats["hits"] + hits,
                "missed shots": self.stats["missed shots"] + missed_shots,
                "latest game": self.timestamp,
                }
            )
        self.write_statistics(self.stats)

        print("Goodbye!")
        return

    # Methods for game setup.
    def prepare_board(self):
        """Method for preparing board for the game."""
        for x in range(self.board_size):
            self.board.append(["O"] * self.board_size)
        return

    def choose_options(self):
        """Method for different options for user."""
        start_game = None
        chosen_option = None
        while start_game is None:
            try:
                print("Choose one of the following options:")
                print("Choose 1 to start new game with 1 boat.")
                print("Choose 2 to start new game with 2 boats.")
                print("Choose 3 to start new game with 3 boats.")
                print("Choose 4 to print the game rules.")
                chosen_option = int(input(f"Choose an option: "))
                if chosen_option in [1, 2, 3]:
                    self.ships = chosen_option
                    # self.board_size += chosen_option
                    # self.turns += chosen_option
                    start_game = True
                elif chosen_option == 4:
                    self.print_rules()
                else:
                    print("Please, choose one of the available options.")
            except ValueError:
                print("Invalid input! Input needs to be a number.")
        return

    def create_ships(self):
        """Method for creating all the ships for the game."""
        for ship in range(self.ships):
            place_taken = True
            while place_taken:
                # Create a ship in random location on board.
                ship_col = self.random_col(self.board)
                ship_row = self.random_row(self.board)
                place_taken = self.check_ship_location(ship_col, ship_row)
            self.battleships.append([ship_col, ship_row])
        if self.debug:
            print(self.battleships)
        return

    def print_rules(self):
        """Method for printing game rules."""
        print("Rules for battleship:")
        print(f"Try to hit the battleship on the board by guessing the right column and row.")
        print(f"You have {self.turns} guesses in total.")
        print("You can choose to have from one to three ships on the board. Try to find all of the ships.")
        print("Good luck!")
        return

    def random_row(self, board):
        return randint(0, len(board) - 1)

    def random_col(self, board):
        return randint(0, len(board[0]) - 1)

    def ship_size(self):
        """Method for returning random size for ship."""
        possible_sizes = [1, 2, 3]
        size = choices(possible_sizes, cum_weights=[5, 7, 8], k=1)  # Relational weights [5, 2, 1]
        return size[0]

    # Methods used during the game.
    def check_ship_location(self, x, y):
        """Method for checking battleship locations."""
        for ship in self.battleships:
            if set([x, y]) == set(ship):
                return True
        return False

    def get_guess(self, guess_type):
        """Method for getting the guess from the user."""
        guess = None
        while guess is None:
            try:
                guess = int(input(f"Guess {guess_type}: "))
                guess -= 1
                # Invert row guesses so the rows go from the bottom to the up.
                inversion_list = [4, 3, 2, 1, 0]
                if guess_type == "row" and guess in inversion_list:
                    guess = inversion_list[guess]
            except ValueError:
                print("Invalid input! Input needs to be a number.")
        return guess

    def print_board(self, board):
        """Method for printing the gameboard."""
        for row in board:
            print(" ".join(row))

    # Statistics methods
    def prepare_statistics(self):
        """Open the statistics file and get the existing data."""
        if os.path.exists("statistics.txt"):
            file = open("statistics.txt", "r")
            stats_json = file.read()
            stats = json.loads(stats_json)
        else:
            # Create a statistics file, if one doesn't exist.
            stats = {
                "games played": 0,
                "hits": 0,
                "missed shots": 0,
                "first game": self.timestamp,
                "latest game": self.timestamp,
            }
            stats_json = json.dumps(stats)
            file = open("statistics.txt", "w")
            file.write(stats_json)
        file.close()
        return stats

    def write_statistics(self, stats):
        """Method for writing statistics into the statistics file."""
        stats_json = json.dumps(stats)
        with open("statistics.txt", "w") as file:
            file.write(stats_json)
        return


if __name__ == '__main__':
    battleship = Battleship()
    game = battleship.battleship()
