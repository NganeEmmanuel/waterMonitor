from Database import crud
from model import authUser
from Service import loginUser


def set_auth_user():
    auth_user = crud.find_by("id", 1, authUser.AuthUser)
    loginUser.login_user = auth_user
