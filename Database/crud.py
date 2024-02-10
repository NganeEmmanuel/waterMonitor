from Database.database import session


def add(persist_object):
    """
        Add the given object to the database and commit the changes.

        Args:
            persist_object: The object to be persisted in the database.

    """
    session.add(persist_object)
    session.commit()
    session.close()
    return persist_object


def find_by(column_name, value, model):
    """
    Retrieve a single object from the database that matches the given criteria.

    Args:
        column_name: The name of the column to filter on.
        value: The value to match in the specified column.
        model: The SQLAlchemy model class to use for the query.

    Returns:
        The first object that matches the given criteria, or None if no such object is found.

    """
    # Query the database for objects matching the criteria
    result = session.query(model).filter(getattr(model, column_name) == value).first()

    # Close the session
    session.close()

    return result


def find_all(model):
    """
    Retrieve all objects of a given model from the database.

    Args:
        model: The SQLAlchemy model class to use for the query.

    Returns:
        A list of all objects of the specified model in the database.

    """
    # Query the database for all objects of the specified model
    results = session.query(model).all()

    # Close the session
    session.close()
    return results
