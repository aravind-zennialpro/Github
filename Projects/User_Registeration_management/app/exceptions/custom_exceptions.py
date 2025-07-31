class UserAlreadyExists(Exception):
    def __init__(self, message="User already exists."):
        self.message = message
        super().__init__(self.message)

class InvalidPasswordFormat(Exception):
    def __init__(self, message="Password does not meet complexity requirements."):
        self.message = message
        super().__init__(self.message)
