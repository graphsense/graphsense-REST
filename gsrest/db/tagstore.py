import aiopg
import hashlib


class Result:
    def __init__(self, rows, columns):
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
        config['port'] = config.get('port', 5432)
        dsn = f"dbname={config['database']} user={config['username']}"\
              f" password={config['password']} host={config['host']}"\
              f" port={config['port']}"
        self.pool = await aiopg.create_pool(dsn)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"set search_path to {config['schema']}")

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

                    query += f" {andd} {paging_key} > %s"
                    params.append(page)
                if paging_key:
                    query += f" order by {paging_key}"
                if pagesize:
                    query += f" limit {pagesize}"
                await cur.execute(query, params)
                return await to_result(cur, paging_key)

    def list_taxonomies(self):
        return self.execute("select * from taxonomy")

    def list_concepts(self, taxonomy):
        return self.execute("select * from concept where taxonomy = %s",
                            [taxonomy])

    def list_address_tags(self, currency, label, page=None, pagesize=None):
        query = """select t.*, tp.is_public from
                       tag t,
                       tagpack tp
                   where
                       t.tagpack = tp.id
                       and t.currency = %s
                       and t.label ilike %s """
        return self.execute(query,
                            params=[currency, label + '%'],
                            paging_key='t.id',
                            page=page,
                            pagesize=pagesize)

    def list_entity_tags(self, currency, label, page=None, pagesize=None):
        query = """select
                    t.*,
                    acm.gs_cluster_id as cluster_id,
                    tp.is_public
                   from
                    tag t,
                    tagpack tp,
                    address_cluster_mapping acm
                   where
                    t.tagpack = tp.id
                    and t.address = acm.address
                    and t.currency = acm.currency
                    and t.is_cluster_definer = true
                    and t.currency = %s
                    and t.label ilike %s"""

        return self.execute(query,
                            params=[currency, label + '%'],
                            paging_key='t.id',
                            page=page,
                            pagesize=pagesize)

    def list_matching_labels(self, currency, expression, limit):
        query = """select label from tag
                   where
                    currency = %s
                    and label ilike %s
                   limit %s"""
        return self.execute(query,
                            params=[currency, expression + '%', limit])

    def list_tags_by_address(self, currency, address, page=None,
                             pagesize=None):
        query = """select t.*, tp.is_public from
                        tag t,
                        tagpack tp
                   where
                        t.tagpack=tp.id
                        and t.currency = %s
                        and t.address = %s"""

        return self.execute(query,
                            params=[currency, address],
                            paging_key='t.id',
                            page=page,
                            pagesize=pagesize)

    def list_address_tags_by_entity(self, currency, entity, page=None,
                                    pagesize=None):
        query = """select t.*, tp.is_public from
                        tag t,
                        tagpack tp,
                        address_cluster_mapping acm
                   where
                        acm.address=t.address
                        and t.currency = %s
                        and acm.gs_cluster_id = %s
                        and t.tagpack=tp.id"""

        return self.execute(query,
                            params=[currency, entity],
                            paging_key='t.id',
                            page=page,
                            pagesize=pagesize)

    def list_entity_tags_by_entity(self, currency, entity, page=None,
                                   pagesize=None):
        query = """select
                        t.*,
                        tp.is_public,
                        acm.gs_cluster_id as cluster_id
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
                        and t.tagpack=tp.id"""

        return self.execute(query,
                            params=[currency, entity],
                            paging_key='t.id',
                            page=page,
                            pagesize=pagesize)

    def list_labels_for_addresses(self, currency, addresses):
        query = """select address, json_agg(label) as labels from tag
                   where
                    currency = %s
                    and address in %s
                   group by address
                   order by address"""
        return self.execute(query,
                            params=[currency, addresses])

    def list_labels_for_entities(self, currency, entities):
        query = """select
                    acm.gs_cluster_id as cluster_id,
                    json_agg(t.label) as labels
                   from
                    tag t,
                    address_cluster_mapping acm
                   where
                    t.address = acm.address
                    and t.currency = acm.currency
                    and t.is_cluster_definer = true
                    and acm.currency = %s
                    and acm.gs_cluster_id in %s
                   group by acm.gs_cluster_id
                   order by acm.gs_cluster_id"""
        return self.execute(query,
                            params=[currency, entities])







