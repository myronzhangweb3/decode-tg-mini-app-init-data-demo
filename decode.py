import base64
import json
import hashlib
import hmac
import os
import sys
from urllib.parse import parse_qs
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


def get_auth_check_string(values):
    param_keys = []

    # 遍历查询参数
    for key, v in values.items():
        if key == "hash":
            continue
        if len(v) != 1:
            raise ValueError("is not a valid auth query")
        param_keys.append(key)

    param_keys.sort()

    data_check_arr = []
    for key in param_keys:
        data_check_arr.append(f"{key}={values[key][0]}")

    return "\n".join(data_check_arr)


def get_hmac256_signature(key, data):
    return hmac.new(key, data, hashlib.sha256).digest()


def decode_auth(auth_header):
    # Base64 decode
    auth_header_bytes = base64.b64decode(auth_header)
    auth_header = auth_header_bytes.decode('utf-8')

    if not auth_header:
        return None

    query = parse_qs(auth_header)
    print(f"auth_header: {json.dumps(query)}")
    hash_value = query.get("hash", [None])[0]
    if not hash_value:
        return None

    auth_check_string = get_auth_check_string(query)
    secret_key = get_hmac256_signature(b"WebAppData", TELEGRAM_BOT_TOKEN.encode())
    expected_hash = get_hmac256_signature(secret_key, auth_check_string.encode())
    expected_hash_string = expected_hash.hex()

    if expected_hash_string != hash_value:
        return None

    # parse user data
    user_data = query.get("user", [None])[0]
    if user_data:
        return json.loads(user_data)

    return None


if __name__ == '__main__':
    auth_data = sys.argv[1]
    print(f"decode result: {decode_auth(auth_data)}")
