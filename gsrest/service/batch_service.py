from gsrest.db import get_connection


def batch(currency, batch_operation):
    print(f'operation {batch_operation}')
    return str(batch_operation)
