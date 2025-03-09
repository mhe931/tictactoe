#!/usr/bin/env python3
# play.py - Main menu for Tic-Tac-Toe game modes
from common import play_game, get_human_move, Board
from tictac import TicTacToe
from rl_agent import RLAgent
import os 

def get_tictoc_move(board):
    """Get move from TicToc AI"""
    tictoc = TicTacToe()
    # Convert board for TicToc
    board_2d = [board.board[i:i+3] for i in range(0, 9, 3)]
    move = tictoc.get_best_move(board_2d)
    if move:
        return move[0] * 3 + move[1] + 1
    return None

def get_rl_move(board):
    """Get move from RL agent"""
    # Check if trained agent exists, if not, train one
    if not os.path.exists("trained_agent.pkl"):
        print("No trained agent found. Training new agent...")
        import train_agent
        train_agent.train_agent()
        print("Training complete. Starting game...")
    
    rl_player = RLAgent()
    rl_player.load()
    return rl_player.choose_action(board)

def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 40)
    print("TIC-TAC-TOE GAME MENU")
    print("=" * 40)
    print("1. Human vs Human")
    print("2. Human vs RL Agent")
    print("3. Human vs TicToc")
    print("4. RL Agent vs TicToc")
    print("5. Exit")
    print("=" * 40)
    return input("Select an option (1-5): ")

def human_vs_human():
    """Play Human vs Human mode"""
    board = Board()
    board.set_players("User 1", "User 2")
    
    # Initialize RL agent as observer
    rl_observer = RLAgent()
    
    while True:
        play_game(
            player1=get_human_move,  # X player
            player2=get_human_move,  # O player
            rl_observer=rl_observer,  # RL agent learns by watching
            board=board
        )
        
        if input("\nPlay again in this mode? (y/n): ").lower() != 'y':
            break
    
    # Save what RL learned
    rl_observer.save()

def human_vs_rl():
    """Play Human vs RL Agent mode"""
    board = Board()
    board.set_players("User", "RL Agent")
    
    # Check if trained agent exists, if not, train one
    if not os.path.exists("trained_agent.pkl"):
        print("No trained agent found. Training new agent...")
        import train_agent
        train_agent.train_agent()
        print("Training complete. Starting game...")
    
    # RL agent as both player and observer
    rl_agent = RLAgent()
    rl_agent.load()  # Load pre-trained agent
    
    while True:
        # Randomly decide who goes first
        import random
        if random.choice([True, False]):
            print("You play as X (first)")
            play_game(
                player1=get_human_move,  
                player2=get_rl_move,
                board=board
            )
        else:
            print("RL Agent plays as X (first)")
            play_game(
                player1=get_rl_move,
                player2=get_human_move,
                board=board
            )
        
        if input("\nPlay again in this mode? (y/n): ").lower() != 'y':
            break

def human_vs_tictoc():
    """Play Human vs TicToc mode"""
    os.system('cls' if os.name == 'nt' else 'clear') 
    board = Board()
    board.set_players("User", "TicToc")
    
    # Initialize RL agent as observer
    rl_observer = RLAgent()
    
    while True:
        play_game(
            player1=get_human_move,    # Human as X
            player2=get_tictoc_move,   # TicToc as O
            rl_observer=rl_observer,   # RL agent learns by watching
            board=board
        )
        
        if input("\nPlay again in this mode? (y/n): ").lower() != 'y':
            break
    
    # Save what RL learned
    rl_observer.save()

def rl_vs_tictoc():
    """Play RL Agent vs TicToc mode"""
    print("\nStarting RL Agent vs TicToc match")
    
    # Number of games
    try:
        num_games = int(input("How many games to play? (default: 10): ") or "10")
    except ValueError:
        num_games = 10
    
    # Speed of play
    try:
        delay = float(input("Delay between moves in seconds (default: 0.5): ") or "0.5")
    except ValueError:
        delay = 0.5
        
    import time
        
    # Initialize counters
    rl_wins = 0
    tictoc_wins = 0
    draws = 0
    
    # Check if trained agent exists, if not, train one
    if not os.path.exists("trained_agent.pkl"):
        print("No trained agent found. Training new agent...")
        import train_agent
        train_agent.train_agent()
        print("Training complete. Starting game...")
    
    # Initialize RL agent
    rl_agent = RLAgent()
    rl_agent.load()
    
    # Initialize TicToc
    tictoc = TicTacToe()
    
    # Play tournament
    for game_num in range(1, num_games + 1):
        print(f"\nGame {game_num} of {num_games}")
        
        board = Board()
        board.set_players("RL Agent", "TicToc")
        
        # Alternate who goes first
        if game_num % 2 == 1:
            result = play_game(
                player1=get_rl_move,      # RL as X
                player2=get_tictoc_move,  # TicToc as O
                board=board
            )
            if result == "X":
                rl_wins += 1
            elif result == "O":
                tictoc_wins += 1
            else:
                draws += 1
        else:
            result = play_game(
                player1=get_tictoc_move,  # TicToc as X
                player2=get_rl_move,      # RL as O
                board=board
            )
            if result == "X":
                tictoc_wins += 1
            elif result == "O":
                rl_wins += 1
            else:
                draws += 1
                
        # Display current score
        print(f"\nCurrent score: RL Agent: {rl_wins}, TicToc: {tictoc_wins}, Draws: {draws}")
        
        # Add delay between games
        time.sleep(delay)
        
    # Final results
    print("\n" + "=" * 40)
    print(f"FINAL RESULTS AFTER {num_games} GAMES")
    print(f"RL Agent wins: {rl_wins}")
    print(f"TicToc wins: {tictoc_wins}")
    print(f"Draws: {draws}")
    print("=" * 40)

def main():
    """Main function with game menu"""
    os.system('cls' if os.name == 'nt' else 'clear') 
    print("Welcome to Tic-Tac-Toe Game!")
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            human_vs_human()
        elif choice == '2':
            human_vs_rl()
        elif choice == '3':
            human_vs_tictoc()
        elif choice == '4':
            rl_vs_tictoc()
        elif choice == '5':
            print("Thank you for playing! Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option (1-5).")

if __name__ == "__main__":
    main()