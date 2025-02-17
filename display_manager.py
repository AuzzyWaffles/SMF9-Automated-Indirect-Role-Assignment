import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import datetime as dt
import os
import sys
from file_path import FilePath
from permissions_manager import PermissionsManager
from uncompliant_finder import UncompliantFinder
from schedule_finder import get_scheduled_associates
from assignment_manager import AssignmentManager


class DisplayManager:
    def __init__(self):
        # Determine whether the app is frozen or running on Pycharm to find app files
        self.file_path = FilePath()

        # Get site name:
        with open(self.file_path.get_persistent_storage_path('site.txt'), "r") as file:
            self.site = file.read().upper()

        # Get saved shifts
        with open(self.file_path.get_persistent_storage_path('saved_shifts.txt'), 'r') as file:
            self.shifts = [shift[:-1] for shift in file.readlines()]

        # Get current year, month, day number, hour
        self.current_time = dt.datetime.now()
        self.year = self.current_time.strftime('%Y')
        self.month = self.current_time.strftime('%m')
        self.day_number = self.current_time.strftime('%d')
        self.hour = self.current_time.strftime('%H')

        # Create instances of Permissions Manager, Uncompliant Finder
        self.pm = PermissionsManager()
        self.uf = UncompliantFinder()

        # Create Main Menu Window
        self.window = tk.Tk()
        self.window.title('Koality Rotation')

        # Create and set a frame to hold the canvas and the scrollbar
        frame = tk.Frame(self.window)
        frame.pack(fill="both", expand=True)

        # Create canvas inside the frame
        self.canvas = tk.Canvas(frame, width=500, height=600, bg='#1399FF')

        # Create and set a vertical scrollbar
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the canvas to use the scrollbar
        self.canvas.config(yscrollcommand=scrollbar.set)

        # Update the scrollable region after content is added
        self.canvas.bind("<Configure>", lambda event, canvas=self.canvas: self.on_frame_configure())

        # Create and set main menu header
        self.text = self.canvas.create_text(260, 60,
                                            text='Koality Rotation',
                                            font=("Helvetica", 20, "bold"))

        # Create and set dropdown menu
        self.dropdown_text = self.canvas.create_text(75, 100, text='Select a Shift:', font=("Helvetica", 12, "bold"))
        self.dropdown_widget = ttk.Combobox(self.window, values=self.shifts)
        self.canvas.create_window(250, 100, window=self.dropdown_widget)

        # Create and set site text
        self.site_text = self.canvas.create_text(435, 100, text=f'Site: {self.site}', font=("Helvetica", 12, "bold"))

        # Create and set date entry
        self.date_text = self.canvas.create_text(73, 132, text='Type a Date:', font=("Helvetica", 12, "bold"))
        self.date_entry = ttk.Entry(width=23)
        self.date_entry.insert(0, string=f'{self.month}-{self.day_number}-{self.year}')
        self.canvas.create_window(250, 132, window=self.date_entry)

        # Create and configure a style for ttk.Button, increase padding and font size
        style = ttk.Style()
        style.configure('TButton', padding=(0, 35, 0, 32), font=('Helvetica', 10))

        # Create buttons
        self.change_site_button = tk.Button(text="Change Site", width=10, command=self.change_site)
        self.change_shifts_button = tk.Button(text='Change Shifts', width=10, command=self.change_shifts)
        self.generate_button = ttk.Button(text="Generate", width=35, command=self.generate_button_click)
        self.permissions_button = ttk.Button(text="Check/Edit Permissions", width=35,
                                             command=self.pm.check_permissions)
        self.add_remove_button = tk.Button(text='Add/Remove Roles',
                                           command=self.add_remove_roles)

        # Set buttons
        self.canvas.create_window(435, 132, window=self.change_site_button)
        self.canvas.create_window(435, 165, window=self.change_shifts_button)
        self.canvas.create_window(250, 200, window=self.generate_button)
        self.canvas.create_window(250, 385, window=self.permissions_button)
        self.canvas.create_window(410, 465, window=self.add_remove_button)

        # Create and set horizontal line
        self.canvas.create_line(0, 445, 500, 445, fill="black", width=2)

        # Determine the path to the Amazon smile logo
        if getattr(sys, 'frozen', False):
            # If the application is frozen (e.g., as a single .exe file)
            bundle_dir = sys._MEIPASS
        else:
            # If the application is not frozen (running in Pycharm)
            bundle_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the Amazon smile logo
        image_path = os.path.join(bundle_dir, 'images', 'image1.png')

        # Create and set Amazon smile logo
        self.smile_image1 = tk.PhotoImage(file=image_path)
        self.canvas.create_image(250, 285, image=self.smile_image1, tag='image1')

        # Create and set saved roles
        self.generate_roles()

    def on_frame_configure(self):
        # Update the scrollable region of the canvas whenever the content changes
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def generate_roles(self):
        # Get saved roles
        with open(self.file_path.get_persistent_storage_path(f'saved_roles.txt'), "r") as file:
            self.lines = [line.strip() for line in file.readlines()]
            curr_y = 465

            # Create and set saved roles and entrys
            self.entry_dict = {}
            for line in self.lines:
                self.canvas.create_text(200, curr_y, text=f'{line.upper()}:', font=("Helvetica", 12, "bold"))

                self.entry_dict[f'{line}_entry'] = ttk.Entry(width=2)
                self.entry_dict[f'{line}_entry'].insert(tk.END, string="0")
                self.canvas.create_window(300, curr_y, window=self.entry_dict[f'{line}_entry'])

                curr_y += 50

        # Start the main loop
        self.canvas.pack()
        self.canvas.mainloop()

    def change_site(self):
        self.site = simpledialog.askstring('Change Site', 'Please enter your site:')
        if self.site:
            self.site = self.site.upper()
            with open(self.file_path.get_persistent_storage_path(f'site.txt'), "w") as file:
                file.write(self.site)
            self.canvas.delete(self.site_text)
            self.site_text = self.canvas.create_text(435, 100, text=f'Site: {self.site}',
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
        except ValueError:
            messagebox.showinfo(title="Error", message="Invalid date entry.\n\nPlease ensure you typed the correct date"
                                                       " and it's formatted as follows: MM/DD/YYYY")
            return

        if not messagebox.askyesno(title="Proceed?", message='Are you sure you would like to proceed?'):
            return

        # Create dictionary saving number of AAs per indirect role
        nums_dict = {line: int(self.entry_dict[f'{line}_entry'].get()) for line in self.lines}

        self.window.destroy()

        # Use imported function to find scheduled associates
        scheduled_associates = get_scheduled_associates(self.site, shift, date)

        # If Scheduling Site takes too long to load and returns False
        if not scheduled_associates:
            DisplayManager()
            return

        # Use PermissionsManager method to get txt for each indirect role
        permissions_dict = self.pm.get_permissions()

        # Create final class object, create final string
        am = AssignmentManager(permissions_dict, nums_dict, scheduled_associates)
        result_string, not_enough_string = am.assign_indirects()
        if not_enough_string:
            final_string = not_enough_string + '\n' + result_string
        else:
            final_string = result_string

        # Place the results in a messagebox
        if not messagebox.askyesno(title="Results", message=f'{final_string}\n Would you like to go back to the Main '
                                                            f'Menu?'):
            return
        DisplayManager()
