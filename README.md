# TimerBot
這是一個專門計時的聊天機器人

## Setup

### Prerequisite
* Python 3
* graphviz

#### Install Dependency
```sh
pip install -r requirements.txt
```

* pygraphviz (For visualizing Finite State Machine)
    * [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)

### Secret Data
建立一個叫做 config.py 的檔案在主目錄下，內容為
```
TELEGRAM_API_TOKEN = 'YOUR_TELEGRAM_API_TOKEN'
TELEGRAM_WEBHOOK_URL = 'YOUR_TELEGRAM_WEBHOOK_URL'
```	
`TELEGRAM_API_TOKEN` and `TELEGRAM_WEBHOOK_URL` in .py **MUST** be set to proper values.
Otherwise, you might not be able to run your code.

### Run Locally
You can either setup https server or using `ngrok` as a proxy.

**`ngrok` would be used in the following instruction**

```sh
ngrok http 5000
```

After that, `ngrok` would generate a https URL.

You should set `TELEGRAM_WEBHOOK_URL` (in config.py) to `https://your-https-URL/hook`.

#### Run the sever
```sh
python3 app.py
```

### Run on my Server

Find @TimerTaskBot on the Telegram and you can run it if my server is opened. I have a server that can run for a long time.

## Finite State Machine
![fsm](./img/fsm.png)

## Usage


## Author
[張頌宇](https://github.com/timcsy)
成大資訊系108級 F74046462
