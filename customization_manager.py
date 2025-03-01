import file_path


def change_site(site):
    """Opens entry box to allow user to change site ID"""
    with open(file_path.get_custom_text('site'), "w") as file:
        file.write(site)


def get_shifts():
    """Opens text box to allow user to change shift start times"""
    with open(file_path.get_custom_text('saved_shifts'), 'r') as file:
        shifts = file.read()
        return shifts


def add_remove_roles():
    """Opens text box to allow user to add/remove roles"""
    with open(file_path.get_custom_text('saved_roles'), "r") as file:
        text = file.read()
        return text


def save(filename, text):
    """Saves content in Add/Remove Roles text box"""
    with open(file_path.get_custom_text(filename), "w") as file:
        for line in text:
            file.write(line + '\n')


