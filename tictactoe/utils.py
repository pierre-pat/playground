def print_grid(grid):
    print("-"*7)
    for row in grid:
        print(f"|{'|'.join(row)}|")
        print("-"*7)

def is_game_over(grid):
    # check horizontals
    for row in grid:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return True, row[0]

    # check verticals
    for col in range(len(grid[0])):
        if grid[0][col] == grid[1][col] == grid[2][col] != " ":
            return True, grid[0][col]

    # Check diagonals
    if grid[0][0] == grid[1][1] == grid[2][2] != " ":
        return True, grid[0][0]
    if grid[2][0] == grid[1][1] == grid[0][2] != " ":
        return True, grid[2][0]

    # check is full
    all_full = all(cell != " " for row in grid for cell in row)
    if all_full:
        return True, None

    return False, None

def is_valid_move(grid, row, col):
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return False
    return grid[row][col] == " "
