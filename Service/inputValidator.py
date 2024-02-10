def is_valid_numeric_input(*args):
    """
    Check if the provided input values are valid numeric values (float or integer).

    Args:
        args: Input values to validate.

    Returns:
        bool: True if all values are valid numeric values, False otherwise.
    """
    for value in args:
        if value and not (isinstance(value, int) or isinstance(value, float)):
            return False
    return True
