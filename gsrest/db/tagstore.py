import aiopg
import hashlib


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


async def to_result(cursor, paging_key=None):
    rows = await cursor.fetchall()
    columns = {}
    i = 0
    for c in cursor.description:
        columns[c.name] = i
        i += 1
    result = Result(rows, columns)
    le = len(result)
    if paging_key is None:
        paging_key = cursor.description[0].name
    else:
        pos = paging_key.find('.') + 1
        paging_key = paging_key[pos:]
    next_page = None if le == 0 else result[le - 1][paging_key]

    return result, next_page


def hide_private_condition(show_private):
    return 'and tp.is_public=true' \
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
        dsn = f"dbname={config['database']} user={config['username']}"\
              f" password={config['password']} host={config['host']}"\
              f" port={config['port']}"

        async def on_connect(conn):
            async with conn.cursor() as cur:
                await cur.execute(
                    f"set search_path to {self.config['schema']}")

        self.pool = await aiopg.create_pool(
            dsn,
            maxsize=config['max_connections'],
            on_connect=on_connect,
            timeout=config['query_timeout'])

    def id(self):
        h = self.config['database'] +\
                    self.config['host'] +\
                    self.config['username']
        h = h.encode('utf-8')
        return hashlib.md5(h).hexdigest()

    async def close(self):
        self.pool.terminate()
        await self.pool.wait_closed()

    async def execute(self, query, params=None, paging_key=None, page=None,
                      pagesize=None):
        if params is None:
            params = []
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                if page and paging_key:
                    if "where" not in query.lower():
                        query += " where"
                        andd = ""
                    else:
                        andd = "and"

                    order = f" {andd} {paging_key} > %s "
                    pos = query.lower().find("order by")
                    if pos == -1:
                        query += order
                    else:
                        query = query[0:pos] + order + query[pos:]
                    params.append(page)
                if "order" not in query.lower() and paging_key:
                    query += f" order by {paging_key}"
                if pagesize:
                    query += f" limit {pagesize}"

                self.logger.debug(f'{query} {params}')
                await cur.execute(query, params)
                return await to_result(cur, paging_key)

    def list_taxonomies(self):
        return self.execute("select * from taxonomy")

    def list_concepts(self, taxonomy):
        return self.execute("select * from concept where taxonomy = %s",
                            [taxonomy])

    def list_address_tags(self, currency, label, show_private=False,
                          page=None, pagesize=None):
        query = f"""select t.*, tp.is_public from
                       tag t,
                       tagpack tp
                   where
                       t.tagpack = tp.id
                       {hide_private_condition(show_private)}
                       and t.currency = %s
                       and t.label = %s """
        return self.execute(query,
                            params=[currency.upper(), label],
                            paging_key='t.id',
                            page=page,
                            pagesize=pagesize)

    def list_entity_tags(self, currency, label, show_private=False,
                         page=None, pagesize=None):
        query = f"""select distinct on (acm.gs_cluster_id)
                    t.*,
                    acm.gs_cluster_id,
                    tp.is_public
                   from
                    tag t,
                    tagpack tp,
                    address_cluster_mapping acm
                   where
                    t.tagpack = tp.id
                    {hide_private_condition(show_private)}
                    and t.currency = %s
                    and t.label = %s
                    and t.is_cluster_definer = true
                    and t.address = acm.address
                    and t.currency = acm.currency
                   order by
                    acm.gs_cluster_id, t.confidence desc"""

        return self.execute(query,
                            params=[currency.upper(), label],
                            paging_key='acm.gs_cluster_id',
                            page=page,
                            pagesize=pagesize)

    def list_matching_labels(self, currency, expression, limit,
                             show_private=False):
        query = f"""select
                    t.label
                   from
                    tag t,
                    label l,
                    tagpack tp
                   where
                    t.label = l.label
                    and tp.id = t.tagpack
                    and t.currency = %s
                    and similarity(l.label, %s) > 0.2
                    {hide_private_condition(show_private)}
                   order by l.label <-> %s
                   limit %s"""
        return self.execute(query,
                            params=[currency.upper(),
                                    expression,
                                    expression,
                                    limit])

    def list_tags_by_address(self, currency, address, show_private=False,
                             page=None,
                             pagesize=None):
        query = f"""select t.*, tp.is_public from
                        tag t,
                        tagpack tp
                   where
                        t.tagpack=tp.id
                        and t.currency = %s
                        and t.address = %s
                        {hide_private_condition(show_private)}
                        """

        return self.execute(query,
                            params=[currency.upper(), address],
                            paging_key='t.id',
                            page=page,
                            pagesize=pagesize)

    def list_address_tags_by_entity(self, currency, entity, show_private=False,
                                    page=None, pagesize=None):
        query = f"""select t.*, tp.is_public from
                        tag t,
                        tagpack tp,
                        address_cluster_mapping acm
                   where
                        acm.address=t.address
                        and t.currency = %s
                        and acm.gs_cluster_id = %s
                        {hide_private_condition(show_private)}
                        and t.tagpack=tp.id"""

        return self.execute(query,
                            params=[currency.upper(), entity],
                            paging_key='t.id',
                            page=page,
                            pagesize=pagesize)

    def list_entity_tags_by_entity(self, currency, entity, show_private=False):
        query = f"""select
                        t.*,
                        tp.is_public,
                        acm.gs_cluster_id
                   from
                        tag t,
                        tagpack tp,
                        address_cluster_mapping acm
                   where
                        acm.address=t.address
                        and t.is_cluster_definer = true
                        and t.currency = acm.currency
                        and t.currency = %s
                        and acm.gs_cluster_id = %s
                        and t.tagpack=tp.id
                        {hide_private_condition(show_private)}
                   order by
                        t.confidence desc
                   limit 1"""

        # TODO also order by frequency

        return self.execute(query, [currency.upper(), entity])

    def list_labels_for_addresses(self, currency, addresses,
                                  show_private=False):
        if not addresses:
            return Result()
        query = f"""select
                    t.address,
                    json_agg(distinct t.label) as labels
                   from
                    tag t,
                    tagpack tp
                   where
                    t.tagpack = tp.id
                    and t.currency = %s
                    and t.address in %s
                    {hide_private_condition(show_private)}
                   group by address
                   order by address"""
        return self.execute(query,
                            params=[currency.upper(), addresses])

    def list_labels_for_entities(self, currency, entities, show_private=False):
        if not entities:
            return Result()
        query = f"""select
                    acm.gs_cluster_id,
                    json_agg(distinct t.label) as labels
                   from
                    tag t,
                    tagpack tp,
                    address_cluster_mapping acm
                   where
                    t.address = acm.address
                    and t.currency = acm.currency
                    and t.is_cluster_definer = true
                    and acm.currency = %s
                    and acm.gs_cluster_id in %s
                    and tp.id = t.tagpack
                    {hide_private_condition(show_private)}
                   group by
                    acm.gs_cluster_id
                   order by acm.gs_cluster_id"""
        return self.execute(query,
                            params=[currency.upper(), entities])

    def count(self, currency, show_private=False):
        hide_private_condition = "is_public = true" \
            if not show_private \
            else "is_public is null"
        query = f"""
            select
                no_labels,
                no_tagged_addresses
            from
                statistics tp
            where
                currency = %s
                and {hide_private_condition}"""
        return self.execute(query,
                            params=[currency.upper()])
