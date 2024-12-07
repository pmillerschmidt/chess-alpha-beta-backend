import chess
import random

class GreedyAgent():
    def __init__(self, color, ob):
        self.color = color
        self.opening_book = chess.polyglot.open_reader(ob)

    def material_gained(self, board, move):
        """
        Function to determine the material gained from a given move
        Citation: https://stackoverflow.com/questions/61778579/what-is-the-best-way-to-find-out-if-the-move-captured-a-piece-in-python-chess
        """
        if board.is_capture(move):
            if board.is_en_passant(move):
                return chess.PAWN
            else:
                return board.piece_at(move.to_square).piece_type
        return 0

    def play(self, board):
        """
        Driver function to determine and make the best move
        """
        legal_moves = list(board.legal_moves)
        max_material = 0
        best_move = None

        if self.opening_book.get(board) != None:
            best_move = self.opening_book.weighted_choice(board).move

        else:
            # go through moves, choose one with the most material gain
            for move in legal_moves:
                if self.material_gained(board, move) > max_material:
                    max_material = self.material_gained(board, move)
                    best_move = move

            # if no move is best, random choice
            if max_material == 0:
                best_move = random.choice(legal_moves)

        board.push(best_move)
