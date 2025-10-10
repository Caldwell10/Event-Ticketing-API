import bcrypt
from sqlalchemy.orm import Session
import re

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
    if not isinstance(seat_labels, str):
        raise ValueError("Seat label must be a string")
    return re.sub(r"\s+", "", seat_labels).upper()
    


# calculate hold expiry time