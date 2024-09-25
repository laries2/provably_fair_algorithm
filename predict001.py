import hashlib
import hmac

# Constants
SALT = '00000000000000000000cd2bcb44f656649c69d8b17ade0399168f3cbe859d26'
N_BITS = 52

def hmac_sha256(key, message):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

def game_result(seed):
    # 1. HMAC_SHA256(message=seed, key=SALT)
    hash_value = hmac_sha256(SALT, seed)
    
    # 2. r = 52 most significant bits
    r = int(hash_value[:N_BITS // 4], 16)
    
    # 3. X = r / 2^52
    X = r / float(2**N_BITS)
    
    # 4. X = 90 / (1 - X)
    result = 90 / (1 - X)
    
    # 5. Return capped to 1 on the lower end
    return max(1, round(result / 100, 2))

# Example usage
current_hash = "ad20def0117cab6072f0a5e30e034f6b604f2dae063e024d54224686f856f60e"  # Replace with your current game hash
predicted_burst_value = game_result(current_hash)

print(f"Current Game Hash: {current_hash}")
print(f"Predicted Burst Value: {predicted_burst_value}")
