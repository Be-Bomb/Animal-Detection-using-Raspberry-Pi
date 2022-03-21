import os
import glob
import datetime


def remove_outdated_files():
    today_date = datetime.date.today()
    remove_date = today_date - datetime.timedelta(days=2)

    images_path = os.path.join(os.getcwd(), "static", "images", "*.jpeg")
    videos_path = os.path.join(os.getcwd(), "static", "videos", "*.avi")

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


def get_detected_images():
    images_path = os.path.join(os.getcwd(), "static", "images", "*.jpeg")
    images = glob.glob(images_path)
    images = sorted(images)

    file_list = []
    for image in images:
        file_name_splited = os.path.split(image)
        directory, file_name = file_name_splited[-2], file_name_splited[-1]
        file_list.append("images/" + file_name)

    return file_list
