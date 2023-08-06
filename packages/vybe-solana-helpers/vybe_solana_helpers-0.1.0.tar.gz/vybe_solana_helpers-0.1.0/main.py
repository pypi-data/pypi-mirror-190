from json import dumps
from vybe_solana_helpers import rust_decimal_raw_parts_to_string


param = {"flags": 2148007936, "hi": 0, "lo": 2000000, "mid": 0}
c = result = rust_decimal_raw_parts_to_string(param["lo"], param["mid"], param["hi"], param["flags"])
print(c)
