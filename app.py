from flask import Flask, request, abort

# ---------------------------------創建Line Bot start---------------------------------- #
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('2DmvpJgdmXcSHowzVSWZVfiF3aqsHskszknRMN7yicHtjlpV64tAEglzv9zzaZDA3NUlyciHlR/hmB/paASDE4rOBRb4tUI8a02iphYx5INjcPHrVmnUQc5x/td5TfPVuxSxWyorQPz4Elx1vp0IyAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('7ee8f5c2aa2dc3a9a0dc6e52ed7241a6')
# ---------------------------------創建Line Bot end----------------------------------- #


# ------------------------------連接Firebase資料庫 start------------------------------- #
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# 引用私密金鑰
cred = credentials.Certificate("line--countdown-firebase-adminsdk-e43zw-fd20d58e12.json")

# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(cred)

# 初始化firestore
db = firestore.client()

# -------------------------------連接Firebase資料庫 end-------------------------------- #


# --------------------------------引用其他套件 start------------------------------------ #
import random
import imgdic
# ---------------------------------引用其他套件 end------------------------------------- #


# 監聽所有來自 /callback 的 Post Request
# 我們利用 Python 套件 flask 的幫助，告訴 Heorku，只要有人(以這個例子來說，是 LINE 送來資訊)呼叫 "https://你-APP-的名字.herokuapp.com/callback" ，就執行下列程式碼
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
        msg_to_user = "請到以下網址發問：https://lineask-1c65c.web.app/#/"
        message = TextSendMessage(text=msg_to_user)
    elif(msg_from_user == "貼圖"):
        randNum1 = random.randint(11537, 11549)
        randNum2 = 0
        if(randNum1 == 11537):
            randNum2 = random.randint(52002734, 52002773)
        elif(randNum1 == 11538):
            randNum2 = random.randint(51626494, 51626533)
        elif(randNum1 == 11539):
            randNum2 = random.randint(52114110, 52114149)
        message = StickerSendMessage(
        package_id=str(randNum1),
        sticker_id=str(randNum2)
        )
    elif(msg_from_user == "我的個資"):
        #從Line的event物件抓資料
        userID = event.source.user_id
        message_type = event.message.type
        msg_to_user = "您的ID: "+userID+"\n訊息種類: "+message_type+"\n您傳的訊息是: "+msg_from_user
        message = TextSendMessage(text=msg_to_user)

        doc = {
        'name':userID , 'message':msg_from_user
        }
        # 建立文件 必須給定 集合名稱 文件id
        # 即使 集合一開始不存在 都可以直接使用

        # 語法
        # doc_ref = db.collection("集合名稱").document("文件id")

        doc_ref = db.collection("NTU_students").document("student_01")

        # doc_ref提供一個set的方法，input必須是dictionary

        doc_ref.set(doc)

    elif(msg_from_user.find("問")== 0 and msg_from_user.find(" ")== 1):
        randNum = random.randint(0,100)
        msg_to_user = msg_from_user.replace("問 ","")+"的機率是"+str(randNum)+"%"
        message = TextSendMessage(text=msg_to_user)
    elif(msg_from_user.find("抽")== 0 and msg_from_user.find("卡")== 1 ):
        url = imgdic.returnCard()
        message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
        )
    else:
        pass

    line_bot_api.reply_message(event.reply_token, message)
    


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
