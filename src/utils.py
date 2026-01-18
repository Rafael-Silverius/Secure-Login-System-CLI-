import hashlib
# --------- Hashing Function ---------
def hash_password(password):
    """
    Returns a SHA-256 hash of the password
    """
    return hashlib.sha256(password.encode()).hexdigest()