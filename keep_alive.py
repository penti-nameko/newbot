# keep_alive.py の例

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Hello! I am alive!"

def run():
    # ホストを '0.0.0.0' に設定して、Renderがアクセスできるようにする
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080)) # PORT環境変数を考慮

def keep_alive():
    t = Thread(target=run)
    t.start()
    print("Keep-aliveサーバーを起動しました。") # このメッセージがログに出ていればOK
