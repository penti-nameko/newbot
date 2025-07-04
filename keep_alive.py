from flask import Flask
from threading import Thread
import os # <--- この行を追加してください

app = Flask('')

@app.route('/')
def home():
    return "Hello! I am alive!"

def run():
    # os.environ.get を使用して安全に PORT を取得します。
    # PORT が設定されていない場合は、デフォルトで 8080 を使用します。
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()
