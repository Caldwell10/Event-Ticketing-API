import bcrypt
from sqlalchemy.orm import Session

# hash payload password before being stored in the database
def hash_password(password: str):
    """Hash a plaintext password."""
    
    # create a salt
    salt = bcrypt.gensalt()

    # hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8')

# normalize seat labels
def normalize_seat_labels(seat_labels):
    # trim whitespace and convert to uppercase
    label = (seat_labels or "").strip().upper()
    if not label:
        raise ValueError("Seat label cannot be empty or just whitespace.")
    return label


# calculate hold expiry time