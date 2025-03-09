import random
import argparse
from tqdm import tqdm
from tictac import TicTacToe
from rl_agent import RLAgent

def train_agent(num_episodes=1000, save_interval=500):
    """
    Train the RL agent through self-play for the specified number of episodes.
    
    Args:
        num_episodes: Number of games to play (default: 1000)
        save_interval: How often to save progress (default: 500)
    """
    agent = RLAgent(learning_rate=0.1, discount_factor=0.95, epsilon=0.2)
    
    print(f"Starting training for {num_episodes} episodes...")

    # Use tqdm to create a progress bar
    for episode in range(1, num_episodes + 1):
        game = TicTacToe()
        done = False
        
        # Initialize for tracking immediate learning
        current_player = "X"  # X always starts
        prev_state = None
        prev_action = None
        
        while not done:
            # Store current state before action
            current_state = game.get_state_key()
            
            # Choose action
            action = agent.choose_action(game)
            
            # If we have a previous state-action pair, update it based on this new state
            if prev_state is not None:
                # Immediate reward for non-terminal states is small
                immediate_reward = 0.0
                agent.learn(prev_state, prev_action, immediate_reward, current_state, False)
                
            # Make the move (action is 0-based, but game takes 1-based)
            game.make_move(action + 1, current_player)
            
            # Check if the game is over
            game_over = False
            reward = 0.0
            
            if game.is_winner(current_player):
                game_over = True
                # Winning player gets positive reward
                reward = 1.0
                # Update Q-value for the winning move immediately
                agent.learn(current_state, action, reward, None, True)
                
                # The other player's last move led to a position where they lost
                if prev_state is not None and current_player != "X": # meaning O just won, so X's last move was bad
                    agent.learn(prev_state, prev_action, -1.0, None, True)
                
            elif game.is_board_full():
                game_over = True
                # Draw is a small positive reward
                reward = 0.2
                # Update Q-value for the final move
                agent.learn(current_state, action, reward, None, True)
            
            # If game continues, store state-action for next iteration
            if not game_over:
                prev_state = current_state
                prev_action = action
                # Switch players
                current_player = "O" if current_player == "X" else "X"
            else:
                done = True
        
        # Save periodically but less frequently to reduce disk I/O
        if episode % save_interval == 0:
            print(f"Completed {episode}/{num_episodes} training episodes")
            agent.save_q_table("q_table_latest.pkl")
        
        print(f" episode: {episode}")
    # Save final model
    agent.save("trained_agent.pkl")
    print(f"Training completed. Agent trained on {num_episodes} games.")

if __name__ == "__main__":
    # Set up argument parser
    # parser = argparse.ArgumentParser(description='Train a reinforcement learning agent for Tic-Tac-Toe')
    # parser.add_argument('--episodes', type=int, default=1000,
    #                     help='Number of training episodes (default: 1000)')
    # parser.add_argument('--save-interval', type=int, default=100,
    #                     help='How often to save training progress (default: 100)')
    
    # # Parse arguments
    # args = parser.parse_args()
    
    # Train the agent with the provided parameters
    # train_agent(num_episodes=args.episodes, save_interval=args.save_interval)
    train_agent(num_episodes=100, save_interval=10)

