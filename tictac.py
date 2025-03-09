import random
from typing import List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TicTacToe:
    def __init__(self):
        # Initialize board with numbers 1-9 for easy position reference
        self.board = [str(i+1) for i in range(9)]
        
        # Define all possible winning combinations on the board
        # Each sublist represents positions that form a win if filled by same player
        self.winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        # Strategic weights for each position on the board
        # Center (4) has highest weight (4), corners (0,2,6,8) have weight 3
        # Other positions have weight 2
        self.position_weights = [
            3, 2, 3,  # Corners and edges weights
            2, 4, 2,  # Center has highest weight
            3, 2, 3
        ]

    def make_move(self, position: int, player: str) -> bool:
        """Attempts to place player's mark ('X' or 'O') at the given position"""
        if self.is_valid_move(position):
            self.board[position] = player
            return True
        return False

    def is_valid_move(self, position: int) -> bool:
        """
        Checks if a move is valid:
        - Position must be within board (0-8)
        - Position must not be already taken by 'X' or 'O'
        """
        return 0 <= position <= 8 and self.board[position] not in ['X', 'O']

    def get_valid_moves(self) -> List[int]:
        """Returns a list of all available positions on the board"""
        return [i for i, spot in enumerate(self.board) if spot not in ['X', 'O']]

    def is_winner(self, player: str) -> bool:
        """
        Checks if the specified player has won by checking all possible
        winning combinations
        """
        for combo in self.winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False

    def is_board_full(self) -> bool:
        """Checks if there are no more valid moves available"""
        return all(spot in ['X', 'O'] for spot in self.board)

    def evaluate_position(self, depth: int) -> int:
        """
        Evaluates the current board state:
        - Returns positive score if AI is winning
        - Returns negative score if human is winning
        - Considers position weights for non-terminal positions
        - Depth is used to prefer winning in fewer moves
        """
        if self.is_winner('O'):  # AI wins
            return 100 + depth
        if self.is_winner('X'):  # Human wins
            return -100 - depth
        if self.is_board_full():
            return 0

        # Calculate score based on position weights
        score = 0
        for i, mark in enumerate(self.board):
            if mark == 'O':
                score += self.position_weights[i]
            elif mark == 'X':
                score -= self.position_weights[i]
        return score

    def get_winning_move(self, player: str) -> Optional[int]:
        """
        Checks if there's an immediate winning move available for the player
        Returns the winning position or None if no winning move exists
        """
        for move in self.get_valid_moves():
            temp = self.board[move]
            self.board[move] = player
            if self.is_winner(player):
                self.board[move] = temp
                return move
            self.board[move] = temp
        return None

    def minimax(self, depth: int, alpha: int, beta: int, is_maximizing: bool) -> Tuple[int, Optional[int]]:
        """
        Implements the minimax algorithm with alpha-beta pruning to find the best move
        - depth: how many moves ahead to look
        - alpha-beta: for pruning (optimization)
        - is_maximizing: True for AI's turn, False for human's turn
        Returns tuple of (score, best_move)
        """
        # Check for immediate winning moves first
        if is_maximizing:
            winning_move = self.get_winning_move('O')
            if winning_move is not None:
                return (100 + depth, winning_move)
        else:
            blocking_move = self.get_winning_move('X')
            if blocking_move is not None:
                return (-100 - depth, blocking_move)

        # Terminal state checks
        if self.is_winner('O'): return (100 + depth, None)
        if self.is_winner('X'): return (-100 - depth, None)
        if self.is_board_full(): return (0, None)
        if depth == 0: return (self.evaluate_position(depth), None)

        # Sort moves by position weights for better alpha-beta pruning
        valid_moves = self.get_valid_moves()
        valid_moves.sort(key=lambda x: self.position_weights[x], reverse=is_maximizing)

        best_move = None
        if is_maximizing:
            # AI's turn - maximize score
            max_eval = float('-inf')
            for move in valid_moves:
                temp = self.board[move]
                self.board[move] = 'O'
                eval_score, _ = self.minimax(depth - 1, alpha, beta, False)
                self.board[move] = temp
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha: break  # Alpha-beta pruning
            return (max_eval, best_move)
        else:
            # Human's turn - minimize score
            min_eval = float('inf')
            for move in valid_moves:
                temp = self.board[move]
                self.board[move] = 'X'
                eval_score, _ = self.minimax(depth - 1, alpha, beta, True)
                self.board[move] = temp
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha: break  # Alpha-beta pruning
            return (min_eval, best_move)

    def get_ai_move(self) -> int:
        """
        Gets the best move for AI using minimax algorithm
        Looks 6 moves ahead by default
        """
        _, best_move = self.minimax(6, float('-inf'), float('inf'), True)
        return best_move

    def display_board(self) -> None:
        """Prints the current state of the board in a readable format"""
        for i in range(0, 9, 3):
            print(f"{self.board[i]} | {self.board[i+1]} | {self.board[i+2]}")
            if i < 6:
                print("---------")

def play_game():
    """
    Main game loop:
    1. Creates new game
    2. Alternates between human and AI turns
    3. Checks for win/draw conditions after each move
    4. Handles user input and displays game state
    """
    game = TicTacToe()
    print("\nGame starts! Use numbers 1-9 to make your move\n")

    while True:
        game.display_board()

        # Human's turn - get input and validate move
        while True:
            try:
                move = int(input("\nEnter your move (1-9): ")) - 1
                if game.make_move(move, 'X'):
                    break
                print("Invalid move, try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a number between 1 and 9.")

        # Check if human won or board is full
        if game.is_winner('X'):
            game.display_board()
            print("Congratulations! You win!")
            break
        
        if game.is_board_full():
            game.display_board()
            print("It's a draw!")
            break

        # AI's turn
        ai_move = game.get_ai_move()
        game.make_move(ai_move, 'O')
        print(f"\nAI moves to position {ai_move + 1}")

        # Check if AI won or board is full
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

# Main program entry point
if __name__ == "__main__":
    print("Welcome to Tic Tac Toe!")
    print("You are X and the AI is O")
    while True:
        play_game()
        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break
