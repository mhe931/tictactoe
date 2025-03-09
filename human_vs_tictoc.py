# human_vs_tictoc.py
from common import play_game, get_human_move, Board
from tictac import TicTacToe
from rl_agent import RLAgent

def get_tictoc_move(board):
    """Get move from TicToc AI"""
    tictoc = TicTacToe()
    # Convert board for TicToc
    board_2d = [board.board[i:i+3] for i in range(0, 9, 3)]
    move = tictoc.get_best_move(board_2d)
    if move:
        return move[0] * 3 + move[1] + 1
    return None

def main():
    board = Board()
    board.set_players("User", "TicToc")
    # Initialize RL agent as observer
    rl_observer = RLAgent()
    
    while True:
        # Play game with human vs TicToc
        play_game(
            player1=get_human_move,    # Human as X
            player2=get_tictoc_move,   # TicToc as O
            rl_observer=rl_observer    # RL agent learns by watching
        )
        
        # Ask to play again
        if input("\nPlay again? (y/n): ").lower() != 'y':
            break
    
    # Save what RL learned
    rl_observer.save()

if __name__ == "__main__":
    main()
