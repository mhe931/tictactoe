import random
from typing import List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TicTacToe:

    def __init__(self):
        self.board = [None] * 9
        # Define all possible winning combinations
        self.winning_combinations = [
            # Rows
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            # Columns
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            # Diagonals
            [0, 4, 8], [2, 4, 6]
        ]
        
    def get_state_key(self):
        """Return a hashable representation of the board state"""
        return tuple(self.board)

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

    def get_valid_moves(self):
        """Get list of empty positions"""
        try:
            return [i for i, spot in enumerate(self.board) if spot is None]
        except Exception as e:
            print(f"Error in get_valid_moves: {e}")
            return []
        
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

    def minimax(self, depth, alpha, beta, is_maximizing):
        """Minimax algorithm with alpha-beta pruning"""
        try:
            if depth == 0 or self.is_winner('X') or self.is_winner('O') or not self.get_valid_moves():
                return self.evaluate_board(), None
            
            valid_moves = self.get_valid_moves()
            if not valid_moves:
                return 0, None
                
            if is_maximizing:
                best_score = float('-inf')
                best_move = random.choice(valid_moves)
                
                for move in valid_moves:
                    self.board[move] = 'O'
                    score, _ = self.minimax(depth-1, alpha, beta, False)
                    self.board[move] = None
                    
                    if score > best_score:
                        best_score = score
                        best_move = move
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
                        
                return best_score, best_move
            else:
                best_score = float('inf')
                best_move = random.choice(valid_moves)
                
                for move in valid_moves:
                    self.board[move] = 'X'
                    score, _ = self.minimax(depth-1, alpha, beta, True)
                    self.board[move] = None
                    
                    if score < best_score:
                        best_score = score
                        best_move = move
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
                        
                return best_score, best_move
                
        except Exception as e:
            print(f"Error in minimax: {e}")
            return 0, None
    def get_ai_move(self) -> int:
        """
        Gets the best move for AI using minimax algorithm
        Looks 6 moves ahead by default
        """
        _, best_move = self.minimax(6, float('-inf'), float('inf'), True)
        return best_move

    def get_best_move(self, depth=6):
        """Get best move using minimax with configurable depth"""
        try:
            if not self.get_valid_moves():
                return None
                
            best_score = float('-inf')
            best_move = None
            
            for move in self.get_valid_moves():
                self.board[move] = 'O'
                score, _ = self.minimax(depth-1, float('-inf'), float('inf'), False)
                self.board[move] = None
                
                if score > best_score:
                    best_score = score
                    best_move = move
            
            return best_move
            
        except Exception as e:
            print(f"Error in get_best_move: {e}")
            return None
        
    def display_board(self) -> None:
        """Prints the current state of the board in a readable format"""
        for i in range(0, 9, 3):
            print(f"{self.board[i]} | {self.board[i+1]} | {self.board[i+2]}")
            if i < 6:
                print("---------")

def play_game() -> None:
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
