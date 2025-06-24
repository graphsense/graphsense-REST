# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).


## [25.07.0/1.12.0] - 2025-06-??

### added
- token_currency filter option for links endpoint
- min/max_date for all endpoints supporting min/max_height to directly filter by date
- added user reported tags endpoint to submit new tags


## [25.06.1/1.11.3] - 2025-06-04

### fixed
- bug loading with _T0 zero index logs or token txs.

## [25.06.0/1.11.2] - 2025-06-02

### added
- added database.list_address_txs_ordered_legacy config to switch back to old list_address_txs_ordered function used e.g. in address and entity links in case of issues with the new one.

### fixed
- Rework and speed up slow list_address_txs_ordered function which means faster link functions and neighbor search.
- fixed on ios without addresses on links endpoint

## [25.05.1/1.11.1] - 2025-05-15

### added
- added database.block_by_date_use_linear_search config option for testing purposes (disables binary search for blocks)

### fixed
- reverted fixed ambiguity eth internal and external txs (#476) - caused problems for the frontend and old gs files

## [25.05.0/1.11.0] - 2025-05-2

### changed
- Search now also returns token and sub tx (traces in eth) ids, iif search yields on result otherwise.
- keyspace autodiscovery now uses blockheight in summary table to select latest keyspace, not only ks name

### fixed
- fixed ambiguity eth internal and external txs (#476)
- tagpack-tool division by zero if label contains only filler words
- user input validation and error messages


## [25.03.0/1.10.0] - 2025-03-14

### changed
- tags are now fetched without currency filter.

### fixed
- fixed regression on utxo self loops on address links.


## [25.01.5/1.9.5] - 2025-01-30

### fixed
- eth filtering txs in eth if blocks have not txs -> min/max tx id failed in some cases.
- bumped tagstore dependency

## [25.01.4/1.9.4] - 2025-01-20

### fixed
- fix connection cleanup for tagstore


## [25.01.3/1.9.3] - 2025-01-20

### fixed
- get_entities for tags fails on nonsensical tags

## [25.01.2/1.9.2] - 2025-01-20

### fixed
- limit parameter not passed to address search


## [25.01.1/1.9.1] - 2025-01-14

### fixed
- bumped tagstore dependency to v25.01.1; fixing best cluster tag queries.

## [25.01.0/1.9.0] - 2025-01-10

### New

- Updated to v25.01.0 of the tagstore only works with newer versions than this (Resync of database needed)
- tagstore is now a direct lib dependency, no duplication of query code anymore
- gs-rest now supports keyspace auto discovery (using the latest complete (summary stats has data) ks in cassandra)

### Changed
- now uses uv to package and dep. mgmt, ruff for linting and formatting
- tests now use testcontainers for more robust/quicker testing setup

## [24.11.2] - 2024-12-03

### Fixed

- Return concepts with tags

## [24.11.1] - 2024-11-27

### Added

- added parameters `include_nonstandard_io` and `include_io_index` for endpoints `/{currency}/txs/{tx_hash}` and `/{currency}/txs/{tx_hash}/{io}` (by default false)

## [24.11.0] - 2024-11-20

### Added

- added parameter `include_actors` for endpoint `/{currency}/addresses/{address}/entity` (by default true)

## [24.10.1] - 2024-10-30

### Fixed
- missing eth/tron address sub-transaction when paging
- missing bulk-endpoints list_token_txs, get_spent_in_txs, get_sending_txs, get_block_by_date, get_tag_summary_by_address

## [24.10.0] - 2024-10-18

### Added

- added endpoiont `/{currency}/addresses/{address}/tag_summary` to fetch a condensed summary of tags on an address
- added endpoint `/{currency}/block_by_date/{date}` to get nearest blocks given a timestamp
- syntax to load token transactions and traces via the `/{currency}/txs/{tx_hash}` endpoint.
- consistent availability of include_actor on all address related endpoints (to improve performance)

### Fixed
- missing links between two addresses on rare occasions (when there was not net outflow for one address).


## [24.04.1]

### Fixed
- unhandled error on bad page token in tags endpoint


## [24.04.0]

### Added

- added parameters `min_height`, `max_height` and `order` to `list_address_links` and `list_entity_links` to limit retrieved txs.

## [24.02.3] - 2024-03-15

### Fixed
- Listing txs between addresses (list_address_txs)

## [24.02.2] - 2024-03-14

- Listing txs between addresses (list_address_txs)

## [24.02.1] - 2024-03-06

### Fixed
- fixed tron address search

## [24.02.0] - 2024-02-29

### Fixed
- address search in account model currencies

### Added
- added parameter `order` to `list_address_txs` and `list_entity_txs` to control sort order of returned list of transactions

## [24.01.3] - 2024-02-22

### Fixed
- Incomplete retrieval of address transactions

## [24.01.2] - 2024-02-09

### Fixed
- support flat block transaction table in eth keyspaces

## [24.01.1] - 2024-01-25

### Fixed
- patched documentation
- openapi spec fix
- remove generation of graphsense-python
- add volume to ratelimiting-redis
- mount openapi as dir

## [24.01.0] - 2024-01-10

### Added
- added support for the tron currency and its tokens
- config option to configure read consistency level
### Fixed
- ordering issues on fetching transactions on address/entity and neighbor level

## [23.09] - 2023-09-20

### Added
- added new endpoints to query tx-graph (dependencies between transactions in utxo currencies /{currency}/txs/{tx_hash}/spent_in and /{currency}/txs/{tx_hash}/spending)
- added support for missing current exchange rates (for sync states before exchange rates where avail.)
### Changed
- changed minimal search key length to 2 (only searches tags and actors)
- changed keyspaces names for testing to avoid conflicts
- fixed propagating unknown exception to the user ([#92](https://github.com/graphsense/graphsense-REST/issues/92))
- fixed linting in github action ([94](https://github.com/graphsense/graphsense-REST/issues/94))
- fixed exception on unknown currency  ([93](https://github.com/graphsense/graphsense-REST/issues/93))


## [23.06] - 2023-06-12
### Changed
- fix new du v1 address not found in /address/{addr}/entity endpoint
- reenabled returning logos from coingecko
- fix search for tx hashes with 0x prefix (closes [#4](https://github.com/graphsense/graphsense-ethereum-etl/issues/4))
- fix search of all zero tx hashes or addresses
- add compatibilty to new tx_reference field in eth-like keyspaces [#8](https://github.com/graphsense/graphsense-ethereum-transformation/issues/8)
- concurrency limit for some bulk requests to avoid overloading db


## [23.03] - 2023-03-28
### Added
- Support for actors to collect tags under the umbrella of their real world controller
- new endpoints /tags/actors/{actor_id} - get actor by id
- new endpoint /tags/actors/{actor_id}/tags - list of tags belonging to the actor
- support search for any category neighbor [#329](https://github.com/graphsense/graphsense-dashboard/issues/329)
- added parameters `min_height`/`max_height` to /addresses/{address}/txs and /entities/{entity}/txs endpoints to allow for range queries
- added flag `include_actors` to /entities/{entity} and /entities/{entity}/neighbors endpoints
- added flag `exclude_best_address_tag` to /entities/{entity} and /entities/{entity}/neighbors endpoints to omit fetching the best address tag

## [23.01] - 2023-12-30
### Added
- Token Support for Ethereum stable coin tokens (WETH, USDT, USDC)
- new API Endpoints /{currency}/token_txs/{tx_hash} to receive token transactions per hash
- new Endpoint /{currency}/supported_tokens to list supported tokens and their parameters.
- Entity and Address txs endpoints now return token transactions
- Entities contain token balances, and other token related aggregated statistics
- Ethereum addresses now contain a field is_contract
- Neighbor endpoints return aggregated token statistics
- Rates endpoint returns rates for token currencies
### Changes
- Fixed handling of contract creation transactions (no to_address)

## [22.11] - 2022-11-25
### Added
- Entity tag tests
- Entity neighbor search limited to max. 5 min
### Changes
- Fixed selection of best address tag
- Improve error message on bad paging state value
- Raise not found error for retrieving entity of non existing eth address
- Performance improvements for entity neighbor search
- Performance improvements for `get_rates`
- Improve entity tag resolution.

## [22.10] - 2022-10-10
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
