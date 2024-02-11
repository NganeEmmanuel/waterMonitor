def is_string_valid_numeric_input(*args):
    """
    Check if the provided string input values are valid numeric values (float or integer).

    Args:
        args: Input values to validate.

    Returns:
        bool: True if all values are valid numeric values, False otherwise.
    """
    for value in args:
        if value is not None and not value.isspace() and value != "":  # checks if it's not empty and not equal to None
            try:
                float(value)  # try converting value to float
            except ValueError:
                return False  # catch error and return false
    return True
