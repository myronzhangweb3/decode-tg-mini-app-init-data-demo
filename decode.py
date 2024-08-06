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
    # 创建一个空列表来存储参数键
    param_keys = []

    # 遍历查询参数
    for key, v in values.items():
        if key == "hash":
            continue
        if len(v) != 1:
            raise ValueError("is not a valid auth query")
        param_keys.append(key)

    # 对键进行排序
    param_keys.sort()

    # 创建数据检查数组
    data_check_arr = []
    for key in param_keys:
        data_check_arr.append(f"{key}={values[key][0]}")

    # 返回拼接的字符串
    return "\n".join(data_check_arr)


def get_hmac256_signature(key, data):
    return hmac.new(key, data, hashlib.sha256).digest()


def decode_auth(auth_header):
    # Base64 解码
    auth_header_bytes = base64.b64decode(auth_header)
    auth_header = auth_header_bytes.decode('utf-8')

    if not auth_header:
        return None

    # 解析查询参数
    query = parse_qs(auth_header)
    print(f"auth_header: {json.dumps(query)}")
    # 获取 hash
    hash_value = query.get("hash", [None])[0]
    if not hash_value:
        return None

    # 计算 HMAC
    auth_check_string = get_auth_check_string(query)
    secret_key = get_hmac256_signature(b"WebAppData", TELEGRAM_BOT_TOKEN.encode())
    expected_hash = get_hmac256_signature(secret_key, auth_check_string.encode())
    expected_hash_string = expected_hash.hex()

    if expected_hash_string != hash_value:
        return None

    # 解析用户数据
    user_data = query.get("user", [None])[0]
    if user_data:
        return json.loads(user_data)

    return None


if __name__ == '__main__':
    auth_data = sys.argv[1]
    print(f"decode result: {decode_auth(auth_data)}")
