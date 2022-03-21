import datetime
import cv2

from utils import opts, handling_file
from yolo import Yolo

from threading import Thread
from flask import Flask, render_template, Response, request, session


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
app.secret_key = "인천대학교 컴퓨터공학과 캡스톤디자인 Be Bomb"


# video_output: output of video recording
# rec: recording status
video_output = None
rec = False


def record(video_output):
    iter = 0
    while rec:
        if iter % 500 == 0:
            print("녹화 중 ...")

        video_output.write(yolo.frame)
        iter += 1


def reserve_record(video_output, start_time, end_time):
    now = datetime.datetime.now()
    iter = 0

    while start_time <= now and now <= end_time:
        if iter % 500 == 0:
            print("예약녹화 중 ...")
        video_output.write(yolo.frame)

        now = datetime.datetime.now()
        iter += 1

    video_output.release()
    print("예약녹화 완료")


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
    global rec, video_output
    now = datetime.datetime.now()

    if request.method == "POST":
        if request.form["button"][:2] == "녹화":
            rec = not rec
            if rec:
                fourcc = cv2.VideoWriter_fourcc(*"XVID")
                video_output = cv2.VideoWriter(
                    f"static/videos/{str(now).replace(':','')}.avi",
                    fourcc,
                    120,
                    (yolo.frame.shape[1], yolo.frame.shape[0]),
                )
                thread = Thread(
                    target=record,
                    args=[video_output],
                )
                thread.start()
            else:
                video_output.release()
                print("녹화 완료")

        elif request.form["button"] == "캡쳐":
            cv2.imwrite(f"static/images/{str(now).replace(':','')}.jpeg", yolo.frame)
            print("캡쳐 완료")

        elif request.form["button"] == "예약녹화":
            start_time = request.form["scheduler"][:19]
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

            end_time = request.form["scheduler"][22:]
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            video_output = cv2.VideoWriter(
                f"static/videos/{str(now).replace(':','')}.avi",
                fourcc,
                120,
                (yolo.frame.shape[1], yolo.frame.shape[0]),
            )
            thread = Thread(
                target=reserve_record,
                args=[video_output, start_time, end_time],
            )
            thread.start()

    return render_template("index.html", rec=rec)


@app.route("/data_chart")
def data_chart():
    return yolo.json if hasattr(yolo, "json") else "Data Chart"


@app.route("/get_images")
def get_images():
    session.clear()

    handling_file.remove_outdated_files()
    file_list = handling_file.get_detected_images()
    if file_list:
        session["imageName"] = file_list
    return "get images"


if __name__ == "__main__":
    handling_file.remove_outdated_files()
    opt = opts.parse_opt()
    yolo = Yolo(opt)

    app.run(host="localhost", debug=True, port=3000)
