from Database.database import session


def add(persist_object):
    session.add(persist_object)
    session.commit()
    session.close()
