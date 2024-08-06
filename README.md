# Decode Telegram MiniApp InitData

The Telegram MiniApp front-end can get [window.Telegram.WebApp.initData](https://core.telegram.org/bots/webapps#initializing-mini-apps), send this to the back-end for Get user information and perform [authentication](https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app).

This repository provides an example of how to decode `window.Telegram.WebApp.initData`.

## Usage

### Set environment variables

```shell
cp .env.example .env
```

### Install Package

```shell
pip install -r requirements.txt
```

### Run frond end

```shell
cd frontend
sh run.sh
```
> The front-end needs to be mapped to the public network and accessed using https, e.g. using ngrok


### Open WebApp

copy tg_init_data:

![](./doc/tg.png)

### Decode tg_init_data
```shell
python3 decode.py {tg_init_data}
```

Example of output results:
```txt
auth_header: {"user": ["{\"id\":5276611418,\"first_name\":\"Myron\",\"last_name\":\"Zhang\",\"username\":\"myronzhangweb3\",\"language_code\":\"zh-hans\",\"allows_write_to_pm\":true}"], "chat_instance": ["-6348001789302836739"], "chat_type": ["sender"], "auth_date": ["1722948364"], "hash": ["e998259d18711b135e84498b15f2242fe72da41e92488e712a67e93e38512866"]}
decode result: {'id': 5276611418, 'first_name': 'Myron', 'last_name': 'Zhang', 'username': 'myronzhangweb3', 'language_code': 'zh-hans', 'allows_write_to_pm': True}
```