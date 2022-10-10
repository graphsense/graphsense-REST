# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [22.10] - 2022-10-07
### Added
- `only_ids` filter for `list_address_neighbors`
- address status field (possible status: clean, dirty, new)
- fetch address status from special delta updater tables
- `direction` to `list_address_txs` and `list_entity_txs` to filter transactions whether they are incoming or outgoing
### Changed
- fetch last synced block from delta updater tables for currency statistics
- show specific error message of eth address with no external txs

## [1.0.1] - 2022-08-26
### Added
- add port to config template
### Changed
- fix `best_address_tag` output in bulk
- improve bulk error message
- enforce max page size for `list_address_tags_by_entity`
- improve tagstore paging (by limit and offset)
- improve `search_neighbors` by entities and addresses
- fix fetching best address tag for single address clusters and multiple tags
- fix display of labels in neighbor list
- pass context to plugins
- fix error wrapping multiple tagstores

## [1.0.0] - 2022-07-13
Also see the changelog of the [OpenAPI specification](https://github.com/graphsense/graphsense-openapi/blob/master/CHANGELOG.md) for any changes to the API.
### Added
- Option to run tests in docker
- add pool_recycle tagstore parameter
### Changed
- make type errors run in "internal server error"
- majority vote on entity tag selection , #75
- fix sorting labels in search result by search term similarity
- handle empty arguments in bulk
- hide tagpack uri for private tagpacks

## [0.5.2] - 2022-03-21
### Added
- add logging config and SMTP logging
- plugin architecture to hook into request processing
- integrate external Tagstores on top of PostgreSQL
- config parameter for filtering private tags by HTTP header
- fuzzy label search
- add number of tagged addresses to statistics
- add `is_cluster_definer` tag property
- add `root_address` entity property
### Changed
- improved bulk retrieval error messages
- retrieve just one tag per entity
- fix `list_entity_links`
- catch NaNs from Cassandra
### Removed
- tag retrieval from Cassandra 

## [0.5.1] - 2021-11-30
### Added
- Service for requesting data from other endpoints in bulk (CSV and JSON)
- Redesign algorithm for retrieving the transactions between two addresses/entities
- Automatically reconnect to DB
- Listing entity transactions
- Endpoint for getting inputs/outputs of a transaction
- Minor performance improvements
- Bux fixes
### Changed
- Webserver from Flask to AIOHttp to support asynchronous request handling
- Tag response model
- Consider entity tags only in deep search for entity neighbors
### Removed
- Tag coherence
- CSV variants of routes in favour of new bulk interface
- Retrieving arbitrary lists of things (list_entities, list_addresses, list_blocks, list_txs)
- Metadata from stats endpoint response

## [0.5.0] 2021-06-02
### Added
- Ethereum support
- Bulk retrieval endpoints for addresses and entities
- Entity can have tags on the entity and the address level.
  Latter are the aggregated tags from contained addresses.
### Changed
- Fetch entity/address with tags optionally
- Calculate tag coherence optionally

## [0.4.5] 2020-11-18

Complete rewrite on top of a [Connexion](https://github.com/zalando/connexion)
server stub generated through [OpenAPI Generator](https://openapi-generator.tech)
given the [Graphsense OpenAPI specification](https://github.com/graphsense/graphsense-openapi).

### Added
- CSV variants of entity/addresses, address/txs and address/links
- integration tests of services against cassandra mockup db instance
- check keyspace existence on startup
- database layer abstraction
### Changed
- changed instance config format to YAML
- changed interface of entity neighbor search endpoint
- changed response of addresses/links endpoint
### Removed
- authentication (to be handled by a proxy)

## [0.4.4] 2020-06-16
### Added
- calculate tag coherence of entities
- add targets filter for neighbors endpoint, fix #33
- CSV download is streamed

## [0.4.3] 2020-05-11
### Added
- Updated Docker base image
- Added gunicorn config file
- Fix swagger UI behind reverse proxy (ProxyFix from werkzeug), fix \#24
- New "search neighbors" options
- List of transactions between one address and its neighbor
- More information from `stats` call
### Changed
- Improved and documented handling of config files
- Harmonized logging in user db (now via app_context logger)
- `tags` namespace replaced `labels` and taxonomy integration

## [0.4.2] - 2019-12-20
### Added
- Checks on input values
### Changed
- Major restructuring and refactoring of API
- Use Gunicorn instead of uWSGI

## [0.4.1] - 2019-07-01
### Changed
- `config.json` contains not only currencies, but also `tagpacks` keyspace
- Currency statistics are now available at `<api_root>/stats` (previously at `<api_root>/`)
### Added
- Query label and label search (for suggestions)
- Unit tests
- Swagger documentation
- JWT Authentication
- Number of labels in statistics
- `start_develop.sh`
- CSV export of txs, tags and neighbors
### Removed
- Egonet calls 

## [0.4.0] - 2019-02-01
### Changed
- Adjustments for new dashboard implementation
- Removed `srcCategory`/`dstCategory` in address/cluster relations
- Fixed exchange rates bug (EUR/USD swapped)
- Run Docker container as non-root user
### Added
- Added primitive tests

## [0.3.3] - 2018-12-06
### Changed
- Reimplementation using Python/Flask
### Added
- Summary statistics of available currencies in root path
- Support for multiple currencies (e.g., `localhost:9000/btc/...`)
- Transactions call (random samples)
- Blocks call (random samples)
- Exchange rates call 
