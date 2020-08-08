from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import random

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('2DmvpJgdmXcSHowzVSWZVfiF3aqsHskszknRMN7yicHtjlpV64tAEglzv9zzaZDA3NUlyciHlR/hmB/paASDE4rOBRb4tUI8a02iphYx5INjcPHrVmnUQc5x/td5TfPVuxSxWyorQPz4Elx1vp0IyAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('7ee8f5c2aa2dc3a9a0dc6e52ed7241a6')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 自己加的
    print(body)
    
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg_from_user = event.message.text
    msg_to_user = ""
    message = ""
    if(msg_from_user == "我要發問"):
        msg_to_user = "請輸入您的問題"
        message = TextSendMessage(text=msg_to_user)
    elif(msg_from_user == "我要貼圖"):
        randNum1 = random.randint(11537, 11539)
        randNum2 = 0
        if(randNum1 == 11537):
            randNum2 = random.randint(52002734, 52002773)
        elif(randNum1 == 11538):
            randNum2 = random.randint(51626494, 51626533)
        else:
            randNum2 = random.randint(52114110, 52114149)
        message = StickerSendMessage(
        package_id=str(randNum1),
        sticker_id=str(randNum2)
        )
    elif(msg_from_user == "我要圖片"):
        message = ImageSendMessage(
        original_content_url='https://example.com/original.jpg',
        preview_image_url='https://example.com/preview.jpg'
        )   

    line_bot_api.reply_message(event.reply_token, message)
    


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
