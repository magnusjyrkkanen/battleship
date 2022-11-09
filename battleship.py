import json
import os
from random import randint
from datetime import datetime


class Battleship():
    """Class for simple battleship game."""

    def __init__(self):
        # Variables.
        self.turns = 4
        self.timestamp = datetime.now(tz=None).isoformat()

        print("Welcome to battleship!")

        self.stats = self.prepare_statistics()
        games_played = self.stats["games played"]
        if games_played == 0:
            print("This is your first game!")
        else:
            print(f"You have played {games_played} games of battleship so far.")

        print("Rules for battleship:")
        print(f"Try to hit the battleship by guessing the right row and column. You have {self.turns} guesses.")

        # Game board.
        self.board = []

        # Prepare board for the game.
        for x in range(5):
            self.board.append(["O"] * 5)

        # Create a ship in random location on board.
        self.ship_row = self.random_row(self.board)
        self.ship_col = self.random_col(self.board)
        # Debug prints
        # print(f"Ship row {ship_row}")
        # print(f"Ship col {ship_col}")

    def battleship(self):
        # Main method for the game.
        hits = 0
        missed_shots = 0

        self.print_board(self.board)

        for turn in range(self.turns):
            print(f"Turn {turn + 1}")

            # Row and column inputs.
            guess_row = None
            guess_col = None
            while guess_row is None:
                try:
                    guess_row = int(input("Guess row: "))
                    guess_row -= 1
                except ValueError:
                    print("Invalid input! Input needs to be a number.")
            while guess_col is None:
                try:
                    guess_col = int(input("Guess column: "))
                    guess_col -= 1
                except ValueError:
                    print("Invalid input! Input needs to be a number.")

            # Handle guesses.
            if guess_row == self.ship_row and guess_col == self.ship_col:
                print("Congratulations! You sunk my battleship!")
                self.board[guess_row][guess_col] = "B"
                self.print_board(self.board)
                hits += 1
                break
            else:
                if (guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4):
                    print("Oops, that's not even in the ocean.")
                elif(self.board[guess_row][guess_col] == "X"):
                    print("You guessed that one already.")
                else:
                    print("You missed my battleship!")
                    self.board[guess_row][guess_col] = "X"
                    missed_shots += 1
                if turn == 3:
                    print("That was the last guess. Game Over!")

            self.print_board(self.board)

        # Update the games played statistic.
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

    def print_board(self, board):
        for row in board:
            print(" ".join(row))

    def random_row(self, board):
        return randint(0, len(board) - 1)

    def random_col(self, board):
        return randint(0, len(board[0]) - 1)

    def prepare_statistics(self):
        # Open the statistics file and get the existing data.
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
        stats_json = json.dumps(stats)
        with open("statistics.txt", "w") as file:
            file.write(stats_json)
        return


if __name__ == '__main__':
    battleship = Battleship()
    game = battleship.battleship()
