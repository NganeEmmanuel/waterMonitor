from Database.database import session
from Service import importService


def login(username, password):
    if username and password:
        user = session.query(importService.User).filter(importService.User.username == username).first()
        if user:
            if user.password == password:
                return "success"
            else:
                return "User credentials not valid"
        else:
            return "User credentials not valid"  # User not found
    else:
        return "Please fill all fields"
