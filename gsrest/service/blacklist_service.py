from gsrest.db.user_db import get_db
from gsrest.model.blacklist import BlacklistToken


def save_token(token):
    blacklist_token = BlacklistToken(token)
    db = get_db()

    if not check_blacklist(token):
        db.execute('INSERT INTO blacklist_tokens (token, blacklisted_on) \
                    VALUES (?, ?)',
                   (blacklist_token.token, blacklist_token.blacklisted_on)
                   )
        db.commit()


def check_blacklist(token):
    db = get_db()
    db_token = db.execute(
        'SELECT * FROM blacklist_tokens WHERE token = ?', (token,)
    ).fetchone()

    if db_token is None:
        # print('Token {} is not blacklisted'.format(token))
        return False
    else:
        # print('Token {} is blacklisted'.format(token))
        return True
