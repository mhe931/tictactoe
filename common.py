# common.py
from enum import Enum
import os

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'

class GameState(Enum):
    ONGOING = 0
    X_WINS = 1
    O_WINS = 2
    DRAW = 3

class Board:
    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        
    def set_players(self, player1_name, player2_name):
        """Set the players' names"""
        self.player1_name = player1_name
        self.player2_name = player2_name
    
    def make_move(self, position, symbol):
        """Make a move using position 1-9"""
        position = int(position) - 1  # Convert to 0-based index
        if self.is_valid_move(position):
            self.board[position] = symbol
            return True
        return False
    
    def is_valid_move(self, position):
        """Check if the move is valid using 0-based index"""
        return 0 <= position < 9 and self.board[position] not in ['X', 'O']
    
    def get_valid_moves(self):
        """Return list of valid positions (1-9)"""
        return [i+1 for i in range(9) if self.board[i] not in ['X', 'O']]
    
    def check_winner(self):
        """Check if there's a winner"""
        lines = [(0,1,2), (3,4,5), (6,7,8),  # Rows
                (0,3,6), (1,4,7), (2,5,8),  # Columns
                (0,4,8), (2,4,6)]           # Diagonals
        
        for line in lines:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]]:
                if self.board[line[0]] == 'X':
                    return GameState.X_WINS
                elif self.board[line[0]] == 'O':
                    return GameState.O_WINS
        
        if all(cell in ['X', 'O'] for cell in self.board):
            return GameState.DRAW
            
        return GameState.ONGOING
    
    def get_state_key(self):
        """Return a string representation of the board state"""
        return ''.join(self.board)
    
    def display(self):
        """Display the board with colored X and O"""
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
        print("\nCurrent board:")
        print(f"{self.player1_name}: {Colors.RED}X{Colors.RESET}  |  "
              f"{self.player2_name}: {Colors.GREEN}O{Colors.RESET}\n")
        
        for i in range(0, 9, 3):
            row = []
            for j in range(3):
                cell = self.board[i + j]
                if cell == 'X':
                    cell = f"{Colors.RED}X{Colors.RESET}"
                elif cell == 'O':
                    cell = f"{Colors.GREEN}O{Colors.RESET}"
                elif cell.isdigit():
                    cell = f"{Colors.BLUE}{cell}{Colors.RESET}"
                row.append(cell)
            print(f"{row[0]} | {row[1]} | {row[2]}")
            if i < 6:
                print(f"{Colors.YELLOW}---------{Colors.RESET}")
        print()

def play_game(player1, player2, rl_observer=None, board=None):
    """Generic game loop that can be used by any game mode"""
    if board is None:
        board = Board()
    current_player = 'X'
    moves_history = []
    
    while True:
        board.display()
        
        try:
            # Get current player's move
            if current_player == 'X':
                move = player1(board)
            else:
                move = player2(board)
            
            # Check if move is valid
            if move is None or not board.make_move(move, current_player):
                print(f"Invalid move! Valid moves are: {board.get_valid_moves()}")
                continue
            
            # Record move for RL training
            if rl_observer:
                moves_history.append((board.get_state_key(), int(move)-1))
            
            # Check game state
            game_state = board.check_winner()
            if game_state != GameState.ONGOING:
                board.display()
                
                # Determine outcome
                if game_state == GameState.DRAW:
                    print("\nGame Over - It's a draw!")
                    reward = 0
                else:
                    print(f"\nGame Over - {current_player} wins!")
                    reward = 1
                
                # Let RL agent learn from the game
                if rl_observer and moves_history:
                    for state, action in moves_history:
                        rl_observer.learn(state, action, reward, board.get_state_key(), True)
                
                return game_state
            
            # Switch players
            current_player = 'O' if current_player == 'X' else 'X'
            
        except Exception as e:
            print(f"Error making move: {e}")
            print(f"Valid moves are: {board.get_valid_moves()}")
            continue

def get_human_move(board):
    """Get move from human player"""
    valid_moves = board.get_valid_moves()
    while True:
        try:
            move = input(f"Enter your move {valid_moves} (or 'z' to quit): ")
            if move.lower() == 'z':
                exit()
            move = int(move)
            if move in valid_moves:
                return move
            print("Invalid move!")
        except ValueError:
            print("Please enter a number!")
