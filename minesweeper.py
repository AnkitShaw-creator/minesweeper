import random as r
import re

class Board():
    def __init__(self, dim_size, bombs):
        self.dim_size = dim_size # dimensions of the board
        self.bombs = bombs # no. of boards to be  planted in the bombs
        
        self.board = self.make_new_board()
        self.assign_values_to_board()
        self.dug = set() # a set to keep track of the places that the user have dug

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombsPlanted = 0
        while bombsPlanted < self.bombs:
            loc = r.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size   
            column = loc % self.dim_size

            if board[row][column] == '*':
                continue # if bomb is already planted in that location

            board[row][column] = '*'
            bombsPlanted += 1
            
        return board

    def assign_values_to_board(self):
        # assigns values to empty spaces
        # represents the no of neighbouring bombs
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue # if there is a bomb already been planted, we should skip to next position
                self.board[r][c] = self.get_nums_neighbouring_bombs(r,c)

    def get_nums_neighbouring_bombs(self, row, col):
        # we need to check the neighbouring cells for bombs and then increment the values of the current cell accordingly
        # we only need to check at the vicinity of the current cell in order increment the cell

        num_neighbouring_bombs = 0 # initializing the counter
        for r in range(max(0, row-1), min(self.dim_size-1, (row+1)+1)):
            for c in range(max(0, col-1), min(self.dim_size-1, (col+1)+1)):
                if r == row and c == col:
                    continue # means that we are in the current location where we need to increment it

                if self.board[r][c]=='*':
                    num_neighbouring_bombs += 1
            
        return num_neighbouring_bombs

    def dig(self, row, col):
        # if the dig was successful return True, else if we dig a bomb return false(game over)
        # following case should be consider:
        # case 1. if we hit a bomb, its game over
        # case 2. if we dig at place near a bomb, finish dig
        # case 3. if none of the above, keep digging
        self.dug.add((row,col))
        if self.board[row][col]=='*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row-1), min(self.dim_size-1, (row+1)+1)):
            for c in range(max(0, col-1), min(self.dim_size-1, (col+1)+1)):
                if (r, c) in self.dug:
                    continue  # if the spot is already dig, don't dig again
                self.dig(r,c)
        
        return True

    def __str__(self):
        visible_board =  [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if (r,c) in self.dug:
                    visible_board[r][c] =  str(self.board[r][c])
                else:
                    visible_board[r][c] =' '

        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep
    
safe = True

def game(board_size = 10, bombs = 10):
    board = Board(board_size, bombs)

    while len(board.dug) < board_size**2 - bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig next? Input as row,column: "))
        row, col = int(user_input[0]), int(user_input[-1])

        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print("Invalid input, please try again")
            continue

        safe = board.dig(row, col) # to check whether we dug a bomb

        if not safe:
            break  # if we hit a bomb, its game over

    if safe:
        print("Congratulations!!! You won")
    else:
        print("Sorry! You dug a bomb and died in explosion")
        # now we must print the entire board for user
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)


if __name__ == '__main__':
    game()