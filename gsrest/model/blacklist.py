import datetime


class BlacklistToken:
    """ Token model for storing JWT tokens """

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
