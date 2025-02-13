import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime as dt
import sys
import os
from permissions_manager import PermissionsManager
from uncompliant_finder import UncompliantFinder
from schedule_finder import get_scheduled_associates
from assignment_manager import AssignmentManager


class DisplayManager:
    def __init__(self):
        # Get current datetime
        self.current_time = dt.datetime.now()
        self.year = self.current_time.strftime('%Y')
        self.month = self.current_time.strftime('%m')
        self.day_number = self.current_time.strftime('%d')
        self.hour = self.current_time.strftime('%H')

        # Setup other classes
        self.pm = PermissionsManager()
        self.uf = UncompliantFinder()

        # Create Main Menu
        self.window = tk.Tk()
        self.window.title('Koality Rotation')
        self.canvas = tk.Canvas(width=1000, height=1000, bg='#1399FF')

        self.text = self.canvas.create_text(260, 60,
                                            text='Thanks for using Koality Rotation!\n\nOnce the '
                                                 'browser opens you will need to log in through Midway.\n\nAfter '
                                                 'logging in please don\'t click anything, the app will handle all '
                                                 'browser activity.\n\nPlease fill out the entries below then click '
                                                 'the \'Generate\' button to begin!',
                                            font=("Helvetica", 9, "bold"))

        self.canvas.create_line(0, 120, 500, 120, fill="black", width=2)

        self.dropdown_text = self.canvas.create_text(75, 135, text='Select a Shift:',
                                                     font=("Helvetica", 12, "bold"))
        self.date_text = self.canvas.create_text(73, 167, text='Type a Date:', font=("Helvetica", 12, "bold"))
        self.eol_text = self.canvas.create_text(50, 200, text='EOL:', font=("Helvetica", 12, "bold"))
        self.ws_text = self.canvas.create_text(50, 250, text='WS:', font=("Helvetica", 12, "bold"))
        self.ps_text = self.canvas.create_text(50, 300, text='PS:', font=("Helvetica", 12, "bold"))
        self.dt_text = self.canvas.create_text(50, 350, text='DT:', font=("Helvetica", 12, "bold"))
        self.refurb_text = self.canvas.create_text(50, 400, text='REFURB:', font=("Helvetica", 12, "bold"))
        self.unload_text = self.canvas.create_text(50, 450, text='UNLOAD:', font=("Helvetica", 12, "bold"))

        self.dropdown_options = ['MOR', 'DAY', 'TWI', 'NIT']
        self.dropdown_widget = ttk.Combobox(self.window, values=self.dropdown_options)
        if int(self.hour) < 8:
            self.dropdown_widget.insert(0, string='MOR')
        elif int(self.hour) < 14:
            self.dropdown_widget.insert(0, string='DAY')
        elif int(self.hour) < 19:
            self.dropdown_widget.insert(0, string='TWI')
        else:
            self.dropdown_widget.insert(0, string='NIT')

        self.date_entry = ttk.Entry(width=23)
        self.date_entry.insert(0, string=f'{self.month}-{self.day_number}-{self.year}')

        self.eol_entry = ttk.Entry(width=2)
        self.eol_entry.insert(tk.END, string="0")
        self.ws_entry = ttk.Entry(width=2)
        self.ws_entry.insert(tk.END, string="0")
        self.ps_entry = ttk.Entry(width=2)
        self.ps_entry.insert(tk.END, string="0")
        self.dt_entry = ttk.Entry(width=2)
        self.dt_entry.insert(tk.END, string="0")
        self.refurb_entry = ttk.Entry(width=2)
        self.refurb_entry.insert(tk.END, string="0")
        self.unload_entry = ttk.Entry(width=2)
        self.unload_entry.insert(tk.END, string="0")

        self.canvas.create_window(350, 135, window=self.dropdown_widget)
        self.canvas.create_window(351, 167, window=self.date_entry)
        self.canvas.create_window(100, 200, window=self.eol_entry)
        self.canvas.create_window(100, 250, window=self.ws_entry)
        self.canvas.create_window(100, 300, window=self.ps_entry)
        self.canvas.create_window(100, 350, window=self.dt_entry)
        self.canvas.create_window(100, 400, window=self.refurb_entry)
        self.canvas.create_window(100, 450, window=self.unload_entry)

        # Create a style for ttk.Button
        style = ttk.Style()

        # Configure the button style to increase padding and font size
        style.configure('TButton', padding=(0, 35, 0, 32), font=('Helvetica', 10))
        self.generate_button = ttk.Button(text="Generate", width=35, command=self.generate_button_click)
        self.permissions_button = ttk.Button(text="Check/Edit Permissions", width=35,
                                             command=self.permissions_button_click)
        self.info_button = tk.Button(text='i', command=lambda: messagebox.showinfo(title="Info", message='Please '
                                                                                                         'input the '
                                                                                                         'date in the '
                                                                                                         'following '
                                                                                                         'format: '
                                                                                                         'MM-DD-YYYY'))

        self.canvas.create_window(350, 235, window=self.generate_button)
        self.canvas.create_window(350, 420, window=self.permissions_button)
        self.canvas.create_window(450, 167, window=self.info_button)

        # Determine the path to the bundled executable or script
        if getattr(sys, 'frozen', False):
            # If the application is frozen (e.g., as a single .exe file)
            bundle_dir = sys._MEIPASS  # PyInstaller creates this variable
        else:
            # If the application is not frozen (running as a script)
            bundle_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to image1.png
        image_path = os.path.join(bundle_dir, 'images', 'image1.png')

        self.smile_image1 = tk.PhotoImage(file=image_path)
        self.canvas.create_image(350, 320, image=self.smile_image1, tag='image1')

        self.canvas.pack()
        self.canvas.mainloop()

    def generate_button_click(self):
        try:
            if (int(self.eol_entry.get()) < 0 or int(self.ps_entry.get()) < 0 or
                    int(self.ws_entry.get()) < 0 or int(self.dt_entry.get()) < 0 or
                    int(self.refurb_entry.get()) < 0 or int(self.unload_entry.get()) < 0):
                messagebox.showinfo(title="Error", message="All role entries must contain valid integers.")
                return
        except ValueError:
            messagebox.showinfo(title="Error", message="All role entries must contain valid integers.")
            return

        shift = self.dropdown_widget.get()
        if shift not in self.dropdown_options:
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

        # If pulling for today or tomorrow, use object method to find uncompliant processors
        # if date == today or date == tomorrow:
        if date == 'DISABLING_UNCOMPLIANT_FINDER':  # uncomment above comment to re-enable
            try:
                uncompliant_processors = self.uf.get_uncompliant_processors()
            except FileNotFoundError:
                messagebox.showinfo(title="Error", message="Could not find the compliance file on your desktop.")
                return

        # If pulling for a date later than tomorrow, ignore processing compliance
        else:
            uncompliant_processors = []

        # Create dictionary saving number of AAs per indirect role
        nums_dict = {'eol': int(self.eol_entry.get()), 'ws': int(self.ws_entry.get()), 'ps': int(self.ps_entry.get()),
                     'dt': int(self.dt_entry.get()), 'refurb': int(self.refurb_entry.get()),
                     'unload': int(self.unload_entry.get())}

        self.window.destroy()

        # Use imported function to find scheduled associates
        scheduled_associates = get_scheduled_associates(shift, date)

        # If Scheduling Site takes too long to load and returns False
        if not scheduled_associates:
            DisplayManager()
            return

        # Use PermissionsManager method to get permissions for each indirect role
        permissions_dict = self.pm.get_permissions()

        # Create final class object
        am = AssignmentManager(permissions_dict, nums_dict, uncompliant_processors, scheduled_associates)
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
