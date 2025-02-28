import os
import sys

current_user = os.getlogin()
if getattr(sys, 'frozen', False):  # If app is running as .exe file
    temp_path = sys._MEIPASS
    base_path = f'C:\\Users\\{current_user}\\.config\\Koality Rotator'
else:  # If app is running in Pycharm
    temp_path = None
    base_path = os.path.dirname(__file__)


def app_init():
    """Gets filepath for specific role permissions depending on whether the app is frozen or running in a normal
        Python environment"""
    if temp_path:  # Execute function only if app is running as .exe file
        if not os.path.exists(base_path):  # If base path isn't on user's PC, make it
            os.makedirs(base_path)
        file_path = os.path.join(base_path, 'txt')
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        files = ['End of Line.txt', 'Problem Solve.txt', 'Waterspider.txt', 'Refurb.txt', 'Unload.txt', 'Detrash.txt',
                 'saved_roles.txt', 'saved_shifts.txt', 'site.txt']

        for filename in files:
            full_path = os.path.join(file_path, filename)
            full_temp_path = os.path.join(temp_path, 'txt', filename)

            if not os.path.exists(full_path):  # If file doesn't exist in base path on PC
                with open(full_path, 'w') as file:
                    with open(os.path.join(full_temp_path)) as file2:
                        text = file2.read()
                    file.write(text)


def get_permissions(role):
    """Gets filepath for specific role permissions. Creates it if it doesn't exist."""
    file_path = os.path.join(base_path, 'txt', f'{role}.txt')
    if not os.path.exists(file_path):  # If file doesn't exist in base path on PC
        with open(file_path, 'w') as file:
            file.write(f'## {role} Permissions\nEnter Logins Here\n\n')
    return file_path


def get_custom_text(file):
    """Gets filepath for custom files such as saved_roles, saved_shifts, or site ID."""
    file_path = os.path.join(base_path, 'txt', f'{file}.txt')
    return file_path


def get_logo():
    """Gets filepath for Amazon Smile Logo depending on whether the app is frozen or running in a normal Python
    Environment"""
    if temp_path:
        logo_image_path = os.path.join(temp_path, 'images', 'image1.png')
    else:
        logo_image_path = os.path.join(base_path, 'images', 'image1.png')
    return logo_image_path


def get_koala():
    """Gets filepath for Amazon Koala Logo depending on whether the app is frozen or running in a normal Python
        Environment"""
    if temp_path:
        koala_image_path = os.path.join(temp_path, 'images', 'image2.ico')
    else:
        koala_image_path = os.path.join(base_path, 'images', 'image2.ico')
    return koala_image_path
