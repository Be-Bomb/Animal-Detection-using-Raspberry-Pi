import os
import glob
import datetime


def remove_file():
    today_date = datetime.date.today()
    remove_date = today_date - datetime.timedelta(days=2)

    images_path = os.path.join(os.getcwd(), "images/*.jpeg")
    videos_path = os.path.join(os.getcwd(), "videos/*.avi")

    images = glob.glob(images_path)
    videos = glob.glob(videos_path)

    for image in images:
        ctime = os.path.getmtime(image)
        ctime = datetime.date.fromtimestamp(ctime)

        if remove_date > ctime:
            os.remove(image)

    for video in videos:
        ctime = os.path.getmtime(video)
        ctime = datetime.date.fromtimestamp(ctime)

        if remove_date > ctime:
            os.remove(video)
