import chess
import chess.polyglot
import PSE

class ScoutAgent():
    
    def __init__(self, color, depth, ob):
        self.color = color
        self.depth = depth
        self.opening_book = chess.polyglot.open_reader(ob)

    def material_count(self, board):
        """
        Function that calculates the material count of the board 
        """
        count = 0
        pieces = [(1, chess.PAWN), (3.1, chess.KNIGHT),
                  (3.2, chess.BISHOP), (4.5, chess.ROOK), (9, chess.QUEEN)]

        for piece in pieces:
            count += piece[0] * len(board.pieces(piece[1], chess.WHITE))
            count += piece[0] * len(board.pieces(piece[1], chess.BLACK))

        return count

    def material_balance(self, board):
        """
        Function that calculates the material balance of the board (white pieces - black pieces)
        """
        w_balance, b_balance = 0, 0
        pieces = [(1, chess.PAWN), (3.1, chess.KNIGHT),
                  (3.2, chess.BISHOP), (4.5, chess.ROOK), (9, chess.QUEEN)]

        for piece in pieces:
            w_balance += piece[0] * len(board.pieces(piece[1], chess.WHITE))
            b_balance += piece[0] * len(board.pieces(piece[1], chess.BLACK))

        balance = w_balance - b_balance
        return balance

    def piece_square_evaluation(self, board, player):
        """
        Function that evaluates the positional strength of a player's pieces
        """
        evaluation = 0

        for piece in board.pieces(chess.PAWN, player):
            evaluation = evaluation + PSE.W_PAWN[piece] if player == chess.WHITE else evaluation - PSE.B_PAWN[piece]
        for piece in board.pieces(chess.KNIGHT, player):
            evaluation = evaluation + PSE.W_KNIGHT[piece] if player == chess.WHITE else evaluation - PSE.B_KNIGHT[piece]
        for piece in board.pieces(chess.BISHOP, player):
            evaluation = evaluation + PSE.W_BISHOP[piece] if player == chess.WHITE else evaluation - PSE.B_BISHOP[piece]
        for piece in board.pieces(chess.QUEEN, player):
            evaluation = evaluation + PSE.W_QUEEN[piece] if player == chess.WHITE else evaluation - PSE.B_QUEEN[piece]
        for piece in board.pieces(chess.KING, player):
            evaluation = evaluation + PSE.W_KING[piece] if player == chess.WHITE else evaluation - PSE.B_KING[piece]

        return evaluation / 1000

    def heuristic(self, board, player):
        """
        Heuristic function to determine the value of a given board position
        """
        # coefficients for material balance & piece-square evaluation
        mbc = 1
        psec = 6
        
        if board.is_checkmate():
            reward = 500 if player == chess.BLACK else -500
        elif board.is_stalemate() or board.is_insufficient_material() or board.is_fivefold_repetition():
            reward = 0
        else:
            reward = mbc * self.material_balance(board) + psec * self.piece_square_evaluation(board, player)

        return reward

    def order_moves(self, board, player):
        """
        Function to order the legal moves from best to worst according to material strength
        """
        result = []
        legal_moves = list(board.legal_moves)
        for move in legal_moves:
            board.push(move)
            score = self.material_balance(board)
            result.append((move, score))
            board.pop()
        
        if player == chess.WHITE:
            result.sort(key = lambda x: x[1], reverse = True)
        else:
            result.sort(key = lambda x: x[1])
        return result

    def scout(self, board, player, depth, alpha, beta):
        """
        Scout (principal variation search) algorithm
        """
        if depth == 0 or board.is_game_over():
            return (None, self.heuristic(board, player))

        ordered_moves = self.order_moves(board, player)
        next_player = chess.BLACK if player == chess.WHITE else chess.WHITE

        best_score = float('-inf') if player == chess.WHITE else float('inf')
        best_move = None

        for move, heuristic in ordered_moves:
            board.push(move)
            if best_move == None:
                score = self.scout(board, next_player, depth - 1, alpha, beta)
            else:
                if alpha != float('-inf'):
                    score = self.scout(board, next_player, depth - 1, alpha, alpha + 1)
                elif beta != float('inf'):
                    score = self.scout(board, next_player, depth - 1, beta - 1, beta)
                if alpha < score[1] < beta:
                    score = self.scout(board, next_player, depth - 1, score[1], beta)
            board.pop()

            if player == chess.WHITE:
                if score[1] > best_score:
                    best_score = score[1]
                    best_move = move
                    alpha = max(alpha, score[1])
            
            elif player == chess.BLACK:
                if score[1] < best_score:
                    best_score = score[1]
                    best_move = move
                    beta = min(beta, score[1])

            if beta <= alpha:
                break

        return (best_move, best_score)

    def play(self, board):
        """
        Driver function to determine and make the best move
        """
        if self.opening_book.get(board) != None:
            move = self.opening_book.weighted_choice(board).move
        elif self.material_count(board) < 15:
            move = self.scout(board, self.color, self.depth + 2, float('-inf'), float('inf'))[0]
        else: 
            move = self.scout(board, self.color, self.depth, float('-inf'), float('inf'))[0]
        
        board.push(move)
