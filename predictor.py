import hashlib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# Constants
BITCOIN_BLOCK_HASH = '00000000000000000000cd2bcb44f656649c69d8b17ade0399168f3cbe859d26'
FINAL_CHAIN_HASH = '5de24be2ba88f21070aca0b909a23ba8977a60e047e750dc6bd637aa3b4defc8'
CHAIN_LENGTH = 10000000

def sha256_hexdigest(data):
    """Compute SHA256 hash of the given data and return the hex digest."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def salt_game_hash(game_hash):
    """Salt the game hash with the preselected Bitcoin block hash."""
    return sha256_hexdigest(game_hash + BITCOIN_BLOCK_HASH)

def verify_game_hash(game_hash, chain_length=CHAIN_LENGTH, final_hash=FINAL_CHAIN_HASH):
    """Verify if the game hash is part of the chain leading to the final hash."""
    salted_hash = salt_game_hash(game_hash)
    
    print(f"Starting salted hash: {salted_hash}")  # Debugging output
    
    for i in range(chain_length):
        if salted_hash == final_hash:
            print(f"Hash matched at iteration {i+1}")
            return True
        salted_hash = sha256_hexdigest(salted_hash)
        
        # Optional: Add periodic checks for long chains to avoid excessive output
        if i % 100000 == 0:
            print(f"Iteration {i+1}: Current hash: {salted_hash}")
    
    print("Final hash did not match.")  # Debugging output
    return False


def hash_to_numeric(game_hash):
    """Convert a SHA256 hash to a numeric feature, normalizing large values."""
    return int(game_hash, 16)  # Convert hexadecimal to decimal integer

def normalize_data(data):
    """Normalize the numeric data to handle large values."""
    scaler = StandardScaler()
    return scaler.fit_transform(data)

def load_data(filepath):
    """Load historical burst data from a CSV file."""
    return pd.read_csv(filepath)

def train_model(data):
    """Train a Random Forest model using historical data."""
    data['game_hash_numeric'] = data['hash'].apply(hash_to_numeric)
    X = data[['game_hash_numeric']]
    y = data['burst_value']
    
    # Normalize data
    X = normalize_data(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse:.2f}")
    
    return model

def predict_burst(model, game_hash):
    """Predict burst value for a given game hash using the trained model."""
    game_hash_numeric = hash_to_numeric(game_hash)
    game_hash_numeric = np.array([[game_hash_numeric]])
    
    # Normalize input
    game_hash_numeric = normalize_data(game_hash_numeric)
    
    predicted_burst = model.predict(game_hash_numeric)[0]
    return predicted_burst

# Example usage
if __name__ == "__main__":
    # Load historical burst data
    data = load_data('burst_data.csv')

    # Train model
    model = train_model(data)
    
    # Example game hash
    example_game_hash = 'f75d240509b2cab5b21c940f12997f82125018c93fe5b1dbc55ac323c68c36fc'  # Replace with an actual hash value

    # Verify if the game hash is valid
    if verify_game_hash(example_game_hash):
        # Predict burst value
        predicted_burst = predict_burst(model, example_game_hash)
        print(f"Predicted Burst Value: {predicted_burst:.2f}")
        print(f"Game Hash: {example_game_hash}")
    else:
        print("Invalid game hash")
