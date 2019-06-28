import datetime
from passlib.hash import pbkdf2_sha256 as sha256
import sqlalchemy
from graphsenserest import db
from authmodel import GraphsenseUser
from os import sys

if __name__ == '__main__':

    user = sys.argv[1]
    password = sys.argv[2]
    admin = {'id': 0, 'userName': user, 'password': str(sha256.hash(password)),
             'creationDate': datetime.datetime.now(), 'isAdmin': True}
    admin = GraphsenseUser(**admin)
    try:
        db.session.add(admin)
        db.session.commit()
        db.session.close()
    except sqlalchemy.exc.IntegrityError as ex:
        print("Admin user already exists")
        print(ex)
