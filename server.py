import argparse
import cv2
from flask import Flask, render_template, Response
from yolo import Yolo

app = Flask(__name__)


@app.route("/video_feed")
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(
        yolo.gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/")
def index():
    # Video streaming home page.
    return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, default="pi", help="input video")
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
