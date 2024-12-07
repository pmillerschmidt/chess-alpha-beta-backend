import contextlib
from random_agent import RandomAgent
from greedy_agent import GreedyAgent
from minimax_agent import MinimaxAgent
from scout_agent import ScoutAgent
with contextlib.redirect_stdout(None):
    import chess
    import chess.polyglot
    from chessboard import display


class Driver():

    def compare_policies(self, P1, P2, simulations, visualize):
        """
        Function to compare the outcome of a game between different policies
        """
        white_wins = draws = black_wins = 0
        for i in range(simulations):
            result = self.play_game_with_viz(P1, P2) if visualize else self.play_game(P1, P2)
            print(f"{int(100 * (i + 1) / simulations)}% done")
            if result.winner == True: white_wins += 1
            elif result.winner == False: black_wins += 1
            else: draws += 1

        return (white_wins, draws, black_wins)  

    def play_game(self, P1, P2):
        """
        Function to make turns for each respective player while the game is active
        """
        board = chess.Board()

        while not board.is_game_over():
            P1.play(board) if board.turn == P1.color else P2.play(board)

        result = board.outcome()
        return result
    
    def play_game_with_viz(self, P1, P2):
        """
        Function to make turns for each respective player while the game is active
        """
        game_board = display.start()
        board = chess.Board()

        while not board.is_game_over() and not display.check_for_quit():
            P1.play(board) if board.turn == P1.color else P2.play(board)
            display.update(board.fen(), game_board)

        display.update(board.fen(), game_board)
        result = board.outcome()
        return result
