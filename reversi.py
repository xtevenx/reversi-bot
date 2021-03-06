"""
Module for move generation in the game Reversi.

Module for move generation in the game Reversi. The algorithm is implemented
quite inefficiently and could be improved.
"""

import numpy

BOARD_SIZE = 8
EMPTY = 2
BLACK = 0
WHITE = 1

a = ord("a")
NOTATION_CHART = {n: chr(n + a) for n in xrange(8)}
COORDINATE_CHART = {chr(n + a): n for n in xrange(8)}

CONVERSION_CHART = {
    0: "X",
    1: "O",
    2: "-"
}

NUMBER_TO_PIECE = {
    2: "  ",
    0: "@@",
    1: "--"
}

STARTING_LEGAL_MOVES = [(2, 3), (3, 2), (4, 5), (5, 4)]
STARTING_LEGAL_MOVES_NOTATION = ['d3', 'c4', 'f5', 'e6']
START_POSITION = numpy.array([
    [2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 1, 0, 2, 2, 2],
    [2, 2, 2, 0, 1, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2],
])

ALLOWED_COORDINATES = frozenset([(x, y) for x in xrange(8) for y in xrange(8)])
ALLOWED_COORDINATES = {x: False for x in ALLOWED_COORDINATES}
NOT_ALLOWED = frozenset([(x, y) for x in [-1, 8] for y in xrange(-1, 9)] +
                        [(x, y) for x in xrange(8) for y in [-1, 8]])
NOT_ALLOWED = {x: True for x in NOT_ALLOWED}
# COORDINATES = ALLOWED_COORDINATES.copy()
# COORDINATES.update(NOT_ALLOWED)

AROUND_FUNCTIONS = [
    lambda x, y: (x - 1, y - 1),
    lambda x, y: (x - 1, y),
    lambda x, y: (x - 1, y + 1),
    lambda x, y: (x, y - 1),
    lambda x, y: (x, y + 1),
    lambda x, y: (x + 1, y - 1),
    lambda x, y: (x + 1, y),
    lambda x, y: (x + 1, y + 1)
]

COORDINATES = {}
for coordinate in ALLOWED_COORDINATES:
    functions = AROUND_FUNCTIONS[:]
    for foo in functions:
        temporary_coordinate = coordinate
        for _ in xrange(2):
            temporary_coordinate = foo(temporary_coordinate[0],
                                       temporary_coordinate[1])
        if max(temporary_coordinate) > 7 or min(temporary_coordinate) < 0:
            functions.remove(foo)
    coordinates = [foo(coordinate[0], coordinate[1]) for foo in functions]
    COORDINATES[coordinate] = coordinates, functions

AVAILABLE_POSITIONS = list(ALLOWED_COORDINATES.keys())
AVAILABLE_POSITIONS.remove((3, 3))
AVAILABLE_POSITIONS.remove((3, 4))
AVAILABLE_POSITIONS.remove((4, 3))
AVAILABLE_POSITIONS.remove((4, 4))


