import pygame, sys
from pygame.locals import *

import random


def getRandomizedBoard():
    # Define the number of pairs of cards
    num_pairs = 8  # 8 pairs means 16 cards in total
    board = list(range(1, num_pairs + 1)) * 2  # Each number appears twice

    # Shuffle the board to randomize the positions
    random.shuffle(board)

    # Create a 4x4 grid (Board with 4 rows and 4 columns)
    randomized_board = []
    for i in range(4):
        randomized_board.append(board[i * 4:(i + 1) * 4])  # Fill each row with 4 elements

    return randomized_board


# Example output
mainBoard = getRandomizedBoard()
print(mainBoard)