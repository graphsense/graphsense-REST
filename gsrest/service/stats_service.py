from datetime import datetime
from gsrest.db.cassandra import get_session
from openapi_server.models.currency_stats import CurrencyStats
from openapi_server.models.stats_ledger import StatsLedger
from openapi_server.models.stats_ledger_version import StatsLedgerVersion


def get_currency_statistics(currency, version=None):
    session = get_session(currency, 'transformed')
    query = "SELECT * FROM summary_statistics LIMIT 1"
    result = session.execute(query).one()
    if result is None:
        raise ValueError('statistics for currency {} not found'
                         .format(currency))
    tstamp = datetime.utcfromtimestamp(result.timestamp) \
        .strftime("%Y-%m-%d %H:%M:%S")
    return CurrencyStats(
            name=currency,
            no_blocks=result.no_blocks,
            no_address_relations=result.no_address_relations,
            no_addresses=result.no_addresses,
            no_entities=result.no_clusters,
            no_txs=result.no_transactions,
            no_labels=result.no_tags,
            timestamp=result.timestamp,
            tools=[],
            notes=[],
            data_sources=[StatsLedger(
                visible_name=currency.upper() + ' Blockchain',
                id=currency + '_ledger',
                version=StatsLedgerVersion(
                    nr=str(result.no_blocks), timestamp=tstamp),
                report_uuid=currency + '_ledger')]
        )