class Board:
    """Board object to represent a position in a game of Reversi."""

    def __init__(self, pieces=None, side=BLACK, copied=False):
        """
        Create piece representations and other needed attributes.

        Create piece representation and determine the legal moves for
        a particular piece representation in 'pieces'. If 'copied' is True,
        don't set the variables because they are expected to be set after
        creation as in the __deepcopy__ function.
        """
        if not copied:
            self.pieces = pieces
            self.side = side
            self.available_positions = AVAILABLE_POSITIONS[:]

            if pieces is None:
                self.pieces = [row[:] for row in START_POSITION]
                self.legal_moves = [move[:] for move in STARTING_LEGAL_MOVES]
                self.legal_moves_notation = STARTING_LEGAL_MOVES_NOTATION[:]
            else:
                self.legal_moves = []
                self.legal_moves_notation = []
                self.update_legal_moves()

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        new_instance = Board(copied=True)
        new_instance.pieces = [row[:] for row in self.pieces]
        new_instance.side = self.side
        new_instance.available_positions = list(self.available_positions)
        new_instance.legal_moves = list(self.legal_moves)
        new_instance.legal_moves_notation = list(self.legal_moves_notation)

        return new_instance

    @staticmethod
    def convert_to_notation(coordinate):
        notation = (NOTATION_CHART[coordinate[1]], coordinate[0] + 1)
        return "".join(map(str, notation))

    @staticmethod
    def convert_to_coordinate(notation):
        return int(notation[1]) - 1, COORDINATE_CHART[notation[0]]

    @staticmethod
    def out_of_bounds(coordinate):
        return coordinate in NOT_ALLOWED

    @staticmethod
    def get_around(coordinate):
        return COORDINATES[coordinate]

    def _legal_position(self, coordinate):
        """
        Finds whether the coordinate is a legal move. Also can be used to
        return the directions in which a move will flip pieces.
        :param coordinate: tuple -> (row, column)
        :return: bool <OR> list
        """

        if self.pieces[coordinate[0]][coordinate[1]] != EMPTY:
            return False

        around, around_functions = self.get_around(coordinate)

        opposite_side = not self.side
        for index, temporary_coordinate in enumerate(around):
            if self.out_of_bounds(temporary_coordinate):
                continue
            if self.pieces[temporary_coordinate[0]][temporary_coordinate[1]] == \
                    opposite_side:
                temporary = around_functions[index](coordinate[0],
                                                    coordinate[1])
                while self.pieces[temporary[0]][temporary[1]] != EMPTY and \
                        not self.out_of_bounds(temporary):
                    if self.pieces[temporary[0]][temporary[1]] == self.side:
                        return True
                    temporary = around_functions[index](
                        temporary[0], temporary[1])

        return False

    def update_legal_moves(self):
        """
        Updates 'self.legal_moves' and 'self.legal_moves_notation'
        :return: None
        """

        self.legal_moves = []

        for coordinate in self.available_positions:
            if self._legal_position(coordinate):
                self.legal_moves.append(coordinate)

        if len(self.legal_moves) is 0:
            self.legal_moves = [None]
            self.legal_moves_notation = [None]
            return

        self.legal_moves_notation = []
        for x in self.legal_moves:
            self.legal_moves_notation.append(self.convert_to_notation(x))

    def _legal_position_directions(self, coordinate):
        """
        Returns the directions in which a move will flip pieces.
        :param coordinate: tuple -> (row, column)
        :return: bool <OR> list
        """

        row, column = coordinate

        if self.pieces[row][column] != EMPTY:
            return False

        around = (
            (row - 1, column - 1),
            (row - 1, column),
            (row - 1, column + 1),
            (row, column - 1),
            (row, column + 1),
            (row + 1, column - 1),
            (row + 1, column),
            (row + 1, column + 1)
        )

        return_value = []
        opposite_side = not self.side
        for index, temporary_coordinate in enumerate(around):
            if self.out_of_bounds(temporary_coordinate):
                continue
            if self.pieces[temporary_coordinate[0]][temporary_coordinate[1]] == opposite_side:
                temporary = coordinate[:]
                while True:
                    temporary = AROUND_FUNCTIONS[index](
                        temporary[0], temporary[1])
                    if self.out_of_bounds(temporary) or \
                            self.pieces[temporary[0]][temporary[1]] == EMPTY:
                        break
                    if self.pieces[temporary[0]][temporary[1]] == self.side:
                        return_value.append(AROUND_FUNCTIONS[index])
                        break
        return return_value

    def _update_board(self, coordinate):
        """
        Updates the board. Called by 'self.move()'
        :param coordinate: coordinate of the move received from 'self.move()'
        :return: None
        """

        directions = self._legal_position_directions(coordinate)
        for direction_function in directions:
            temporary = coordinate[:]
            while True:
                temporary = direction_function(temporary[0], temporary[1])
                if self.out_of_bounds(temporary) or \
                        self.pieces[temporary[0]][temporary[1]] in \
                        (EMPTY, self.side):
                    break
                if self.pieces[temporary[0]][temporary[1]] == (not self.side):
                    self.pieces[temporary[0]][temporary[1]] = self.side

        self.pieces[coordinate[0]][coordinate[1]] = self.side

    def move(self, notation=None, refresh_moves=True):
        """
        Registers a move in the 'notation' format (eg. "4c") or 'None' if there
        is no possible move. Updates the board, legal moves and changes the
        side-to-go accordingly.
        :param notation: str <- move to be made <OR> None
        :param refresh_moves: bool <- whether or not to refresh the legal moves
        :return: None
        """

        # if notation not in self.legal_moves_notation:
        #     return None

        if notation is not None:
            self._update_board(self.convert_to_coordinate(notation))
            self.available_positions.remove(
                self.convert_to_coordinate(notation))

        self.side = int(not self.side)

        if refresh_moves:
            self.update_legal_moves()

    def is_over(self):
        """
        Checks if the game is over.
        :return: bool
        """

        game_over = True

        for _ in xrange(2):
            self.side = int(not self.side)
            self.update_legal_moves()
            if self.legal_moves != [None]:
                game_over = False

        return game_over

    def display(self):
        """
        Displays the current board.
        :return: None
        """

        rows = []
        for index in xrange(len(self.pieces)):
            row = self.pieces[index]
            str_row = map(lambda x: NUMBER_TO_PIECE[x], row)
            rows.append(str(index + 1) + " | " + " | ".join(str_row) + " |\n")

        abc_line = "     a    b    c    d    e    f    g    h  \n"
        separator = "  +--" + "--+--" * 7 + "--+\n"
        print abc_line + separator + separator.join(rows) + separator

    def score(self):
        """
        Displays the current score.
        :return: int <- score
        """

        score = [0, 0]
        for row in self.pieces:
            for piece in row:
                if piece == BLACK:
                    score[0] += 1
                if piece == WHITE:
                    score[1] += 1
        return score

    def get_pieces(self):
        pieces = "".join(CONVERSION_CHART[piece]
                         for row in self.pieces for piece in row)
        return pieces + CONVERSION_CHART[self.side]


if __name__ == "__main__":
    b = Board()
    b.display()
