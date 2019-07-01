from graphsenserest import db
from passlib.hash import pbkdf2_sha256 as sha256


class GraphsenseUser(db.Model):
    __tablename__ = "GraphsenseUser"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    userName = db.Column(db.String(120), nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(120), nullable=True)
    creationDate = db.Column(db.Date, nullable=False)


    def queryByIdStringOrNameFragment(idOrNameStr, limit=10):
        """Get a person by name or id.
        @return the query."""
        query = None
        try:
            query = db.session.query(GraphsenseUser).filter(GraphsenseUser.id == int(idOrNameStr))
        except:
            query = db.session.query(GraphsenseUser).filter(GraphsenseUser.sysName.like(
                "%%%s%%" % idOrNameStr)).limit(limit)
        return query

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(userName=username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class RevokedJWTToken(db.Model):
    __tablename__ = "revoked_tokens"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
