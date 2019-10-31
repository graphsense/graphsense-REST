from cassandra.cluster import Cluster

from flask import current_app, g

from gsrest.util.exceptions import MissingConfigError


def init_app(app):
    app.teardown_appcontext(close_db)


def get_cluster():
    if 'ccluster' not in g:
        current_app.logger.info("Creating new Cassandra cluster connection.")
        g.ccluster = Cluster(current_app.config["CASSANDRA_NODES"])

    return g.ccluster


def get_session(currency, keyspace):
    if 'csession' not in g:
        current_app.logger.info("Creating new Cassandra session.")
        cluster = get_cluster()
        g.csession = cluster.connect()

    session = g.csession

    if 'MAPPING' not in current_app.config:
        raise MissingConfigError('Missing config property: MAPPING')
    ks_mapping = current_app.config['MAPPING']
    if currency is None and keyspace == 'tagpacks':
        if 'tagpacks' not in ks_mapping:
            raise MissingConfigError('Missing config property: tagpacks')
        session.set_keyspace(ks_mapping['tagpacks'])
    elif currency is not None and keyspace in ('raw', 'transformed'):
        if currency not in ks_mapping:
            raise MissingConfigError(
                'Unknown currency in config: {}'.format(currency))
        if keyspace == 'raw':
            session.set_keyspace(ks_mapping[currency][0])
        elif keyspace == 'transformed':
            session.set_keyspace(ks_mapping[currency][0])
    else:
        raise ValueError("Invalid keyspace request: {} {}".format(
            currency, keyspace))

    return session


def close_db(e=None):
    current_app.logger.info("Closing cassandra connection.")
    cluster = g.pop('ccluster', None)

    if cluster is not None:
        cluster.shutdown()
