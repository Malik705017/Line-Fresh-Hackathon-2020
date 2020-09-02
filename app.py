
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
from firebase_admin import storage

# 引用私密金鑰
cred = credentials.Certificate("line--countdown-firebase-adminsdk-e43zw-fd20d58e12.json")

# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(credential= cred, options={"storageBucket": "line--countdown.appspot.com"})

# 初始化firestore
db = firestore.client()
bucket = storage.bucket()

# -------------------------------連接Firebase資料庫 end-------------------------------- #

# --------------------------------引用其他套件 start------------------------------------ #

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

    # 印出event內容
    print(body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


def sendDefaultMessage(reply_token, text=""):
    msg_to_user = text 
    if msg_to_user:
        msg_to_user = msg_to_user + '\n'
    msg_to_user = msg_to_user + "上傳照片以加入提醒清單"
    message = TextSendMessage(text=msg_to_user, quick_reply=QuickReply(items=[
                                QuickReplyButton(action=CameraAction(label="拍照上傳")),
                                QuickReplyButton(action=CameraRollAction(label="從手機上傳"))
                            ]))
    line_bot_api.reply_message(reply_token, message)

def initUserInfo(user_id):
    doc_ref = db.collection(user_id).document('User Info')

    doc_ref.set({"status": "Standby"})

def getUserInfo(user_id):
    doc_ref = db.collection(user_id).document('User Info')

    return doc_ref.get().to_dict()

def setUserInfo(user_id, docs):
    doc_ref = db.collection(user_id).document('User Info')
    
    doc_ref.set(docs)

def setUserStatus(user_id, status="default"):
    docs = getUserInfo(user_id)
    docs['status'] = status
    setUserInfo(user_id, docs)

def getUserStatus(user_id):
    docs = getUserInfo(user_id)
    return docs['status']

# 問候訊息
@handler.add(FollowEvent)
def handle_follow(event):
    initUserInfo(event.source.user_id)
    sendDefaultMessage(event.reply_token)


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
   
    #從Line的event物件抓資料
    userID = event.source.user_id
    message_type = event.message.type
    msg_from_user = event.message.text
    
    msg_to_user = ""
    message = ""

    if(msg_from_user == "化妝保養品" or msg_from_user == "生鮮食材" or msg_from_user == "零食甜點" or msg_from_user == "醫療藥用品"):
        if(getUserStatus(event.source.user_id) == "Image Uploaded Successfully"):
            docs = getUserInfo(event.source.user_id)
            last_image = docs['image just uploaded']
            doc_ref = db.collection(event.source.user_id).document(last_image)
            doc_ref.set({"category": msg_from_user})

            message = "已將此物品歸類至「" + msg_from_user + "」"
            sendDefaultMessage(event.reply_token, message)
            setUserStatus(event.source.user_id, "Standby")

    
# 處理圖片訊息（接收到圖片訊息時啟動）
@handler.add(MessageEvent, message=ImageMessage)
def handle_img_message(event):
    if getUserStatus(event.source.user_id) == "Standby":
        message_content = line_bot_api.get_message_content(event.message.id)

        temp_file_path = event.source.user_id
        with open(temp_file_path, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)

        file_name = str(event.timestamp) + ".jpg"
        saving_path = str(event.source.user_id) + "/" + file_name
        blob = bucket.blob(saving_path)

        with open(temp_file_path, 'rb') as photo:
            blob.upload_from_file(photo)

        import os
        os.remove(temp_file_path)
        

        docs = getUserInfo(event.source.user_id)
        docs['image just uploaded'] = file_name
        setUserInfo(event.source.user_id, docs)

        setUserStatus(event.source.user_id, "Image Uploaded Successfully")


    #contents = (寫好的json檔案)
    contents =  {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "micro",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "size": "full",
            "action": {      #action定義點下去之後要做什麼動作，這邊是設定message action
              "type": "message",
              "label": "action",
              "text": "化妝保養品"
            },
            "aspectMode": "cover",
            "aspectRatio": "7.65:10",
            "gravity": "top",
            "url": "https://i.imgur.com/n4GTDov.png"
          }
        ],
        "paddingAll": "0px"
      }
    },
        {
      "type": "bubble",
      "size": "micro",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "size": "full",
            "action": {      #action定義點下去之後要做什麼動作，這邊是設定message action
              "type": "message",
              "label": "action",
              "text": "化妝保養品"
            },
            "aspectMode": "cover",
            "aspectRatio": "7.65:10",
            "gravity": "top",
            "url": "https://i.imgur.com/n4GTDov.png"
          }
        ],
        "paddingAll": "0px"
      }
    },
        {
      "type": "bubble",
      "size": "micro",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "size": "full",
            "action": {      #action定義點下去之後要做什麼動作，這邊是設定message action
              "type": "message",
              "label": "action",
              "text": "化妝保養品"
            },
            "aspectMode": "cover",
            "aspectRatio": "7.65:10",
            "gravity": "top",
            "url": "https://i.imgur.com/n4GTDov.png"
          }
        ],
        "paddingAll": "0px"
      }
    },
        {
      "type": "bubble",
      "size": "micro",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "size": "full",
            "action": {      #action定義點下去之後要做什麼動作，這邊是設定message action
              "type": "message",
              "label": "action",
              "text": "化妝保養品"
            },
            "aspectMode": "cover",
            "aspectRatio": "7.65:10",
            "gravity": "top",
            "url": "https://i.imgur.com/n4GTDov.png"
          }
        ],
        "paddingAll": "0px"
      }
    },
        {
      "type": "bubble",
      "size": "micro",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "size": "full",
            "action": {      #action定義點下去之後要做什麼動作，這邊是設定message action
              "type": "message",
              "label": "action",
              "text": "化妝保養品"
            },
            "aspectMode": "cover",
            "aspectRatio": "7.65:10",
            "gravity": "top",
            "url": "https://i.imgur.com/n4GTDov.png"
          }
        ],
        "paddingAll": "0px"
      }
    },
        {
      "type": "bubble",
      "size": "micro",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "size": "full",
            "action": {      #action定義點下去之後要做什麼動作，這邊是設定message action
              "type": "message",
              "label": "action",
              "text": "化妝保養品"
            },
            "aspectMode": "cover",
            "aspectRatio": "7.65:10",
            "gravity": "top",
            "url": "https://i.imgur.com/n4GTDov.png"
          }
        ],
        "paddingAll": "0px"
      }
    },
        {
      "type": "bubble",
      "size": "micro",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "size": "full",
            "action": {      #action定義點下去之後要做什麼動作，這邊是設定message action
              "type": "message",
              "label": "action",
              "text": "化妝保養品"
            },
            "aspectMode": "cover",
            "aspectRatio": "7.65:10",
            "gravity": "top",
            "url": "https://i.imgur.com/n4GTDov.png"
          }
        ],
        "paddingAll": "0px"
      }
    }
  ]
}


    message = FlexSendMessage(
            alt_text = "flex message",
            contents = contents
            ) 
    
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
