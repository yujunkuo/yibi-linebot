# Import Packages
import os
from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MemberJoinedEvent, TextSendMessage

# API Interface
app = Flask(__name__)

# Environment
load_dotenv()

# LINE Bot Info
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# Default Function
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# LINE Bot Auto-Reply
@handler.add(MemberJoinedEvent)
def echo(event):
    greeting_message = '''
    歡迎新朋友❤️❤️❤️
    ❶請詳閱記事本公告🪧
    ❷相簿產品都是精選必推
    ❸官網自行下單或截圖私訊我
    ————————————
    ·全館🈵千免運
    ·未滿千運費7-11 $35/宅配$80
    ·可轉帳、linepay
    ————————————
    🔍追蹤我IG: _yibi.yaya
    截圖至官方帳號
    https://lin.ee/UXrVtzk
    →贈「好友禮」+「老客人禮」
    ————————————
    ⚠️取貨請錄影維護彼此權益
    ⚡️快電商加盟私訊我🫶🏻
    🛒我的賣場連結
    https://yibishare.c2cbuy.com
    '''
    line_bot_api.reply_message(
        event.reply_token, 
        TextSendMessage(text=greeting_message))

# Main
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)