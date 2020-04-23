timeout = 300
capture_output = True
accesslog = '/home/dockeruser/gunicorn-access.log'
errorlog = '/home/dockeruser/gunicorn-error.log'
loglevel = 'debug'
bind = "0.0.0.0:9000"
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
}

def post_fork(server, worker):
    server.log.info('Worker spawned (pid: %s)', worker.pid)

def pre_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info('Forked child, re-executing.')

def when_ready(server):
    server.log.info('Server is ready. Spawning workers')
