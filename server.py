import argparse
import datetime
import cv2
from threading import Thread
import time

from flask import Flask, render_template, Response, request, redirect

from yolo import *


# import pyrebase
# import json


# with open("auth.json") as f:
#     config = json.load(f)

# firebase = pyrebase.initialize_app(config)
# db = firebase.database()

# password는 암호화해서 넣어야 함.
# 일단 여기서는 했다고 가정.
# signin = {"password": 1234, "username":"heejin"}
# db.child("users").child("kook").set(signin)


app = Flask(__name__)

out = None
rec = False


def record(out):
    while rec:
        out.write(yolo.frame)


@app.route("/video_feed")
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(
        yolo.gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# Video streaming home page.
@app.route("/")
def index():
    global rec
    return render_template("index.html", rec=rec)


# Video streaming home page.
@app.route("/result", methods=["GET", "POST"])
def result():
    global rec, out
    now = datetime.datetime.now()

    if request.method == "POST":
        if request.form["button"][:2] == "녹화":
            rec = not rec
            if rec:
                fourcc = cv2.VideoWriter_fourcc(*"XVID")
                out = cv2.VideoWriter(
                    f"videos/{str(now).replace(':','')}.avi",
                    fourcc,
                    120,
                    (1280, 720),
                )
                thread = Thread(
                    target=record,
                    args=[out],
                )
                thread.start()
                timer = time.time()
                # timed = str(datetime.timedelta(seconds=timer)).split(".")
            else:
                out.release()

        elif request.form["button"] == "캡쳐":
            cv2.imwrite(f"images/{str(now).replace(':','')}.jpeg", yolo.frame)

    # return render_template("index.html", rec=rec, timed=timed)
    return render_template("index.html", rec=rec)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Server gets Raspberry pi's capture through zmq"
    )
    parser.add_argument("--input", type=str, default=0, help="input video")
    parser.add_argument(
        "--weights", type=str, default="data/yolov4_tiny.weights", help="yolo weights"
    )
    parser.add_argument(
        "--configure", type=str, default="data/yolov4_tiny.cfg", help="yolo configure"
    )
    parser.add_argument(
        "--label", type=str, default="data/coco.names", help="coco class label"
    )
    parser.add_argument(
        "--confidence", type=float, default=0.5, help="minimum confidence"
    )
    parser.add_argument(
        "--threshold", type=float, default=0.3, help="minimum threshold"
    )
    args = parser.parse_args()
    yolo = Yolo(args)

    app.run(host="localhost", debug=True, port=3000)
