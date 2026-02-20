from itertools import cycle

from .players import HumanPlayer, MinimaxPlayer
from .utils import is_valid_move, is_game_over, print_grid

class TTT:
    def __init__(self, p1, p2):
        self.grid = [[" " for _ in range(3)] for __ in range(3)]
        self.player = cycle([p1, p2])

    def run(self):
        game_over = False
        player_sign = None

        while not game_over:
            valid_move = False
            while not valid_move:
                player = next(self.player)
                row, col, sign = player.get_move(self.grid)
                valid_move = is_valid_move(self.grid, row, col)
                if valid_move:
                    self.grid[row][col] = sign
                else:
                    print("Invalid mode, try again.")

            game_over, player_sign = is_game_over(self.grid)

        print_grid(self.grid)
        if player_sign:
            print(f"Player {player_sign} won!")
        else:
            print("It's a draw!")

if __name__ == "__main__":
    game = TTT(HumanPlayer("O"), MinimaxPlayer("X"))
    game.run()
