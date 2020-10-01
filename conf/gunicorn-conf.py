timeout = 300
capture_output = True
accesslog = '-'
errorlog = '-'
loglevel = 'debug'
bind = "0.0.0.0:9000"


def post_fork(server, worker):
    server.log.info('Worker spawned (pid: %s)', worker.pid)


def pre_fork(server, worker):
    pass


def pre_exec(server):
    server.log.info('Forked child, re-executing.')


def when_ready(server):
    server.log.info('Server is ready. Spawning workers')
