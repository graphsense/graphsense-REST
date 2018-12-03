from graphsenserest import app as application
from graphsensedao import connect
from uwsgidecorators import postfork


@postfork
def postfork_connect():
    connect(application)


if __name__ == "__main__":
    # deactivate debug and multiple processes in production
    # because of memory usage and security
    # host='0.0.0.0',port='8888'
    application.run(debug=False, processes=1)
