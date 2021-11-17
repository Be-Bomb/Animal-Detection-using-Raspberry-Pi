import socket
import time
from imutils.video import VideoStream
import imagezmq
import argparse


def main(args):
    # connect_to='tcp://각자 노트북 ip주소 입력:5555'
    sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(args.ip))

    rpi_name = socket.gethostname()  # send RPi hostname with each image

    picam = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)  # allow camera sensor to warm up

    while True:  # send images as stream until Ctrl-C
        image = picam.read()
        sender.send_image(rpi_name, image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=None, type=str, required=True, help="ip")
    args = parser.parse_args()

    main(args)
