from math import floor


def calculate_id_group_with_overflow(tx_id: int, bucket_size: int):
    blub = int(floor(float(tx_id) / bucket_size))
    if blub.bit_length() >= 32:
        # downcast to 32bit integer
        blub = (blub + 2**31) % 2**32 - 2**31
    return blub
