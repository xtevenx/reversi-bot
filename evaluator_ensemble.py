"""
File: evaluator_nn.py -- version 0.1.1

Description: This evaluation module uses a pre-trained neural network.
"""


import cPickle
import numpy

from math import log

INSTANCE_FILES = ["network.pkl", "network_test.pkl"]
LOOK_NICE = False

NETWORKS = []
for network_file in INSTANCE_FILES:
    f = open(network_file, "r")
    NETWORKS.append(cPickle.load(f))
    f.close()


def convert_to_input(board):
    pieces = board.pieces
    converted = []
    for row in pieces:
        for piece in row:
            if piece == 0:
                converted += [1, 0]
            elif piece == 1:
                converted += [0, 1]
            else:
                converted += [0, 0]

    if board.side == 0:
        converted.append(0)
    else:
        converted.append(1)

    return converted


def draw_function(t):
    return t / 50.0


def evaluate(board):
    if board.is_over():
        score = board.score()
        return 100 * (score[0] - score[1])

    if LOOK_NICE:
        pieces = board.pieces
        empty_places = 0
        for row_index in xrange(len(pieces)):
            for column_index in xrange(len(pieces[row_index])):
                if pieces[row_index][column_index] == 2:
                    empty_places += 1
        look_nice_factor = draw_function(60 - empty_places)
    else:
        look_nice_factor = 1


    inputs = numpy.array([convert_to_input(board)])
    output = 0
    for network in NETWORKS:
        temp = network.think(inputs)
        output += -100 * numpy.log(1 / temp - 1 + 10 ** -8)  # Convert to pieces.
    output /= len(NETWORKS)

    return look_nice_factor * output

