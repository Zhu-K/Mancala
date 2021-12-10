import lib.board as board

sym = {
    'TL' : '╔',
    'TR' : '╗',
    'BL' : '╚',
    'BR' : '╝',
    'H'  : '═',
    'V'  : '║',
    'LT' : '╠',
    'RT' : '╣',
    'TT' : '╦',
    'BT' : '╩',
    'X'  : '╬',
}

class Game(board.Board):
    def __init__(self, player = 0) -> None:
        super().__init__()
        self.current_player = player
        self.table_width = 0
        self.setup()

    def fillCell(self, num, width):
        padding = ' ' * (width // 2 - 1)
        if num >= 10:
            extra = ''
        else:
            extra = ' '
        return padding + extra + str(num) + padding

    def draw(self):
        cell_w = 4
        self.table_width = 8 * (cell_w + 1) + 1
        # player 0 index
        if self.current_player:
            drawing = " \n"
        else:
            drawing = ' ' * (2 + int(1.5 * cell_w)) + ''.join([str(i) + ' ' * cell_w for i in range(1, 7)]) + '\n'
        # first row
        drawing += sym['TL'] + (sym['H'] * cell_w + sym['TT']) * 7 + sym['H'] * cell_w + sym['TR'] + '\n'
        # second row
        for i in range(7):
            drawing += sym['V'] + self.fillCell(self.cells[i], cell_w)
        drawing += sym['V'] + ' ' * cell_w + sym['V'] + '\n'
        # third row
        drawing += sym['V'] + ' ' * cell_w + sym['LT'] + (sym['H'] * cell_w + sym['X']) * 5 + sym['H'] * cell_w + sym['RT'] + ' ' * cell_w + sym['V'] + '\n'
        # fourth row
        drawing += sym['V'] + ' ' * cell_w
        for i in range(13, 6, -1):
            drawing += sym['V'] + self.fillCell(self.cells[i], cell_w)
        drawing += sym['V'] + '\n'
        # fifth line
        drawing += sym['BL'] + (sym['H'] * cell_w + sym['BT']) * 7 + sym['H'] * cell_w + sym['BR'] + '\n'
        # player 1 index
        if not self.current_player:
            drawing += " \n"
        else:
            drawing += ' ' * (2 + int(1.5 * cell_w)) + ''.join([str(i) + ' ' * cell_w for i in range(6, 0, -1)]) + '\n'
        return drawing