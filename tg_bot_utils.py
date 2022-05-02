import os


def clean_folder():
    for root, dirs, files in os.walk('./pics/', topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def pre_start_work():
    if not os.path.exists('./pics'):
        os.mkdir('./pics')
    clean_folder()
    os.environ["APIKEY"] = "683989153:AAFplDb83gWdBPS0c0OLmK9GX4tZw4U9Cjc"
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
