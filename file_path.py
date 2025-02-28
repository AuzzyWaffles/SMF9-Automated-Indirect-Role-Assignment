import os
import sys

current_user = os.getlogin()
if getattr(sys, 'frozen', False):  # If app is running as .exe file
    txt_temp_path = logo_bundle_dir = koala_bundle_dir = sys._MEIPASS
    txt_base_path = f'C:\\Users\\{current_user}\\.config\\Koality Rotator\\'
else:  # If app is running in Pycharm
    txt_base_path = logo_bundle_dir = koala_bundle_dir = None


def get_txt(filename):
    """Gets filepath for specific role permissions depending on whether the app if frozen or running in a normal
    Python environment"""
    if txt_base_path:  # If app is running as .exe file
        if not os.path.exists(txt_base_path):  # If base path isn't on user's PC, make it
            os.makedirs(txt_base_path)

        if not os.path.exists(txt_base_path + filename):  # If file doesn't exist within base path on user's PC, make it
            with open(f'{txt_base_path}{filename}', 'w') as file:
                with open(txt_temp_path) as file2:
                    text = file2.read()
                file.write(text)

        return os.path.join(txt_base_path, filename)

    else:  # If app is running in Pycharm
        temp_txt_base_path = os.path.dirname(__file__)
        return os.path.join(temp_txt_base_path, 'txt', filename)


def get_logo():
    """Gets filepath for Amazon Smile Logo depending on whether the app is frozen or running in a normal Python
    Environment"""
    global logo_bundle_dir
    if not logo_bundle_dir:
        logo_bundle_dir = os.path.dirname(os.path.abspath(__file__))  # If app is running in Pycharm
    image_path = os.path.join(logo_bundle_dir, 'images', 'image1.png')
    return image_path


def get_koala():
    """Gets filepath for Amazon Koala Logo depending on whether the app is frozen or running in a normal Python
        Environment"""
    global koala_bundle_dir
    if not koala_bundle_dir:
        koala_bundle_dir = os.path.dirname(os.path.abspath(__file__))  # If app is running in Pycharm
    image_path = os.path.join(koala_bundle_dir, 'images', 'image2.ico')
    return image_path
