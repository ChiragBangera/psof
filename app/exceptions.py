class UserNotFound(Exception):
    def __init__(self, user_id):
        self.user_id = user_id


class UserAlreadyExist(Exception):
    pass
