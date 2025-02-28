import tkinter as tk
from tkinter import ttk, messagebox
import file_path


class PermissionsManager:
    def __init__(self):
        with open(file_path.get_custom_text('saved_roles'), "r") as file:
            self.indirect_roles = [line.strip() for line in file.readlines()]

        self.window = None

    def check_permissions(self):
        permissions_string = ""

        for role in self.indirect_roles:
            with open(file_path.get_permissions(role), "r") as file:
                text = file.read()
                permissions_string += text

        self.window = tk.Tk()
        self.window.title("Check/Edit Permissions")
        self.window.iconbitmap(file_path.get_koala())
        text = tk.Text(self.window)
        text.insert(tk.END, chars=permissions_string)

        save_button = ttk.Button(self.window, text="Save", width=20,
                                 command=lambda: self.__save_permissions(text))
        save_button.place(x=480, y=10)

        # Create a vertical scrollbar
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=text.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the Text widget to use the scrollbar
        text.config(yscrollcommand=scrollbar.set)

        text.pack()
        self.window.mainloop()

    def __save_permissions(self, text):
        saved_permissions = text.get("1.0", 'end-1c').split("##")

        if len(saved_permissions) - 1 != len(self.indirect_roles):
            tk.messagebox.showinfo(title="Error",
                                   message='Error: Changes not saved.\n\nIf you need to add or remove roles, '
                                           'please do so on the main menu by clicking "Add/Remove Roles."')
            self.window.destroy()
            return
        else:
            for n in range(1, len(saved_permissions)):
                saved_permissions[n] = f"##{saved_permissions[n]}"

            saved_permissions_iter = iter(saved_permissions[1:])
            for role in self.indirect_roles:
                with open(file_path.get_permissions(role), "w") as file:
                    file.write(next(saved_permissions_iter))

        self.window.destroy()
        tk.messagebox.showinfo(title="Saved!", message='Permissions Saved!')

    def get_permissions(self):
        permissions_dict = {}
        for role in self.indirect_roles:
            with open(file_path.get_permissions(role), "r") as file:
                text = file.read()
                permissions_dict[role] = text.split("\n")

        return permissions_dict
