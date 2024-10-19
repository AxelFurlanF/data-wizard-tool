import bcrypt


def get_password_hash(password):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def verify_password(plain_password, hashed_password):
    # Check if the hashed password matches the plain text password
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
