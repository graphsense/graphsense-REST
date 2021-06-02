import connexion.problem


def notfound(detail):
    return connexion.problem(404, "Not Found", detail)


def badrequest(detail):
    return connexion.problem(400, "Bad Request", detail)


def internalerror(detail):
    return connexion.problem(500, "Internal Server Error", detail)
