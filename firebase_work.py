import pyrebase
import firebase_admin
from firebase_admin import credentials
from datetime import timedelta
import json

cred = credentials.Certificate("service-account-file.json")
f = open('config.json')
config = json.load(f)
f.close()

firebase_admin.initialize_app(cred)
firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()

def storagePush(type, name, today_date):
    date_format = today_date.strftime("%Y%m%d")
    if type == "video":
        storage.child(f"videos/{date_format}/{name}").put(f"videos/{date_format}/{name}")
    elif type == "photo":
        storage.child(f"images/{date_format}/{name}").put(f"images/{date_format}/{name}")

def storageRemove(today_date):
    remove_date = (today_date  - timedelta(1)).strftime("%Y%m%d")
    # 디렉토리 자체를 삭제
    storage.delete(f"videos/{remove_date}")
    storage.delete(f"images/{remove_date}")

