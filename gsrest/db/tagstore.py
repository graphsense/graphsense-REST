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

    def list_taxonomies(self):
        return self.execute("select * from taxonomy")

    def list_concepts(self, taxonomy):
        return self.execute("select * from concept where taxonomy = %s",
                            [taxonomy])

    def list_address_tags(self,
                          label,
                          show_private=False,
                          page=None,
                          pagesize=None):
        query = f"""select
                        t.*,
                        tp.uri,
                        tp.uri,
                        tp.creator,
                        tp.title,
                        tp.is_public,
                        c.level,
                        acm.gs_cluster_id
                    from
                       tag t,
                       tagpack tp,
                       confidence c,
                       address_cluster_mapping acm
                   where
                       t.tagpack = tp.id
                       and t.confidence = c.id
                       and acm.address=t.address
                       and acm.currency=t.currency
                       {hide_private_condition(show_private)}
                       and t.label = %s """
        return self.execute(query,
                            params=[label],
                            paging_key='t.id',
                            page=page,
                            pagesize=pagesize)

    def list_matching_labels(self,
                             currency,
                             expression,
                             limit,
                             show_private=False):
        currency_condition = "and t.currency = %s" if currency else ""
        params = [currency.upper()] if currency else []
        query = f"""select
                    t.label
                   from
                    tag t,
                    label l,
                    tagpack tp
                   where
                    t.label = l.label
                    and tp.id = t.tagpack
                    {currency_condition}
                    and similarity(l.label, %s) > 0.2
                    {hide_private_condition(show_private)}
                   order by l.label <-> %s
                   limit %s"""
        return self.execute(query,
                            params=params + [expression, expression, limit])

    def list_matching_actors(self, expression, limit, show_private=False):
        query = f"""select
                    a.id,
                    a.label
                   from
                    actor a,
                    actorpack ap
                   where
                    ap.id = a.actorpack
                    and similarity(a.label, %s) > 0.2
                    {hide_private_condition(show_private, 'ap')}
                   order by a.label <-> %s
                   limit %s"""
        return self.execute(query, params=[expression, expression, limit])

    def list_tags_by_address(self,
                             currency,
                             address,
                             show_private=False,
                             page=None,
                             pagesize=None):
        query = f"""select
                        t.*,
                        tp.uri,
                        tp.creator,
                        tp.title,
                        tp.is_public,
                        c.level,
                        acm.gs_cluster_id
                    from
                        tag t,
                        tagpack tp,
                        confidence c,
                        address_cluster_mapping acm
                    where
                        t.tagpack=tp.id
                        and c.id=t.confidence
                        and t.currency = %s
                        and t.address = %s
                        and acm.address=t.address
                        and acm.currency=t.currency
                        {hide_private_condition(show_private)}
                    order by
                        c.level desc
                        """

        address = address.strip()
        if is_eth_like(currency):
            address = address.lower()

        return self.execute(query,
                            params=[currency.upper(), address],
                            paging_key='t.id',
                            page=page,
                            pagesize=pagesize)

    def list_address_tags_by_entity(self,
                                    currency,
                                    entity,
                                    show_private=False,
                                    page=None,
                                    pagesize=None):
        query = f"""select
                        t.*,
                        tp.uri,
                        tp.creator,
                        tp.title,
                        tp.is_public,
                        c.level,
                        acm.gs_cluster_id
                    from
                        tag t,
                        tagpack tp,
                        address_cluster_mapping acm,
                        confidence c
                    where
                        acm.address=t.address
                        and acm.currency=t.currency
                        and c.id=t.confidence
                        and t.currency = %s
                        and acm.gs_cluster_id = %s
                        {hide_private_condition(show_private)}
                        and t.tagpack=tp.id
                    order by
                        c.level desc,
                        t.address asc
                        """

        return self.execute(query,
                            params=[currency.upper(), entity],
                            paging_key='t.id',
                            page=page,
                            pagesize=pagesize)

    async def count_address_tags_by_entity(self,
                                           currency,
                                           entity,
                                           show_private=False):
        query = f"""select
                        sum(count) as count
                    from
                        tag_count_by_cluster
                    where
                        currency = %s
                        and gs_cluster_id = %s
                        {hide_private_condition(show_private, table_alias=None)}"""  # noqa
        return await self.execute(query, [currency.upper(), entity])

    async def get_best_entity_tag(self, currency, entity, show_private=False):
        if is_eth_like(currency):
            # in case of eth we want to propagate the best address tag
            # regardless of if the tagpack is a defines it as cluster definer
            # since cluster == entity in eth
            cluster_definer_condition = ""
        else:
            cluster_definer_condition = """and
                            (cd.is_cluster_definer=true
                                AND t.is_cluster_definer=true
                            OR
                            cd.is_cluster_definer=false
                                AND t.is_cluster_definer!=true
                        )"""

        query = f"""select
                        t.*,
                        tp.uri,
                        tp.creator,
                        tp.title,
                        tp.is_public,
                        cd.gs_cluster_id,
                        c.level
                   from
                        tag t,
                        tagpack tp,
                        address_cluster_mapping acm,
                        cluster_defining_tags_by_frequency_and_maxconfidence cd,
                        confidence c
                   where
                        cd.gs_cluster_id=acm.gs_cluster_id
                        and cd.currency = acm.currency
                        and cd.label = t.label
                        and cd.max_level = c.level
                        and acm.address=t.address
                        and t.currency = acm.currency
                        and cd.currency = %s
                        and cd.gs_cluster_id = %s
                        and t.tagpack=tp.id
                        and t.address=cd.address
                        {cluster_definer_condition}
                        and c.id = t.confidence
                        {hide_private_condition(show_private, table_alias='cd')}
                   order by
                        cd.max_level desc,
                        cd.no_addresses desc,
                        cd.is_cluster_definer desc,
                        t.address desc
                   limit 1"""  # noqa

        return await self.execute(query, [currency.upper(), entity])

    async def list_labels_for_addresses(self,
                                        currency,
                                        addresses,
                                        show_private=False):
        if not addresses:
            raise TypeError('x')
            return Result(), None

        if is_eth_like(currency):
            addresses = tuple(addr.lower().strip() for addr in addresses)
        else:
            addresses = tuple(addr.strip() for addr in addresses)

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
        return await self.execute(query, params=[currency.upper(), addresses])

    async def list_actors_address(self, currency, address, show_private=False):
        if not address:
            raise TypeError('x')
            return Result(), None
        query = f"""select
                    distinct t.actor as id, ac.label as label
                   from
                    tag t,
                    actor ac,
                    tagpack tp
                   where
                    t.actor = ac.id
                    and t.tagpack = tp.id
                    and t.currency = %s
                    and t.address = %s
                    {hide_private_condition(show_private)}
                    order by label"""
        return await self.execute(query, params=[currency.upper(), address])

    async def list_labels_for_entities(self,
                                       currency,
                                       entities,
                                       show_private=False):
        if not entities:
            return Result(), None
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
        return await self.execute(query, params=[currency.upper(), entities])

    async def list_actors_entity(self, currency, entity, show_private=False):
        if not entity:
            return Result(), None
        query = f"""select
                    distinct t.actor as id, ac.label as label
                   from
                    tag t,
                    actor ac,
                    address_cluster_mapping acm,
                    tagpack tp
                   where
                    t.address = acm.address
                    and t.tagpack = tp.id
                    and t.currency = acm.currency
                    and acm.currency = %s
                    and acm.gs_cluster_id = %s
                    and ac.id = t.actor
                    {hide_private_condition(show_private)}
                    order by label"""
        return await self.execute(query, params=[currency.upper(), entity])

    async def get_actor(self, actor_id):
        query = "SELECT * FROM actor WHERE id=%s"
        return await self.execute(query, params=[actor_id])

    async def get_actor_categories(self, actor_id):
        query = (
            "SELECT actor_categories.*,concept.label FROM "
            "actor_categories, concept "
            "WHERE actor_categories.category_id = concept.id and actor_id=%s")
        return await self.execute(query, params=[actor_id])

    async def get_actor_jurisdictions(self, actor_id):
        query = (
            "SELECT actor_jurisdictions.*,concept.label FROM "
            "actor_jurisdictions, concept "
            "WHERE actor_jurisdictions.country_id = concept.id and actor_id=%s"
        )
        return await self.execute(query, params=[actor_id])

    async def get_nr_of_tags_by_actor(self, actor_id):
        query = "SELECT count(*) FROM tag WHERE actor=%s"
        return await self.execute(query, params=[actor_id])

    def list_address_tags_for_actor(self,
                                    actor_id,
                                    show_private=False,
                                    page=None,
                                    pagesize=None):
        query = f"""select
                        t.*,
                        tp.uri,
                        tp.creator,
                        tp.title,
                        tp.is_public,
                        c.level,
                        acm.gs_cluster_id
                    from
                       tag t,
                       tagpack tp,
                       confidence c,
                       address_cluster_mapping acm
                   where
                       t.tagpack = tp.id
                       and t.confidence = c.id
                       and acm.address=t.address
                       and acm.currency=t.currency
                       {hide_private_condition(show_private)}
                       and t.actor = %s """
        return self.execute(query,
                            params=[actor_id],
                            paging_key='t.id',
                            page=page,
                            pagesize=pagesize)

    def count(self, currency, show_private=False):
        query = """
            select
                no_labels,
                no_implicit_tagged_addresses as no_tagged_addresses
            from
                statistics tp
            where
                currency = %s"""
        return self.execute(query, params=[currency.upper()])
