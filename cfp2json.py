import configparser
import json
import re

def infer_type(val: str):
    v = val.strip()
    lower = v.lower()
    if lower in ('true', 'yes', 'on'):
        return True
    if lower in ('false', 'no', 'off'):
        return False
    if re.fullmatch(r'\d+', v):
        return int(v)
    if re.fullmatch(r'\d+\.\d*', v):
        return float(v)
    return v

def ini_to_json(input_path: str, output_path: str):
    cfg = configparser.ConfigParser()
    cfg.read(input_path)

    data = {}
    # Include DEFAULT as its own section if you like; otherwise just iterate cfg.sections()
    for section in cfg.sections():
        items = cfg.items(section)
        data[section] = {key: infer_type(val) for key, val in items}

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)



f1 = "eg.ini"
f2 = "eg.json"   

ini_to_json(f1, f2)