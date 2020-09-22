
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
import datetime 
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
    doc_ref = db.collection('users').document(user_id)

    doc_ref.set({"status": "Standby"})

def getUserInfo(user_id):
    doc_ref = db.collection('users').document(user_id)

    return doc_ref.get().to_dict()

def setUserInfo(user_id, docs):
    doc_ref = db.collection('users').document(user_id)
    
    doc_ref.set(docs)

def setUserStatus(user_id, status="default"):
    docs = getUserInfo(user_id)
    docs['status'] = status
    setUserInfo(user_id, docs)

def getUserStatus(user_id):
    docs = getUserInfo(user_id)
    return docs['status']

def getUserImageList(user_id):

    return [{ "category" : "保健食品",
             "expire_date" : "2022-03-12",
             "file" : "1600489971207.jpg"
              }] #回傳圖片名稱

def generateJson(user_id , imgList):

    jsonContent = {
          "type": "carousel",
          "contents": []
        }

    for item in imgList:
      blob = bucket.blob(user_id + "/" + item['file'])
      category = item['category']
      expire_date = item['expire_date']
      url = "default"
      url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
      
      aCard = {
              "type": "bubble",
              "size": "micro",
              "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "url": "https://i.imgur.com/Zn1Pwbf.jpg"
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "零食甜點",
                    "wrap": True,
                    "weight": "bold",
                    "size": "md"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "text",
                        "text": "2020-09-20",
                        "wrap": True,
                        "weight": "bold",
                        "size": "md",
                        "flex": 0
                      }
                    ]
                  },
                  {
                    "type": "text",
                    "text": "即將到期！",
                    "wrap": True,
                    "size": "sm",
                    "margin": "md",
                    "color": "#ff5551",
                    "flex": 0,
                    "weight": "bold"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "button",
                    "style": "primary",
                    "action": {
                      "type": "message",
                      "label": "已使用完畢",
                      "text": "done"
                    },
                    "height": "sm"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "一週後提醒我",
                      "text": "一週後"
                    },
                    "height": "sm"
                  }
                ]
              },
              "styles": {
                "body": {
                  "backgroundColor": "#D3FFEC"
                },
                "footer": {
                  "backgroundColor": "#D3FFEC"
                }
              }
            }
      
      aCard['hero']['url'] = url
      aCard['body']['contents'][0]['text'] = category
      aCard['body']['contents'][1]['contents'][0]['text'] = expire_date
      
      jsonContent['contents'].append(aCard)

      print(url)

    return jsonContent
      

      

# 問候訊息
@handler.add(FollowEvent)
def handle_follow(event):
    initUserInfo(event.source.user_id)
    text = "哈囉～！歡迎使用滴答提醒。\n\n我可以幫助您記錄容易過期或忘記使用的產品並適時提醒您。\n\n您可以使用選單中的「紀錄品項」可以上傳照片，接著只要輸入日期就能成功紀錄。\n如果您需要查看紀錄的產品與過期日，請點選「查看品項」。"
    sendDefaultMessage(event.reply_token, text)

@handler.add(PostbackEvent)
def handle_postback(event):
    if (getUserStatus(event.source.user_id) == "wait_for_expire_date"):
        docs = getUserInfo(event.source.user_id)
        last_image = docs['image just uploaded']
        doc_ref = db.collection('users').document(event.source.user_id).collection('stocks').document(last_image)
        docs = doc_ref.get().to_dict()
        docs['expire_date'] = event.postback.params['date']
        doc_ref.set(docs)
        setUserStatus(event.source.user_id, "Standby")
        sendDefaultMessage(event.reply_token, "有效日期為「"+event.postback.params['date']+"」，我會在到期前提醒你ㄉ")

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
   
    #從Line的event物件抓資料
    userID = event.source.user_id
    message_type = event.message.type
    msg_from_user = event.message.text
    
    msg_to_user = ""
    message = ""
    items = ["化妝保養品","生鮮食材","冷凍料理","零食甜點","料理用品","保健食品","醫療藥用品"]
    match = False
    for item in items:
      if(msg_from_user == item):
        match = True
        break

    if(getUserStatus(event.source.user_id) == "wait_for_select_category"):
        if(match == True):
            docs = getUserInfo(event.source.user_id)
            last_image = docs['image just uploaded']
            doc_ref = db.collection('users').document(event.source.user_id).collection('stocks').document(last_image)
            doc_ref.set({"category": msg_from_user, "file": last_image})

            msg_to_user = "已將此物品歸類至「" + msg_from_user + "」，請告訴我有效日期。"
            message = TextSendMessage(text=msg_to_user, quick_reply=QuickReply(items=[
                                QuickReplyButton(action=DatetimePickerAction(label="選擇日期", mode="date", data="expire_date"))
                            ]))
            line_bot_api.reply_message(event.reply_token, message)
            setUserStatus(event.source.user_id, "wait_for_expire_date")
    
    elif(msg_from_user == "記錄品項"):
        sendDefaultMessage(event.reply_token)

    elif(msg_from_user == "提醒我"):
        imglist = getUserImageList(userID)
        content = generateJson(userID , imglist)

        message = FlexSendMessage(
            alt_text = "flex message",
            contents = content
            ) 
    
        line_bot_api.reply_message(event.reply_token, message)

    
    
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

        setUserStatus(event.source.user_id, "wait_for_select_category")


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
              "text": "生鮮食材"
            },
            "aspectMode": "cover",
            "aspectRatio": "7.65:10",
            "gravity": "top",
            "url": "https://i.imgur.com/DfBKjG2.png"
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
              "text": "冷凍料理"
            },
            "aspectMode": "cover",
            "aspectRatio": "7.65:10",
            "gravity": "top",
            "url": "https://i.imgur.com/hO3hYW8.png"
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
              "text": "零食甜點"
            },
            "aspectMode": "cover",
            "aspectRatio": "7.65:10",
            "gravity": "top",
            "url": "https://i.imgur.com/iXJ2LYM.png"
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
              "text": "料理用品"
            },
            "aspectMode": "cover",
            "aspectRatio": "7.65:10",
            "gravity": "top",
            "url": "https://i.imgur.com/6nQMDds.png"
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
              "text": "保健食品"
            },
            "aspectMode": "cover",
            "aspectRatio": "7.65:10",
            "gravity": "top",
            "url": "https://i.imgur.com/karOgVl.png"
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
              "text": "醫療藥用品"
            },
            "aspectMode": "cover",
            "aspectRatio": "7.65:10",
            "gravity": "top",
            "url": "https://i.imgur.com/seM9Ff3.png"
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
