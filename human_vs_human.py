# human_vs_human.py
from common import play_game, get_human_move, Board
from rl_agent import RLAgent

def main():
    # Initialize RL agent as observer
    board = Board()
    board.set_players("User 2", "User 1")
    
    rl_observer = RLAgent()
    
    while True:
        # Play game with two human players
        play_game(
            player1=get_human_move,  # X player
            player2=get_human_move,  # O player
            rl_observer=rl_observer  # RL agent learns by watching
        )
        
        # Ask to play again
        if input("\nPlay again? (y/n): ").lower() != 'y':
            break
    
    # Save what RL learned
    rl_observer.save()

if __name__ == "__main__":
    main()
