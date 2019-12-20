# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
