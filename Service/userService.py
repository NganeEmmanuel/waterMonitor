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


def get_user_by_name(name):
    return crud.find_by("name", name, user.User)


def find_users_by_string_ids(approvers):
    """
    Finds users' names based on a list of user IDs.

    Args:
        approvers (str): A string of user IDs separated by commas or a single ID with no comma.

    Returns:
        str: A string containing the users' names separated by commas.

    """
    # Split the string of IDs by comma
    ids = approvers.split(',')

    # Initialize an empty list to store the users' names
    user_names = []

    # Iterate over each ID
    for u_id in ids:
        # Remove leading and trailing whitespaces from the ID
        u_id = u_id.strip()

        # Perform a search in the user database using crud.find_by("id", id, user.User)
        db_user = crud.find_by("id", u_id, user.User)

        # If a matching user is found, append their name to the user_names list
        if user:
            user_names.append(db_user.name)

    # Create a string of users' names separated by commas
    result = ', '.join(user_names)

    # Return the string of users' names
    return result
