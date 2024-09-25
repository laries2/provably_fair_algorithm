import hashlib

# Hash of the preselected Bitcoin block (block #637645)
bitcoin_block_hash = "00000000000000000000cd2bcb44f656649c69d8b17ade0399168f3cbe859d26"

# Function to generate the next game hash in the chain
def next_hash(current_hash):
    return hashlib.sha256(current_hash.encode()).hexdigest()

# Function to salt the game hash with the Bitcoin block hash
def salt_hash(game_hash, bitcoin_hash):
    return hashlib.sha256((game_hash + bitcoin_hash).encode()).hexdigest()

# Function to calculate the burst value from a salted hash
def calculate_burst_value(salted_hash):
    # Convert the salted hash to an integer
    int_value = int(salted_hash, 16)
    # Calculate the burst value, example: modulo 1000
    burst_value = (int_value % 10000000) / 100000.0
    return round(burst_value, 2)

# Example usage
current_hash = "b04b67bc48fe8fa49d9491236f4e1e241e7c5061f8d3b89756a4b075c9224f85"  # Replace with your current game hash
next_game_hash = next_hash(current_hash)
salted_hash = salt_hash(next_game_hash, bitcoin_block_hash)
predicted_burst_value = calculate_burst_value(salted_hash)

print(f"Next Game Hash: {next_game_hash}")
print(f"Salted Hash: {salted_hash}")
print(f"Predicted Burst Value: {predicted_burst_value}")
