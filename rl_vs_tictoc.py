# rl_vs_tictoc.py
from common import play_game, Board, GameState, Colors
from tictac import TicTacToe
from rl_agent import RLAgent
import random
import time

def get_tictoc_move(board):
    """Get move from TicToc AI"""
    tictoc = TicTacToe()
    
    # Convert board for TicToc
    tictoc_board = []
    for i in range(9):
        cell = board.board[i]
        if cell == 'X':
            tictoc_board.append('X')
        elif cell == 'O':
            tictoc_board.append('O')
        else:
            tictoc_board.append(None)
    
    # Set TicToc's internal board state
    tictoc.board = tictoc_board
    
    try:
        # Get valid moves from TicToc's perspective
        valid_moves = tictoc.get_valid_moves()
        if not valid_moves:
            return None
            
        # Try to get best move with lower depth if board is partially filled
        filled_spots = sum(1 for cell in tictoc_board if cell in ['X', 'O'])
        depth = min(6, 9 - filled_spots)  # Adjust depth based on remaining moves
        
        move = tictoc.get_best_move(depth=depth)
        if move is not None:
            # Convert TicToc's move (0-8) to our format (1-9)
            return move + 1
            
    except Exception as e:
        print(f"TicToc error: {e}")
    
    # Fallback: choose random valid move
    valid_moves = board.get_valid_moves()
    if valid_moves:
        return random.choice(valid_moves)
    return None

def get_rl_move(board):
    """Get move from RL agent"""
    move = rl_player.choose_action(board)
    if isinstance(move, tuple):
        return move[0] * 3 + move[1] + 1
    return move

def play_game_with_names(player1, player2, rl_observer=None, rl_plays_x=True):
    """Wrapper for play_game that sets player names"""
    board = Board()
    if rl_plays_x:
        board.set_players("Agent", "TicToc")
    else:
        board.set_players("TicToc", "Agent")
    return play_game(player1, player2, rl_observer, board)

def play_tournament(num_games, delay=1):
    """Play multiple games between RL and TicToc"""
    scores = {"RL": 0, "TicToc": 0, "Draws": 0}
    rl_as_x_wins = 0
    rl_as_o_wins = 0
    
    print(f"\n{Colors.BLUE}Starting tournament of {num_games} games...{Colors.RESET}\n")
    
    for game in range(num_games):
        # Alternate who plays X
        rl_plays_x = game % 2 == 0
        
        print(f"\n{Colors.YELLOW}Game {game + 1}{Colors.RESET}")
        print(f"RL plays as: {Colors.RED + 'X' + Colors.RESET if rl_plays_x else Colors.GREEN + 'O' + Colors.RESET}")
        
        # Play the game with proper names
        result = play_game_with_names(
            player1=get_rl_move if rl_plays_x else get_tictoc_move,
            player2=get_tictoc_move if rl_plays_x else get_rl_move,
            rl_observer=rl_observer,
            rl_plays_x=rl_plays_x
        )
        
        # Record results
        if result == GameState.X_WINS:
            winner = "RL" if rl_plays_x else "TicToc"
            if winner == "RL":
                rl_as_x_wins += 1
        elif result == GameState.O_WINS:
            winner = "RL" if not rl_plays_x else "TicToc"
            if winner == "RL":
                rl_as_o_wins += 1
        else:
            winner = "Draw"
        
        if winner == "RL":
            scores["RL"] += 1
        elif winner == "TicToc":
            scores["TicToc"] += 1
        else:
            scores["Draws"] += 1
        
        # Show current score
        print(f"\n{Colors.BLUE}Current Score (Game {game + 1}/{num_games}):{Colors.RESET}")
        print(f"RL: {scores['RL']} ({scores['RL']/(game+1)*100:.1f}%)")
        print(f"TicToc: {scores['TicToc']} ({scores['TicToc']/(game+1)*100:.1f}%)")
        print(f"Draws: {scores['Draws']} ({scores['Draws']/(game+1)*100:.1f}%)")
        
        # Save progress periodically
        if (game + 1) % 10 == 0:
            rl_player.save("rl_player.pkl")
            rl_observer.save("rl_observer.pkl")
            print(f"\n{Colors.BLUE}Progress saved!{Colors.RESET}")
        
        # Add delay between games
        time.sleep(delay)

def main():
    global rl_player, rl_observer
    
    # Initialize RL agents
    rl_player = RLAgent()
    rl_observer = RLAgent()  # Second agent that learns by watching
    
    # Get number of games from user
    while True:
        try:
            num_games = int(input("Enter number of games to play: "))
            if num_games > 0:
                break
            print("Please enter a positive number!")
        except ValueError:
            print("Please enter a valid number!")
    
    # Get delay between games
    while True:
        try:
            delay = float(input("Enter delay between games (seconds, 0 for no delay): "))
            if delay >= 0:
                break
            print("Please enter a non-negative number!")
        except ValueError:
            print("Please enter a valid number!")
    
    # Play the tournament
    play_tournament(num_games, delay)
    
    # Ask to play another tournament
    while input("\nPlay another tournament? (y/n): ").lower() == 'y':
        while True:
            try:
                num_games = int(input("Enter number of games to play: "))
                if num_games > 0:
                    break
                print("Please enter a positive number!")
            except ValueError:
                print("Please enter a valid number!")
        play_tournament(num_games, delay)

if __name__ == "__main__":
    main()
