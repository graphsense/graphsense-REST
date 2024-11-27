import aiopg
import hashlib
from gsrest.util import is_eth_like


class Result:

    def __init__(self, rows=None, columns=None):
        if rows is None:
            rows = []
        if columns is None:
            columns = {}
        self.rows = rows
        self.columns = columns

    def __iter__(self):
        self.pointer = 0
        return self

    def __next__(self):
        if self.pointer >= len(self.rows):
            raise StopIteration
        self.pointer += 1
        return self[self.pointer - 1]

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, i):
        return Row(self.rows[i], self.columns)


class Row:

    def __init__(self, row, columns):
        self.row = row
        self.columns = columns

    def __getitem__(self, key):
        return self.row[self.columns[key]]


async def to_result(logger, cursor, page=None, pagesize=None):
    rows = await cursor.fetchall()
    logger.debug(f'result size {len(rows)}')
    columns = {}
    i = 0
    for c in cursor.description:
        columns[c.name] = i
        i += 1
    result = Result(rows, columns)
    le = len(result)
    next_page = None if page is None or not pagesize or le < pagesize \
        else int(page) + pagesize

    return result, next_page


def hide_private_condition(show_private, table_alias='tp'):
    prefix = table_alias + '.' if table_alias else ''
    return f'and {prefix}is_public=true' \
        if not show_private else ''


class Tagstore:

    def __init__(self, config, logger):
        self.logger = logger
        self.config = config

    async def connect(self):
        config = self.config
        config['database'] = config.get('database', 'tagstore')
        config['username'] = config.get('username', 'tagstore')
        config['password'] = config.get('password', 'tagstore')
        config['schema'] = config.get('schema', 'tagstore')
        config['host'] = config.get('host', 'localhost')
        config['port'] = int(config.get('port', 5432))
        config['query_timeout'] = int(config.get('query_timeout', 300))
        config['max_connections'] = int(config.get('max_connections', 10))
        config['pool_recycle'] = int(config.get('pool_recycle', 3600))
        dsn = f"dbname={config['database']} user={config['username']}"\
              f" password={config['password']} host={config['host']}"\
              f" port={config['port']}"

        async def on_connect(conn):
            self.logger.debug('Tagstore connect')
            async with conn.cursor() as cur:
                await cur.execute(f"set search_path to {self.config['schema']}"
                                  )

        self.pool = await aiopg.create_pool(
            dsn,
            maxsize=config['max_connections'],
            on_connect=on_connect,
            timeout=config['query_timeout'],
            pool_recycle=config['pool_recycle'])

    def id(self):
        h = self.config['database'] +\
            self.config['host'] +\
            self.config['username']
        h = h.encode('utf-8')
        return hashlib.md5(h).hexdigest()

    async def close(self):
        self.pool.terminate()
        await self.pool.wait_closed()

    async def execute(self,
                      query,
                      params=None,
                      paging_key=None,
                      page=0,
                      pagesize=None):
        if params is None:
            params = []
        async with self.pool.acquire() as conn:
            self.logger.debug(f'pool size {self.pool.size}, freesize'
                              f' {self.pool.freesize}')
            async with conn.cursor() as cur:
                if pagesize:
                    query += " limit %s"
                    params.append(pagesize)
                if not page:
                    page = 0
                query += " offset %s"
                params.append(page)

                self.logger.debug(f'{query} {params}')
                await cur.execute(query, params)
                return await to_result(self.logger, cur, page, pagesize)
