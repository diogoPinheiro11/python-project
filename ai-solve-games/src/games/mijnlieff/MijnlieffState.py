from typing import Optional

from games.mijnlieff.MijnlieffAction import MijnlieffAction
from games.mijnlieff.MijnlieffResult import MijnlieffResult
from games.state import State


class MijnlieffState(State):
    EMPTY_CELL = -1

    def __init__(self, rows: int = 5, cols: int = 5):
        super().__init__()

        if rows < 5 or cols < 5:
            raise Exception("the number of rows must be 4 or over")

        """
        the dimensions of the board
        """
        self.__num_rows = rows
        self.__num_cols = cols

        """
        the grid
        """
        self.__grid = [[MijnlieffState.EMPTY_CELL for _i in range(self.__num_cols)] for _j in range(self.__num_rows)]

        """
        counts the number of turns in the current game
        """
        self.__turns_count = 1

        """
        the index of the current acting player
        """
        self.__acting_player = 0

        """
        determine if a winner was found already 
        """
        self.__has_winner = False

    def __check_winner(self, player):
        # check for 4 across
        for row in range(1, self.__num_rows):
            for col in range(1, self.__num_cols - 4):
                if self.__grid[row][col] == player and \
                        self.__grid[row][col + 1] == player and \
                        self.__grid[row][col + 2] == player and \
                        self.__grid[row][col + 3] == player:
                    return True

        # check for 4 up and down
        for row in range(1, self.__num_rows - 4):
            for col in range(1, self.__num_cols):
                if self.__grid[row][col] == player and \
                        self.__grid[row + 1][col] == player and \
                        self.__grid[row + 2][col] == player and \
                        self.__grid[row + 3][col] == player:
                    return True

        # check upward diagonal
        for row in range(1, self.__num_rows):
            for col in range(1, self.__num_cols - 4):
                if self.__grid[row][col] == player and \
                        self.__grid[row - 1][col + 1] == player and \
                        self.__grid[row - 2][col + 2] == player and \
                        self.__grid[row - 3][col + 3] == player:
                    return True

        # check downward diagonal
        for row in range(1, self.__num_rows - 4):
            for col in range(1, self.__num_cols - 4):
                if self.__grid[row][col] == player and \
                        self.__grid[row + 1][col + 1] == player and \
                        self.__grid[row + 2][col + 2] == player and \
                        self.__grid[row + 3][col + 3] == player:
                    return True

        return False

    def get_grid(self):
        return self.__grid

    def get_num_players(self):
        return 2

    def validate_action(self, action: MijnlieffAction) -> bool:
        col = action.get_col()
        row = action.get_row()

        # valid column
        if col < 1 or col >= self.__num_cols:
            return False
        # valid row
        if row < 1 or row >= self.__num_rows:
            return False
        
        # full column
        if self.__grid[row][col] != MijnlieffState.EMPTY_CELL:
            return False

        return True

    def update(self, action: MijnlieffAction):
        col = action.get_col()
        row = action.get_row()

        # drop the checker
        self.__grid[row][col] = self.__acting_player

        # determine if there is a winner
        self.__has_winner = self.__check_winner(self.__acting_player)

        # switch to next player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

        self.__turns_count += 1

    def __display_cell(self, row, col):
        print({
                  0: 'X',
                  1: 'O',
                  MijnlieffState.EMPTY_CELL: ' '
              }[self.__grid[row][col]], end="")

    def __display_numbers(self):
        for col in range(1, self.__num_cols):
            print(' ', end="")
            print(col, end="")
        print("")

    def __display_separator(self):
        for col in range(1, self.__num_cols):
            print("--", end="")
        print("-")

    def display(self):
        self.__display_numbers()
        self.__display_separator()

        for row in range(1, self.__num_rows):
            print(row, end="")
            print('|', end="")
            for col in range(1, self.__num_cols):
                self.__display_cell(row, col)
                print('|', end="")
            print("")
            self.__display_separator()

        self.__display_numbers()
        print("")

    def __is_full(self):
        return self.__turns_count > (self.__num_cols * self.__num_rows)

    def is_finished(self) -> bool:
        return self.__has_winner or self.__is_full()

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned_state = MijnlieffState(self.__num_rows, self.__num_cols)
        cloned_state.__turns_count = self.__turns_count
        cloned_state.__acting_player = self.__acting_player
        cloned_state.__has_winner = self.__has_winner
        for row in range(1, self.__num_rows):
            for col in range(1, self.__num_cols):
                cloned_state.__grid[row][col] = self.__grid[row][col]
        return cloned_state

    def get_result(self, pos) -> Optional[MijnlieffResult]:
        if self.__has_winner:
            return MijnlieffResult.LOOSE if pos == self.__acting_player else MijnlieffResult.WIN
        if self.__is_full():
            return MijnlieffResult.DRAW
        return None

    def get_num_rows(self):
        return self.__num_rows

    def get_num_cols(self):
        return self.__num_cols

    def before_results(self):
        pass

    def get_possible_actions(self):
        grid: list[list[int]] = []
        for i in range(self.get_num_rows()):
            for j in range(self.get_num_cols()):
                grid.append([i, j])

        return list(filter(
            lambda action: self.validate_action(action),
            map(
                lambda pos: MijnlieffAction(pos[0], pos[1]),
                grid))
        )

    def sim_play(self, action):
        new_state = self.clone()
        new_state.play(action)
        return new_state