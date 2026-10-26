import math
import time

class MathDuel:
    def __init__(self, start_number=16, allowed_moves=None):
        if allowed_moves is None:
            allowed_moves = [1, 2, 3]
        self.start_number = start_number
        self.allowed_moves = allowed_moves
        self.current_number = start_number
        self.player_turn = 1  # Player 1 starts (MAX)
        self.game_over = False
        self.winner = None
        self.move_history = []

    def reset(self):
        """Reset the game state."""
        self.current_number = self.start_number
        self.player_turn = 1
        self.game_over = False
        self.winner = None
        self.move_history = []

    def make_move(self, move):
        """Implements making a move.
        - Subtract `move` from current_number
        - Check if the game is over
        - Switch turns
        """
        if move not in self.allowed_moves or move > self.current_number or self.game_over: # check if the move is valid or not
            return False  # Invalid move
        self.current_number -= move # subtract the move from the current number
        self.move_history.append((self.player_turn, move))
        if self.current_number == 0: # if the current number is 0, the game is over
            self.game_over = True # if the current number is 0, the game is over
            self.winner = self.player_turn # the winner is the player who made the last move
        else:
            self.player_turn = 2 if self.player_turn == 1 else 1 # switch turns
        return True # return True if the move is valid

    def evaluate(self):
        """Evaluates the game state.
        Return:
          +1 if MAX wins
          -1 if MIN wins
           0 if game not over
        """
        if not self.game_over: # if the game is not over, return 0
            return 0
        # The player who just played is the winner
        if self.winner == 1: # if the winner is 1, return 1
            return 1  # MAX wins
        elif self.winner == 2: # if the winner is 2, return -1
            return -1  # MIN wins
        return 0 # return 0 if the game is not over

    def minimax(self, state, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
        """Minimax with alpha-beta pruning."""
        if state == 0:
            # If state is 0, the previous player won
            return -1 if is_maximizing else 1
        if depth == 0:
            return 0  # Optionally, treat as draw/unknown
        if is_maximizing:
            max_eval = -math.inf
            for move in self.allowed_moves:
                if move > state:
                    continue
                eval = self.minimax(state - move, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = math.inf
            for move in self.allowed_moves:
                if move > state:
                    continue
                eval = self.minimax(state - move, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval

    def get_best_move(self):
        """Use minimax to find the best move for the current player."""
        best_move = None # initialize the best move to None
        if self.player_turn == 1: # if the player is 1, return the best move for the player
            best_eval = -math.inf # initialize the best evaluation to -infinity
            for move in self.allowed_moves:
                if move > self.current_number: # if the move is greater than the current number, continue
                    continue
                eval = self.minimax(self.current_number - move, 100, False)
                if eval > best_eval: # if the evaluation is greater than the best evaluation, update the best evaluation and the best move
                    best_eval = eval # update the best evaluation
                    best_move = move # update the best move
        else: # if the player is 2, return the best move for the player
            best_eval = math.inf
            for move in self.allowed_moves:
                if move > self.current_number: # if the move is greater than the current number, continue
                    continue
                eval = self.minimax(self.current_number - move, 100, True)
                if eval < best_eval: # if the evaluation is less than the best evaluation, update the best evaluation and the best move
                    best_eval = eval # update the best evaluation
                    best_move = move    
        return best_move

    def print_game_state(self):
        """Print the current state of the game."""
        player_name = "Player 1" if self.player_turn == 1 else "AI"
        role = "MAX" if self.player_turn == 1 else "MIN"
        print(f"\nCurrent number: {self.current_number}")
        print(f"{player_name}'s turn ({role})")
        print(f"Allowed moves: {[m for m in self.allowed_moves if m <= self.current_number]}")
        if self.game_over:
            print(f"Game over! {player_name} wins!")

