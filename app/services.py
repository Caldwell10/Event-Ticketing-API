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



# calculate hold expiry time