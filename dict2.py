import hashlib

# Function to generate the SHA256 hash
def sha256_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

# Function to get the next hash in the sequence
def get_next_hash(current_hash):
    return sha256_hash(current_hash)

# Function to calculate the burst value from a salted hash
def calculate_burst_value(salted_hash):
    hash_int = int(salted_hash, 16)
    e = 2.718281828459045
    if (hash_int % 33) == 0:
        return 1.0
    return round((100 * e ** ((hash_int % 52) / (2**52))) / 100.0, 2)

# Function to generate the next burst value
def generate_next_burst_value(current_hash, bitcoin_block_hash):
    next_hash = get_next_hash(current_hash)
    salted_hash = sha256_hash(next_hash + bitcoin_block_hash)
    next_burst_value = calculate_burst_value(salted_hash)
    return next_hash, next_burst_value

# Example usage
current_hash = '486316c11544b3e88f03bde127c44c6eb96a0b58952bff1795a0ee55ee0f4572'  # Replace with the actual current hash value
bitcoin_block_hash = '00000000000000000000cd2bcb44f656649c69d8b17ade0399168f3cbe859d26'

next_hash, next_burst_value = generate_next_burst_value(current_hash, bitcoin_block_hash)

print("Next Hash:", next_hash)
print("Next Burst Value:", next_burst_value)
