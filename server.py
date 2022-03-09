import argparse
import datetime
from datetime import datetime
import cv2
from threading import Thread

from flask import Flask, render_template, Response, request
import json

# local
from yolo import *
import firebase_work as fb


app = Flask(__name__)

# video_output: output of video recording
# rec: recording status
video_output = None
rec = False



# APP Token 받은 후 app-token.json 파일 생성
@app.route("/get_token", methods=['POST'])
def get_token():
    if request.method == 'POST':
        request_data = json.loads(request.data.decode('utf-8'))
        with open('app-token.json', 'w') as file:
            json.dump(request_data, file)
    return ""



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
                    f"videos/{str(now).replace(':','')}.avi",
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
            # storage에 저장
            # fb.storagePush("video", video_name)

        elif request.form["button"] == "캡쳐":
            cv2.imwrite(f"images/{str(now).replace(':','')}.jpeg", yolo.frame)
            print("캡쳐 완료")
            # storage에 저장
            # fb.storagePush("photo", img_name)

        elif request.form["button"] == "예약녹화":
            start_time = request.form["scheduler"][:19]
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

            end_time = request.form["scheduler"][22:]
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            video_output = cv2.VideoWriter(
                f"videos/{str(now).replace(':','')}.avi",
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
    parser.add_argument(
        "--frame", type=int, default=50, help="threshold of frame count"
    )
    args = parser.parse_args()
    yolo = Yolo(args)

    app.run(host="localhost", debug=True, port=3000)
