def get_first_key_present(target_dict, keylist):
    for k in keylist:
        if k in target_dict:
            return target_dict[k]
    raise KeyError(f"Non of the keys {keylist} is present in {target_dict}.")


def is_eth_like(network: str) -> bool:
    return network == 'eth' or network == 'trx'
