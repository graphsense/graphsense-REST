class UserFacingExceptions(Exception):
    """ Hierarchy of exceptions that end up being communicated
     to the end user, but do not produce error logs """


class NotFoundException(UserFacingExceptions):
    """ this exception should be used if some
     item is not found e.g. the database. """


class BadUserInputException(UserFacingExceptions):
    """ this exception should be used if the user input is not valid. """
