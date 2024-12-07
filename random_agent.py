import chess
import random

class RandomAgent():
    def __init__(self, color):
        self.color = color

    def play(self, board):
        """
        Driver function to determine and make the best move
        """
        legal_moves = list(board.legal_moves)
        move = random.choice(legal_moves)
        board.push(move)
