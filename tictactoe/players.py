from abc import ABC, abstractmethod

from .utils import print_grid
from .utils import is_game_over

class Player(ABC):
    def __init__(self, sign):
        self.sign = sign

    @abstractmethod
    def get_move(self, grid) -> tuple[int, int, str]:
        pass

class HumanPlayer(Player):

    def get_move(self, grid) -> tuple[int, int, str]:
        print_grid(grid)
        move = input("Enter the move [row,col] range 0-2, i.e. 2,1: ")
        row, col = move.strip().split(",")
        row, col = row.strip(), col.strip()
        return int(row), int(col), self.sign

class MinimaxPlayer(Player):

    def __init__(self, sign):
        super().__init__(sign)
        self.opponent = "X" if self.sign == "O" else "O"

    def get_move(self, grid) -> tuple[int, int, str]:
        best_move = (-1, -1)
        best_score = -float("inf")
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == " ":
                    grid[i][j] = self.sign
                    score = self._minimax(grid, maximize=False)
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
                    grid[i][j] = " "

        return best_move[0], best_move[1], self.sign

    def _minimax(self, grid, maximize=True) -> int | float:
        is_over, winner = is_game_over(grid)
        if is_over:
            if winner == self.sign: return 10
            if winner == self.opponent: return -10
            return 0

        if maximize:
            best_score = -float("inf")

            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == " ":
                        grid[i][j] = self.sign
                        score = self._minimax(grid, maximize=False)
                        grid[i][j] = " "
                        if score > best_score:
                            best_score = score
        else:
            best_score = float("inf")
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == " ":
                        grid[i][j] = self.opponent
                        score = self._minimax(grid, maximize=True)
                        grid[i][j] = " "
                        if score < best_score:
                            best_score = score
        return best_score
