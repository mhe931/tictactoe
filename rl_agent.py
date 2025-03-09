# rl_agent.py
import random
import pickle
import os
from collections import defaultdict

class RLAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        """
        Initialize RL agent with:
        learning_rate: How quickly the agent updates its Q-values (0-1)
        discount_factor: How much future rewards matter (0-1)
        epsilon: Chance of random exploration (0-1)
        """
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.q_table = defaultdict(float)  # Use defaultdict for sparse representation
        self.save_counter = 0  # Counter to track when to save
        
        # Try to load existing Q-table
        self.load_q_table()
    
    def choose_action(self, board):
        """Choose an action using epsilon-greedy strategy"""
        valid_moves = board.get_valid_moves()
        
        # Exploration: random move
        if random.random() < self.epsilon:
            return random.choice(valid_moves)
        
        # Exploitation: best known move
        return self.get_best_action(board, valid_moves)
    
    def get_best_action(self, board, valid_moves):
        """Get the action with highest Q-value for current state"""
        state = board.get_state_key()
        best_value = float('-inf')
        best_actions = []  # Track equally good actions
        
        # Find action(s) with highest Q-value
        for move in valid_moves:
            state_action = (state, move-1)  # Convert to 0-based index for internal use
            value = self.q_table[state_action]  # defaultdict returns 0 for missing keys
            
            if value > best_value:
                best_value = value
                best_actions = [move]  # Reset list with this move
            elif value == best_value:
                best_actions.append(move)  # Add equally good move
        
        # Choose randomly among best actions (exploration among equally good actions)
        return random.choice(best_actions if best_actions else valid_moves)
    
    def learn(self, state, action, reward, next_state, done):
        """Update Q-values using Q-learning algorithm"""
        # Get current Q-value
        state_action = (state, action)
        current_q = self.q_table[state_action]  # defaultdict returns 0 for missing keys
        
        if done:
            # Terminal state
            new_q = current_q + self.lr * (reward - current_q)
        else:
            # Non-terminal state
            # Get valid moves more efficiently
            empty_positions = [i for i, char in enumerate(next_state) if char == ' ']
            
            # Check if we have any valid next actions
            if empty_positions:
                # Get maximum Q-value for next state from valid moves
                next_values = [self.q_table[(next_state, move)] for move in empty_positions]
                next_max = max(next_values) if next_values else 0
            else:
                next_max = 0
            
            # Q-learning formula
            new_q = current_q + self.lr * (reward + self.gamma * next_max - current_q)
        
        # Update Q-table
        self.q_table[state_action] = new_q
        
        # Less aggressive saving (use a counter and save every 5000 updates)
        self.save_counter += 1
        if self.save_counter >= 5000:
            self.save_q_table()
            self.save_counter = 0
    
    def load_q_table(self, filename="q_table.pkl"):
        """Load Q-table if it exists"""
        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as f:
                    loaded_table = pickle.load(f)
                    # Convert to defaultdict if it was a regular dict
                    if not isinstance(loaded_table, defaultdict):
                        self.q_table = defaultdict(float, loaded_table)
                    else:
                        self.q_table = loaded_table
                print(f"Loaded Q-table with {len(self.q_table)} state-action pairs")
            except Exception as e:
                print(f"Error loading Q-table: {e}")
                self.q_table = defaultdict(float)
        else:
            print("No existing Q-table found. Starting fresh.")
            self.q_table = defaultdict(float)
    
    def save_q_table(self, filename="q_table.pkl"):
        """Save Q-table to file"""
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self.q_table, f)
            print(f"Saved Q-table with {len(self.q_table)} state-action pairs")
        except Exception as e:
            print(f"Error saving Q-table: {e}")
    
    def save(self, filename="trained_agent.pkl"):
        """Save the entire agent state"""
        state = {
            'q_table': self.q_table,
            'lr': self.lr,
            'gamma': self.gamma,
            'epsilon': self.epsilon
        }
        try:
            with open(filename, 'wb') as f:
                pickle.dump(state, f)
            # Also save Q-table separately
            self.save_q_table()
            print(f"Agent saved successfully with {len(self.q_table)} learned states")
        except Exception as e:
            print(f"Error saving agent: {e}")
    
    def load(self, filename="trained_agent.pkl"):
        """Load the entire agent state"""
        try:
            with open(filename, 'rb') as f:
                state = pickle.load(f)
            self.q_table = state['q_table']
            self.lr = state['lr']
            self.gamma = state['gamma']
            self.epsilon = state['epsilon']
            print(f"Agent loaded successfully with {len(self.q_table)} learned states")
        except Exception as e:
            print(f"Error loading agent: {e}")
            # Try to load just Q-table as fallback
            self.load_q_table()
