from math import floor
# import ctypes


def calculate_id_group_with_overflow(tx_id: int, bucket_size: int):
    blub = int(floor(float(tx_id) / bucket_size))
    if blub.bit_length() >= 31:
        # downcast to 32bit integer
        # blub = ctypes.c_uint32(blub).value
        blub = (blub + 2**31) % 2**32 - 2**31
    return blub
