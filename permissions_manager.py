import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from file_path import FilePath


class PermissionsManager:
    def __init__(self):
        self.indirect_roles = ['eol', 'ps', 'dt', 'ws', 'refurb', 'unload']
        self.window = None
        self.file_path = FilePath()

    def check_permissions(self):
        permissions_string = ""

        for role in self.indirect_roles:
            with open(self.file_path.get_persistent_storage_path(f'{role}.txt'), "r") as file:
                text = file.read()
                permissions_string += text
        self.window = tk.Tk()
        self.window.title("Check/Edit Permissions")
        text = tk.Text(self.window)
        text.insert(tk.END, chars=permissions_string)

        save_button = ttk.Button(self.window, text="Save", width=20,
                                 command=lambda: self.__save_permissions(text))
        save_button.place(x=480, y=10)
        text.pack()
        self.window.mainloop()

    def __save_permissions(self, text):
        saved_permissions = text.get("1.0", 'end-1c').split("##")
        saved_permissions.remove("")

        for n in range(len(saved_permissions)):
            saved_permissions[n] = f"##{saved_permissions[n]}"

        saved_permissions_iter = iter(saved_permissions)
        for role in self.indirect_roles:
            with open(self.file_path.get_persistent_storage_path(f'{role}.txt'), "w") as file:
                file.write(next(saved_permissions_iter))

        self.window.destroy()
        tk.messagebox.showinfo(title="Saved!", message='Permissions Saved!')

    def get_permissions(self):
        permissions_dict = {}
        for role in self.indirect_roles:
            with open(self.file_path.get_persistent_storage_path(f'{role}.txt'), "r") as file:
                text = file.read()
                permissions_dict[role] = text.split("\n")

        return permissions_dict

    def add_remove_roles(self):
        with open(self.file_path.get_persistent_storage_path(f'saved_roles.txt'), "r") as file:
            roles = ''
            text = file.read()
            roles += text
        self.window = tk.Tk()
        self.window.title("Add/Remove Roles")
        text = tk.Text(self.window)
        text.insert(tk.END, chars=roles)

        save_button = ttk.Button(self.window, text="Save", width=20,
                                 command=lambda: self.__save_roles(text))
        save_button.place(x=480, y=10)
        text.pack()
        self.window.mainloop()

    def __save_roles(self, text):
        saved_permissions = text.get("1.0", 'end-1c').split('\n')
        saved_permissions = [item for item in saved_permissions if item != '']
        with open(self.file_path.get_persistent_storage_path(f'saved_roles.txt'), "w") as file:
            for role in saved_permissions:
                file.write(role + '\n')

        self.window.destroy()
        tk.messagebox.showinfo(title="Saved!",
                               message='Roles Saved!\nYou\'ll need to restart the program to see changes.')
