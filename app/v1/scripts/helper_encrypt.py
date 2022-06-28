from passlib.context import CryptContext


class HelperEncrypt:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, password, hash):
        return self.pwd_context.verify(password, hash)
