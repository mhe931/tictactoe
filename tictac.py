import random
from typing import List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TicTacToe:
    def __init__(self):
        # Initialize board with numbers 1-9 instead of spaces
        self.board = [str(i+1) for i in range(9)]
        self.winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        self.position_weights = [
            3, 2, 3,  # Corners and edges weights
            2, 4, 2,  # Center has highest weight
            3, 2, 3
        ]

    def make_move(self, position: int, player: str) -> bool:
        """Make a move on the board."""
        if self.is_valid_move(position):
            self.board[position] = player
            return True
        return False

    def is_valid_move(self, position: int) -> bool:
        """Check if the move is valid."""
        return 0 <= position <= 8 and self.board[position] not in ['X', 'O']

    def get_valid_moves(self) -> List[int]:
        """Get all valid moves."""
        return [i for i, spot in enumerate(self.board) if spot not in ['X', 'O']]

    def is_winner(self, player: str) -> bool:
        """Check if the given player has won."""
        for combo in self.winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False

    def is_board_full(self) -> bool:
        """Check if the board is full."""
        return all(spot in ['X', 'O'] for spot in self.board)

    def evaluate_position(self, depth: int) -> int:
        """Evaluate the current board position."""
        if self.is_winner('O'):  # AI wins
            return 100 + depth
        if self.is_winner('X'):  # Human wins
            return -100 - depth
        if self.is_board_full():
            return 0

        # Position-based evaluation
        score = 0
        for i, mark in enumerate(self.board):
            if mark == 'O':
                score += self.position_weights[i]
            elif mark == 'X':
                score -= self.position_weights[i]
        return score

    def get_winning_move(self, player: str) -> Optional[int]:
        """Check if there's a winning move available."""
        for move in self.get_valid_moves():
            temp = self.board[move]  # Store original value
            self.board[move] = player
            if self.is_winner(player):
                self.board[move] = temp  # Restore original value
                return move
            self.board[move] = temp  # Restore original value
        return None

    def minimax(self, depth: int, alpha: int, beta: int, is_maximizing: bool) -> Tuple[int, Optional[int]]:
        """Minimax algorithm with alpha-beta pruning."""
        # Check for immediate winning moves or blocking moves
        if is_maximizing:
            winning_move = self.get_winning_move('O')
            if winning_move is not None:
                return (100 + depth, winning_move)
        else:
            blocking_move = self.get_winning_move('X')
            if blocking_move is not None:
                return (-100 - depth, blocking_move)

        # Base cases
        if self.is_winner('O'):
            return (100 + depth, None)
        if self.is_winner('X'):
            return (-100 - depth, None)
        if self.is_board_full():
            return (0, None)
        if depth == 0:
            return (self.evaluate_position(depth), None)

        valid_moves = self.get_valid_moves()
        valid_moves.sort(key=lambda x: self.position_weights[x], reverse=is_maximizing)

        best_move = None
        if is_maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                temp = self.board[move]  # Store original value
                self.board[move] = 'O'
                eval_score, _ = self.minimax(depth - 1, alpha, beta, False)
                self.board[move] = temp  # Restore original value
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return (max_eval, best_move)
        else:
            min_eval = float('inf')
            for move in valid_moves:
                temp = self.board[move]  # Store original value
                self.board[move] = 'X'
                eval_score, _ = self.minimax(depth - 1, alpha, beta, True)
                self.board[move] = temp  # Restore original value
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return (min_eval, best_move)

    def get_ai_move(self) -> int:
        """Get the best move for AI."""
        _, best_move = self.minimax(6, float('-inf'), float('inf'), True)
        return best_move

    def display_board(self) -> None:
        """Display the current board state."""
        for i in range(0, 9, 3):
            print(f"{self.board[i]} | {self.board[i+1]} | {self.board[i+2]}")
            if i < 6:
                print("---------")

def play_game():
    """Main game loop."""
    game = TicTacToe()
    print("\nGame starts! Use numbers 1-9 to make your move\n")

    while True:
        game.display_board()

        # Human turn
        while True:
            try:
                move = int(input("\nEnter your move (1-9): ")) - 1
                if game.make_move(move, 'X'):
                    break
                print("Invalid move, try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a number between 1 and 9.")

        if game.is_winner('X'):
            game.display_board()
            print("Congratulations! You win!")
            break
        
        if game.is_board_full():
            game.display_board()
            print("It's a draw!")
            break

        # AI turn
        ai_move = game.get_ai_move()
        game.make_move(ai_move, 'O')
        print(f"\nAI moves to position {ai_move + 1}")

        if game.is_winner('O'):
            game.display_board()
            print("AI wins!")
            print("***************************************************")
            print("***************************************************")
            break
        
        if game.is_board_full():
            game.display_board()
            print("It's a draw!")
            break

if __name__ == "__main__":
    print("Welcome to Tic Tac Toe!")
    print("You are X and the AI is O")
    while True:
        play_game()
        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break
