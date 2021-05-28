
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## Unreleased

### Added
- Ethereum support
- Bulk retrieval enpoints for addresses and entities
- Entity can have tags on the entity and the address level. Latter are the aggregated tags from contained addresses.

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
