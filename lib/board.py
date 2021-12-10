class Board:
    def __init__(self, cells = [0] * 14, player = 0) -> None:
        self.cells = cells
        self.current_player = player
        self.winner = -1

    def setup(self):
        for i in range(14):
            if i % 7:
                self.cells[i] = 4
            else:
                self.cells[i] = 0

    def getScore(self, player : int) -> int:
        return self.cells[player * 7]

    def play(self, player, index, verbose = False):
        if player == self.current_player:
            if 7 > index >= 1:
                index = player * 7 + index
                if verbose:
                    pass
                    #print(f"playing index {index}")
                if self.cells[index] > 0:
                    self._playRaw(index)
                    if self.checkWin():
                        pass
                        # game ended
                    else:
                        self.current_player = 1 - self.current_player
                else:
                    pass
                    # nothing on that cell, cant play
            else:
                pass
                # invalid index, out of bounds
        else:
            pass
            # not your turn!

    def _playRaw(self, index):
        count = self.cells[index]
        self.cells[index] = 0
        player_bank = self.current_player * 7
        opponent_bank = 7 - player_bank
        while count > 0:
            index -= 1
            index %= 14
            if index == opponent_bank:  # skip opponent score slot
                continue
            self.cells[index] += 1
            count -= 1
        if player_bank < index < player_bank + 7:
            if self.cells[index] == 1:       # final cell was previously empty
                opposite_cell = 14 - index
                if self.cells[opposite_cell] > 0:
                    self.cells[self.current_player * 7] += self.cells[opposite_cell] + 1       # collect own cell and steal from opposing cell
                    self.cells[index] = 0
                    self.cells[opposite_cell] = 0
        elif index == player_bank:                                                  # free move if lands on self bank
            self.current_player = 1 - self.current_player

        sum_player0 = sum(self.cells[1:7])
        sum_player1 = sum(self.cells[8:14])
        if sum_player0 == 0:
            self.cells[8:14] = [0] * 6
            self.cells[7] += sum_player1
        elif sum_player1 == 0:
            self.cells[1:7] = [0] * 6
            self.cells[0] += sum_player0

    def checkWin(self):
        if self.cells[0] > 24:
            self.winner = 0
            return True
        elif self.cells[7] > 24:
            self.winner = 1
            return True
        elif self.cells[0] == 24 and self.cells[7] == 24:
            self.winner = 2                 # tie
            return True

cells = [18, 0, 1, 1, 1, 3, 0, 23, 1, 0, 0, 0, 0, 0]