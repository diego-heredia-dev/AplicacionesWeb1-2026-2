class AuthError(Exception):
    def __init__(self, message, status_code=401):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
