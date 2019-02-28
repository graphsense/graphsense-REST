import datetime
from passlib.hash import pbkdf2_sha256 as sha256
import sqlalchemy
from graphsenserest import db
from authmodel import GraphsenseUser

if __name__ == '__main__':
    admin = {'id': 0, 'userName': "admin", 'password': str(sha256.hash('test123')),
             'creationDate': datetime.datetime.now(), 'isAdmin': True}
    admin = GraphsenseUser(**admin)
    try:
        db.session.add(admin)
        db.session.commit()
        db.session.close()
    except sqlalchemy.exc.IntegrityError as ex:
        print("Admin user already exists")
        print(ex)





