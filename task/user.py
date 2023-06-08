class User:
    def __init__(self, name, password, right="admin"):
        self.name = name,
        self.password = password
        self.right = right
        self.is_login = False
