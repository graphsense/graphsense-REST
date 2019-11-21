from cassandra.cluster import Cluster
from cassandra.query import named_tuple_factory

from flask import current_app, g, abort

from gsrest.util.exceptions import MissingConfigError


def init_app(app):
    app.teardown_appcontext(close_db)


def get_cluster():
    if 'ccluster' not in g:
        current_app.logger.info("Creating new Cassandra cluster connection.")
        g.ccluster = Cluster(current_app.config["CASSANDRA_NODES"])

    return g.ccluster


def get_keyspace_mapping_definition():
    if 'MAPPING' not in current_app.config:
        raise MissingConfigError('Missing config property: MAPPING')
    return current_app.config['MAPPING']


def get_supported_currencies():
    ks_mapping = get_keyspace_mapping_definition()
    return dict(filter(lambda elem: elem[0] != 'tagpacks',
                       ks_mapping.items())).keys()


def get_keyspace_mapping(currency, keyspace_type):
    ks_mapping = get_keyspace_mapping_definition()
    if currency is None and keyspace_type == 'tagpacks':
        if 'tagpacks' not in ks_mapping:
            raise MissingConfigError('Missing config property: tagpacks')
        return ks_mapping['tagpacks']
    elif currency is not None and keyspace_type in ('raw', 'transformed'):
        if currency not in ks_mapping:
            abort(404, 'Unknown currency in config: {}'.format(currency))
        if keyspace_type == 'raw':
            return ks_mapping[currency][0]
        elif keyspace_type == 'transformed':
            return ks_mapping[currency][1]
    else:
        raise ValueError("Invalid keyspace request: {} {}".format(
            currency, keyspace_type))


def get_session(currency, keyspace_type):
    if 'csession' not in g:
        current_app.logger.info("Creating new Cassandra session.")
        cluster = get_cluster()
        g.csession = cluster.connect()

    session = g.csession
    # enforce standard row factory (can be overridden on service-level)
    session.row_factory = named_tuple_factory

    keyspace = get_keyspace_mapping(currency, keyspace_type)
    session.set_keyspace(keyspace)

    return session


def close_db(e=None):
    current_app.logger.info("Closing cassandra connection.")
    cluster = g.pop('ccluster', None)

    if cluster is not None:
        cluster.shutdown()
