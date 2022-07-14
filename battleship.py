from random import randint


class Battleship():
    """Class for simple battleship game."""

    def __init__(self):
        print("Welcome to battleship!")

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
        # Main method.

        self.print_board(self.board)

        for turn in range(4):
            print(f"Turn {turn + 1}")

            # Row and column inputs.
            guess_row = None
            guess_col = None
            while guess_row is None:
                try:
                    guess_row = int(input("Guess row: "))
                except ValueError:
                    print("Invalid input! Input needs to be a number.")
            while guess_col is None:
                try:
                    guess_col = int(input("Guess column: "))
                except ValueError:
                    print("Invalid input! Input needs to be a number.")

            # Handle guesses.
            if guess_row == self.ship_row and guess_col == self.ship_col:
                print("Congratulations! You sunk my battleship!")
                self.board[guess_row][guess_col] = "B"
                self.print_board(self.board)
                break
            else:
                if (guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4):
                    print("Oops, that's not even in the ocean.")
                elif(self.board[guess_row][guess_col] == "X"):
                    print("You guessed that one already.")
                else:
                    print("You missed my battleship!")
                    self.board[guess_row][guess_col] = "X"
                if turn == 3:
                    print("Game Over")

            self.print_board(self.board)

    def print_board(self, board):
        for row in board:
            print(" ".join(row))

    def random_row(self, board):
        return randint(0, len(board) - 1)

    def random_col(self, board):
        return randint(0, len(board[0]) - 1)


if __name__ == '__main__':
    battleship = Battleship()
    game = battleship.battleship()
