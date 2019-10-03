#!/usrbin/env python3
# coding: utf-8
'''Script to add user to SQLite database (/var/lib/graphsense-rest/users.db)'''

from argparse import ArgumentParser
import datetime
from passlib.hash import pbkdf2_sha256 as sha256
import sqlalchemy
from graphsenserest import db
from authmodel import GraphsenseUser


if __name__ == '__main__':

    parser = ArgumentParser(description='Add user to REST API',
                            epilog='GraphSense - http://graphsense.info')
    parser.add_argument('-u', '--user', dest='user', type=str, required=True,
                        help='user name')
    parser.add_argument('-p', '--pass', dest='passwd', type=str, required=True,
                        help='user password')
    parser.add_argument('--uid', dest='uid', type=int, required=True,
                        help='user id')
    args = parser.parse_args()

    admin = {
        "id": args.uid,
        "userName": args.user,
        "password": str(sha256.hash(args.passwd)),
        "creationDate": datetime.datetime.now(),
        "isAdmin": True
    }
    admin = GraphsenseUser(**admin)
    try:
        db.session.add(admin)
        db.session.commit()
        db.session.close()
    except sqlalchemy.exc.IntegrityError as ex:
        print(ex)
