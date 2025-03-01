import file_path


def get_site():
    """Opens site.txt and returns site ID"""
    with open(file_path.get_custom_text('site'), "r") as file:
        site = file.read()
        return site


def get_shifts():
    """Opens saved_shifts.txt and returns all shifts"""
    with open(file_path.get_custom_text('saved_shifts'), 'r') as file:
        shifts = file.read()
        return shifts


def get_roles():
    """Opens saved_roles.txt and returns all roles"""
    with open(file_path.get_custom_text('saved_roles'), "r") as file:
        text = file.read()
        return text


def save(filename, text):
    """Writes text in files for given filename and text arguments"""
    with open(file_path.get_custom_text(filename), 'w') as file:
        for line in text:
            file.write(line + '\n')
