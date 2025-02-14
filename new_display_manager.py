import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import datetime as dt
import sys
import os
from file_path import FilePath
from permissions_manager import PermissionsManager
from uncompliant_finder import UncompliantFinder
from schedule_finder import get_scheduled_associates
from assignment_manager import AssignmentManager


class DisplayManager:
    def __init__(self):
        self.file_path = FilePath()

        # Get site name:
        with open(self.file_path.get_persistent_storage_path('site.txt'), "r") as file:
            self.site = file.read().upper()

        with open(self.file_path.get_persistent_storage_path('saved_shifts.txt'), 'r') as file:
            self.shifts = [shift[:-1] for shift in file.readlines()]

        # Get current datetime
        self.current_time = dt.datetime.now()
        self.year = self.current_time.strftime('%Y')
        self.month = self.current_time.strftime('%m')
        self.day_number = self.current_time.strftime('%d')
        self.hour = self.current_time.strftime('%H')

        # Setup other classes
        self.pm = PermissionsManager()
        self.uf = UncompliantFinder()

        # Create Main Menu Window
        self.window = tk.Tk()
        self.window.title('Koality Rotation')

        # Create a frame to hold the canvas and the scrollbar
        frame = tk.Frame(self.window)
        frame.pack(fill="both", expand=True)

        # Create canvas inside the frame
        self.canvas = tk.Canvas(frame, width=500, height=600, bg='#1399FF')

        # Add a vertical scrollbar
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the canvas to use the scrollbar
        self.canvas.config(yscrollcommand=scrollbar.set)

        # Update the scrollable region after content is added
        self.canvas.bind("<Configure>", lambda event, canvas=self.canvas: self.on_frame_configure())
        self.text = self.canvas.create_text(260, 60,
                                            text='Thanks for using Koality Rotation!\n\nOnce the '
                                                 'browser opens you will need to log in through Midway.\n\nAfter '
                                                 'logging in please don\'t click anything, the app will handle all '
                                                 'browser activity.\n\nPlease fill out the entries below then click '
                                                 'the \'Generate\' button to begin!',
                                            font=("Helvetica", 9, "bold"))

        self.canvas.create_line(0, 120, 500, 120, fill="black", width=2)

        self.dropdown_text = self.canvas.create_text(75, 135, text='Select a Shift:', font=("Helvetica", 12, "bold"))
        self.dropdown_widget = ttk.Combobox(self.window, values=self.shifts)
        self.canvas.create_window(250, 135, window=self.dropdown_widget)

        self.site_text = self.canvas.create_text(435, 135, text=f'Site: {self.site}', font=("Helvetica", 12, "bold"))

        self.date_text = self.canvas.create_text(73, 167, text='Type a Date:', font=("Helvetica", 12, "bold"))
        self.date_entry = ttk.Entry(width=23)
        self.date_entry.insert(0, string=f'{self.month}-{self.day_number}-{self.year}')
        self.canvas.create_window(250, 167, window=self.date_entry)

        # Create a style for ttk.Button
        style = ttk.Style()

        # Configure the button style to increase padding and font size
        style.configure('TButton', padding=(0, 35, 0, 32), font=('Helvetica', 10))

        self.change_site_button = tk.Button(text="Change Site", width=10, command=self.change_site)
        self.change_shifts_button = tk.Button(text='Change Shifts', width=10, command=self.change_shifts)
        self.generate_button = ttk.Button(text="Generate", width=35, command=self.generate_button_click)
        self.permissions_button = ttk.Button(text="Check/Edit Permissions", width=35,
                                             command=self.pm.check_permissions)

        self.canvas.create_window(435, 167, window=self.change_site_button)
        self.canvas.create_window(435, 200, window=self.change_shifts_button)
        self.canvas.create_window(250, 235, window=self.generate_button)
        self.canvas.create_window(250, 420, window=self.permissions_button)

        self.canvas.create_line(0, 480, 500, 480, fill="black", width=2)

        self.add_remove_button = tk.Button(text='Add/Remove Roles',
                                           command=self.add_remove_roles)
        self.canvas.create_window(410, 500, window=self.add_remove_button)

        self.entry_dict = {}

        self.generate_roles()

    def on_frame_configure(self):
        # Update the scrollable region of the canvas whenever the content changes
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def generate_roles(self):
        with open(self.file_path.get_persistent_storage_path(f'saved_roles.txt'), "r") as file:
            self.lines = [line.strip() for line in file.readlines()]
            curr_y = 500

            for line in self.lines:
                self.canvas.create_text(200, curr_y, text=f'{line.upper()}:', font=("Helvetica", 12, "bold"))

                self.entry_dict[f'{line}_entry'] = ttk.Entry(width=2)
                self.entry_dict[f'{line}_entry'].insert(tk.END, string="0")
                self.canvas.create_window(300, curr_y, window=self.entry_dict[f'{line}_entry'])

                curr_y += 50

        self.canvas.pack()
        self.canvas.mainloop()

    def change_site(self):
        self.site = simpledialog.askstring('Change Site', 'Please enter your site:')
        if self.site:
            self.site = self.site.upper()
            with open(self.file_path.get_persistent_storage_path(f'site.txt'), "w") as file:
                file.write(self.site)
            self.canvas.delete(self.site_text)
            self.site_text = self.canvas.create_text(435, 135, text=f'Site: {self.site}',
                                                     font=("Helvetica", 12, "bold"))

    def change_shifts(self):
        messagebox.showinfo(title="Shifts Input", message="Please ensure all shifts are entered as follows:\nHH-MM-00")
        with open(self.file_path.get_persistent_storage_path('saved_shifts.txt'), 'r') as file:
            shifts = ''
            text = file.read()
            shifts += text
            self.text_window = tk.Tk()
            self.text_window.title('Change Shifts')
            text = tk.Text(self.text_window)
            text.insert(tk.END, chars=shifts)

            save_button = ttk.Button(self.text_window, text="Save", width=20,
                                     command=lambda: self.__save(text, 'saved_shifts.txt'))
            save_button.place(x=480, y=10)
            text.pack()
            self.text_window.mainloop()

    def add_remove_roles(self):
        with open(self.file_path.get_persistent_storage_path(f'saved_roles.txt'), "r") as file:
            roles = ''
            text = file.read()
            roles += text

        self.text_window = tk.Tk()
        self.text_window.title("Add/Remove Roles")
        text = tk.Text(self.text_window)
        text.insert(tk.END, chars=roles)

        save_button = ttk.Button(self.text_window, text="Save", width=20,
                                 command=lambda: self.__save(text, 'saved_roles.txt'))
        save_button.place(x=480, y=10)
        text.pack()
        self.text_window.mainloop()

    def __save(self, text, txt):
        saved_text = text.get("1.0", 'end-1c').split('\n')
        saved_text = [item for item in saved_text if item != '']
        with open(self.file_path.get_persistent_storage_path(txt), "w") as file:
            for role in saved_text:
                file.write(role + '\n')

        self.text_window.destroy()
        tk.messagebox.showinfo(title="Saved!",
                               message='Saved!')

        self.window.destroy()
        DisplayManager()

    def generate_button_click(self):
        try:
            for line in self.lines:
                if (int(self.entry_dict[f'{line}_entry'].get())) < 0:
                    messagebox.showinfo(title="Error", message="All role entries must contain valid integers.")
                    return
        except ValueError:
            messagebox.showinfo(title="Error", message="All role entries must contain valid integers.")
            return

        shift = self.dropdown_widget.get()
        if shift not in self.shifts:
            messagebox.showinfo(title="Error", message="Please select a valid shift from the dropdown menu.")
            return

        date = self.date_entry.get()

        try:
            date = dt.datetime(int(date[6:]), int(date[0:2]), int(date[3:5]))
            today = dt.datetime(int(self.year), int(self.month), int(self.day_number))
        except ValueError:
            messagebox.showinfo(title="Error", message="Invalid date entry.\n\nPlease ensure you typed the correct date"
                                                       " and it's formatted as follows: MM/DD/YYYY")
            return

        if not messagebox.askyesno(title="Proceed?", message='Are you sure you would like to proceed?'):
            return

        # Create dictionary saving number of AAs per indirect role
        nums_dict = {line: self.entry_dict[f'{line}_entry'].get() for line in self.lines}

        self.window.destroy()

        # Use imported function to find scheduled associates
        scheduled_associates = get_scheduled_associates(shift, date)

        # If Scheduling Site takes too long to load and returns False
        if not scheduled_associates:
            DisplayManager()
            return

        # Use PermissionsManager method to get txt for each indirect role
        permissions_dict = self.pm.get_permissions()

        # Create final class object
        am = AssignmentManager(permissions_dict, nums_dict, [], scheduled_associates)
        result_string, uncompliant_string, not_enough_string = am.assign_indirects()
        if len(not_enough_string) > 0:
            final_string = not_enough_string + '\n' + result_string + '\n' + uncompliant_string
        else:
            final_string = result_string + '\n' + uncompliant_string

        self.window = tk.Tk()
        self.window.title('Results')
        text = tk.Text(self.window)
        text.insert(tk.END, chars=final_string)
        save_button = tk.Button(self.window, text="Main Menu", width=20, height=4,
                                command=self.main_menu_button_click)
        save_button.place(x=480, y=10)
        text.pack()
        self.window.mainloop()

    def permissions_button_click(self):
        self.pm.check_permissions()

    def main_menu_button_click(self):
        self.window.destroy()
        DisplayManager()


DisplayManager()
