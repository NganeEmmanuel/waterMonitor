from model import user
from Database import crud
from Service import emailValidatorService


def add_user(name, username, email, password, authority):
    """
    Add a new user to the database.

    Args:
        name (str): The name of the user.
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The password of the user.
        authority (str): The type of authority for the user.

    Returns:
        str: The result message indicating the success or possible errors.

    """
    # Check if fields are not empty/blank else return "blank field" error
    if any(not field.strip() for field in (name, username, email, password, authority)):
        return "Please fill in all require (*) fields"

    # check for email validity
    if not emailValidatorService.validate_email(email):
        return "Invalid email format"

    # Create a new User object and set the attributes
    new_user = user.User()
    new_user.name = name
    new_user.username = username
    new_user.email = email
    new_user.password = password
    new_user.authority = authority

    # Add the new user to the database
    try:
        return crud.add(new_user)
    except Exception as e:

        # Handle any exceptions, such as duplicate fields
        return str(e)


def get_all_users():
    return crud.find_all(user.User)