"""
# list tags by address
# cql: SELECT * FROM address_tags WHERE address_id = %s
# sql:
select t.*, l.label, a.address, tp.is_public from
    tag t,
    address a,
    tagpack tp,
    label l
where
    t.address_id=a.id
    and t.tagpack_id=tp.id
    and t.label_id = l.id
    and a.currency = %s
    and a.address = %s

# list entity tags by entity
# cql: SELECT * FROM cluster_tags WHERE cluster_id_group = %s and cluster_id = %s
# sql:
select t.*, l.label, acm.gs_cluster_id as cluster_id, tp.is_public from
    tag t,
    tagpack tp,
    address_cluster_mapping acm,
    label l,
    address a
where
    acm.address_id=t.address_id
    and t.label_id = l.id
    and acm.gs_cluster_id = %s
    and t.tagpack_id=tp.id
    and t.is_cluster_definer = true
    and t.address_id = a.id
    and a.currency = %s

# list address tags by entity
# cql: SELECT * FROM cluster_address_tags WHERE cluster_id_group = %s and cluster_id = %s
# sql:
select t.*, l.label, a.address, tp.is_public from
    tag t,
    tagpack tp,
    address_cluster_mapping acm,
    label l,
    address a
where
    acm.address_id=t.address_id
    and t.label_id = l.id
    and t.address_id = a.id
    and acm.gs_cluster_id = %s
    and t.tagpack_id=tp.id
    and a.currency = %s

# include labels
# cql: select cluster_id, label from cluster_tags where cluster_id_group = %s and cluster_id = %s
# sql:
select t.label, l.label, acm.gs_cluster_id as cluster_id, tp.is_public from
    tag t,
    tagpack tp,
    address_cluster_mapping acm,
    label l
where
    acm.address_id=t.address_id
    and t.label_id = l.id
    and acm.gs_cluster_id = %
    and t.tagpack_id=tp.id
    and t.is_cluster_definer = true

# list address tags
# cql: SELECT * FROM address_tag_by_label WHERE label_norm_prefix = %s and label_norm = %s
# sql:

select t.*, a.address, a.currency, l.label, tp.is_public from
    tag t,
    tagpack tp,
    address a
where
    t.label_id = l.id
    and t.tagpack_id = tp.id
    and t.address_id = a.id

# without fuzzy search
    and l.label ilike 'xy%'

# with fuzzy search:

    order by %s <-> l.label
    limit 10


# list cluster tags
# cql: SELECT * FROM cluster_tag_by_label WHERE label_norm_prefix = %s and label_norm = %s

select t.*, a.currency, acm.gs_cluster_id as cluster_id, l.label, tp.is_public from
    tag t,
    tagpack tp,
    address_cluster_mapping acm,
    address a
where
    t.label_id = l.id
    and t.tagpack_id = tp.id
    and t.address_id = acm.address_id
    and acm.address_id = a.id
    and t.is_cluster_definer = true

# without fuzzy search
    and l.label ilike 'xy%'

# with fuzzy search:

    order by %s <-> l.label
    limit 10



# list concepts

select * from concepts where taxonomy = %s;

# list taxonomonies
select * from taxonomy;

# schema changes:

# naming conventions:
alter table tag rename column address to address_id;
alter table tag rename column confidence to confidence_id;
alter table tag rename column tagpack to tagpack_id;
alter table concept rename column taxonomy to taxonomy_id;

# because might not be very informative:
alter table address drop column created;

# indices:
create index tag_address_index on tag (address_id);
create index tag_tagpack_index on tag (tagpack_id);
create index tag_is_cluster_definer_index on tag (is_cluster_definer);
create index acm_gs_cluster_id_index on address_cluster_mapping (gs_cluster_id);

# normalize label, probably better for label search:
create table label (
   id SERIAL PRIMARY KEY,
   label VARCHAR NOT NULL
);
alter table tag drop column label;
alter table tag add column label_id integer references label(id);
create index label_index on label (label);
"""
