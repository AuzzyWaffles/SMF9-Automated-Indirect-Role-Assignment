import file_path

with open(file_path.get_custom_text('saved_roles'), "r") as file:
    indirect_roles = [line.strip() for line in file.readlines()]

    def check_permissions():
        permissions_string = ""

        for role in indirect_roles:
            with open(file_path.get_permissions(role), "r") as file:
                text = file.read()
                permissions_string += text
        return permissions_string


    def save_permissions(text):
        saved_permissions = text.get("1.0", 'end-1c').split("##")

        if len(saved_permissions) - 1 != len(indirect_roles):
            return False
        else:
            for n in range(1, len(saved_permissions)):
                saved_permissions[n] = f"##{saved_permissions[n]}"

            saved_permissions_iter = iter(saved_permissions[1:])
            for role in indirect_roles:
                with open(file_path.get_permissions(role), "w") as file:
                    file.write(next(saved_permissions_iter))
            return True

    def get_permissions():
        permissions_dict = {}
        for role in indirect_roles:
            with open(file_path.get_permissions(role), "r") as file:
                text = file.read()
                permissions_dict[role] = text.split("\n")

        return permissions_dict
