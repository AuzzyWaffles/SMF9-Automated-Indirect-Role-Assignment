import sys
import os


class FilePath:
    def __init__(self):
        self.current_user = os.getlogin()

    def get_persistent_storage_path(self, filename):
        # If the application is frozen (running as a standalone executable)
        if getattr(sys, 'frozen', False):
            temp_path = sys._MEIPASS
            temp_path = os.path.join(temp_path, 'txt\\', filename)
            base_path = f'C:\\Users\\{self.current_user}\\.config\\Koality Rotation\\'

            # If base path isn't on user's PC, make it
            if not os.path.exists(base_path):
                os.makedirs(base_path)

            # If .txt file doesn't exist within base path on user's PC, make it
            if not os.path.exists(base_path + filename):
                with open(f'{base_path}{filename}', 'w') as file:
                    with open(temp_path) as file2:
                        text = file2.read()
                    file.write(text)

            return os.path.join(base_path, filename)

        else:
            # If running in a normal Python environment
            base_path = os.path.dirname(__file__)
            return os.path.join(base_path, 'txt', filename)
