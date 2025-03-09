# human_vs_rl.py
from common import play_game, get_human_move, Board
from rl_agent import RLAgent

def get_rl_move(board):
    """Get move from RL agent"""
    action = rl_player.choose_action(board)
    return action[0] * 3 + action[1] + 1

def main():
    board = Board()
    board.set_players("User", "Agent")
    # Initialize RL agents
    global rl_player  # The one that plays
    rl_player = RLAgent()
    rl_observer = RLAgent()  # The one that learns by watching
    
    while True:
        # Reset the board for a new game
        board = Board()
        board.set_players("User", "Agent")
        
        # Play game with human vs RL
        play_game(
            player1=get_human_move,  # Human as X
            player2=get_rl_move,     # RL as O
            rl_observer=rl_observer,  # Second RL agent learns by watching
            board=board  # Pass the board with custom player names
        )
        
        # Ask to play again
        if input("\nPlay again? (y/n): ").lower() != 'y':
            break
    
    # Save what both RL agents learned
    rl_player.save("rl_player.pkl")
    rl_observer.save("rl_observer.pkl")

if __name__ == "__main__":
    main()
