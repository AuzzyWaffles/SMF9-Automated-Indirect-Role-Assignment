import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import file_path
from assignment_manager import AssignmentManager
import permissions_manager as pm
from schedule_finder import get_scheduled_associates
import customization_manager as custom


class DisplayManager:
    def __init__(self):

        with open(file_path.get_custom_text('site'), "r") as file:
            self.site = file.read().upper()

        self.shifts = None

        self.current_time = dt.datetime.now()
        self.year = self.current_time.strftime('%Y')
        self.month = self.current_time.strftime('%m')
        self.day_number = self.current_time.strftime('%d')
        self.hour = self.current_time.strftime('%H')

        self.window = tk.Tk()
        self.window.title('Koality Rotator')
        self.window.iconbitmap(file_path.get_koala())
        self.center_window(self.window, 500, 600)

        self.text_window = None
        self.text_box = None
        self.lines = None
        self.entry_dict = None

        # Create Scrollbar
        frame = tk.Frame(self.window)
        frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(frame, width=500, height=600, bg='#1399FF')
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.config(yscrollcommand=scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Configure>", lambda event, canvas=self.canvas: self.on_frame_configure())

        # self.text = self.canvas.create_text(260, 60,
        #                                     text='Koality Rotator',
        #                                     font=("Helvetica", 20, "bold"))
        #
        # self.dropdown_text = self.canvas.create_text(75, 100, text='Select a Shift:', font=("Helvetica", 12, "bold"))
        self.dropdown_widget = None
        # self.dropdown_widget.set("Select an option")
        # self.canvas.create_window(250, 100, window=self.dropdown_widget)

        self.site_text = None

        # self.date_text = self.canvas.create_text(73, 132, text='Type a Date:', font=("Helvetica", 12, "bold"))
        self.date_entry = ttk.Entry(width=23)
        self.date_entry.insert(0, string=f'{self.month}-{self.day_number}-{self.year}')
        # self.canvas.create_window(250, 132, window=self.date_entry)

        style = ttk.Style()
        style.configure('TButton', padding=(0, 35, 0, 32), font=('Helvetica', 10))

        self.change_site_button = tk.Button(text="Change Site", width=10, command=self.change_site)
        self.change_shifts_button = tk.Button(text='Change Shifts', width=10, command=self.change_shifts)
        self.generate_button = ttk.Button(text="Generate", width=35, command=self.generate_button_click)
        self.permissions_button = ttk.Button(text="Check/Edit Permissions", width=35,
                                             command=self.check_permissions)
        self.add_remove_button = tk.Button(text='Add/Remove Roles',
                                           command=self.add_remove_roles)

        # self.canvas.create_window(435, 132, window=self.change_site_button)
        # self.canvas.create_window(435, 165, window=self.change_shifts_button)
        # self.canvas.create_window(250, 200, window=self.generate_button)
        # self.canvas.create_window(250, 385, window=self.permissions_button)
        # self.canvas.create_window(410, 465, window=self.add_remove_button)

        # self.canvas.create_line(0, 445, 500, 445, fill="black", width=2)

        self.smile_image1 = tk.PhotoImage(file=file_path.get_logo())
        # self.canvas.create_image(250, 285, image=self.smile_image1, tag='image1')

        self.generate_canvas()
        self.canvas.pack()
        self.canvas.mainloop()

    def center_window(self, window, width, height):
        # Get the screen's width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Get the window's size after packing the Text widget
        window.update_idletasks()  # Ensure the window size is calculated

        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set the window's geometry (size + position)
        window.geometry(f'{width}x{height}+{x}+{y - 40}')

    def on_frame_configure(self):
        """Update the scrollable region of the canvas whenever the content changes"""
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling"""
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def generate_canvas(self):
        """Reads and creates text/entry for every saved role"""
        self.canvas.create_text(260, 60,
                                            text='Koality Rotator',
                                            font=("Helvetica", 20, "bold"))
        self.canvas.create_text(75, 100, text='Select a Shift:', font=("Helvetica", 12, "bold"))
        self.shifts = custom.get_shifts().split('\n')
        self.shifts.pop()
        self.dropdown_widget = ttk.Combobox(self.window, values=self.shifts)
        self.dropdown_widget.set("Select an option")
        self.canvas.create_window(250, 100, window=self.dropdown_widget)
        self.site_text = self.canvas.create_text(435, 100, text=f'Site: {self.site}', font=("Helvetica", 12, "bold"))
        self.canvas.create_text(73, 132, text='Type a Date:', font=("Helvetica", 12, "bold"))
        self.canvas.create_window(250, 132, window=self.date_entry)
        self.canvas.create_window(435, 132, window=self.change_site_button)
        self.canvas.create_window(435, 165, window=self.change_shifts_button)
        self.canvas.create_window(250, 200, window=self.generate_button)
        self.canvas.create_window(250, 385, window=self.permissions_button)
        self.canvas.create_window(410, 465, window=self.add_remove_button)
        self.canvas.create_line(0, 445, 500, 445, fill="black", width=2)
        self.canvas.create_image(250, 285, image=self.smile_image1, tag='image1')

        with open(file_path.get_custom_text('saved_roles'), "r") as file:
            self.lines = [line.strip() for line in file.readlines()]
            curr_y = 465

            self.entry_dict = {}
            for line in self.lines:
                self.canvas.create_text(200, curr_y, text=f'{line}:', font=("Helvetica", 12, "bold"))

                self.entry_dict[f'{line}_entry'] = ttk.Entry(width=2)
                self.entry_dict[f'{line}_entry'].insert(tk.END, string="0")
                self.canvas.create_window(300, curr_y, window=self.entry_dict[f'{line}_entry'])

                curr_y += 50

        self.canvas.pack()
        self.canvas.mainloop()


    def change_site(self):
        try:
            self.site = simpledialog.askstring('Change Site', 'Please enter your site:').upper()
            custom.change_site(self.site)
            self.canvas.delete(self.site_text)
            self.site_text = self.canvas.create_text(435, 100, text=f'Site: {self.site}',
                                                     font=("Helvetica", 12, "bold"))
        except AttributeError:
            pass

    def change_shifts(self):
        messagebox.showinfo(title="Shifts Input", message="Please ensure all shifts are entered as follows:\nHH-MM-00")
        shifts = custom.get_shifts()

        self.text_window = tk.Tk()
        self.text_window.title('Change Shifts')
        self.text_window.iconbitmap(file_path.get_koala())
        self.text_box = tk.Text(self.text_window)
        self.text_box.insert(tk.END, chars=shifts)

        save_button = ttk.Button(self.text_window, text="Save", width=20,
                                 command=lambda: self.__save('saved_shifts'))
        save_button.place(x=480, y=10)

        # Create a vertical scrollbar
        scrollbar = tk.Scrollbar(self.text_window, orient="vertical", command=self.text_box.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the Text widget to use the scrollbar
        self.text_box.config(yscrollcommand=scrollbar.set)

        self.text_box.pack()
        self.center_window(self.text_window, 630, 300)
        self.text_window.mainloop()

    def add_remove_roles(self):
        roles = custom.add_remove_roles()
        self.text_window = tk.Tk()
        self.text_window.title("Add/Remove Roles")
        self.text_window.iconbitmap(file_path.get_koala())
        self.text_box = tk.Text(self.text_window)
        self.text_box.insert(tk.END, chars=roles)

        save_button = ttk.Button(self.text_window, text="Save", width=20,
                                 command=lambda: self.__save('saved_roles'))
        save_button.place(x=480, y=10)

        # Create a vertical scrollbar
        scrollbar = tk.Scrollbar(self.text_window, orient="vertical", command=self.text_box.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the Text widget to use the scrollbar
        self.text_box.config(yscrollcommand=scrollbar.set)

        self.text_box.pack()
        self.center_window(self.text_window, 630, 300)
        self.text_window.mainloop()

    def __save(self, filename):
        text = self.text_box.get("1.0", 'end-1c').split('\n')
        text = [item for item in text if item != '']
        custom.save(filename, text)

        self.text_window.destroy()
        tk.messagebox.showinfo(title="Saved!",
                               message='Saved!')

        self.canvas.delete('all')
        self.generate_canvas()

    def check_permissions(self):
        permissions_string = pm.check_permissions()

        self.text_window = tk.Tk()
        self.text_window.title("Check/Edit Permissions")
        self.text_window.iconbitmap(file_path.get_koala())
        text = tk.Text(self.text_window)
        text.insert(tk.END, chars=permissions_string)

        save_button = ttk.Button(self.text_window, text="Save", width=20,
                                 command=lambda: self.__save_permissions(text))
        save_button.place(x=480, y=10)

        # Create a vertical scrollbar
        scrollbar = tk.Scrollbar(self.text_window, orient="vertical", command=text.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the Text widget to use the scrollbar
        text.config(yscrollcommand=scrollbar.set)

        text.pack()
        self.center_window(self.text_window, 630, 300)
        self.text_window.mainloop()

    def __save_permissions(self, text):
        saved = pm.save_permissions(text)
        self.text_window.destroy()
        if not saved:
            tk.messagebox.showinfo(title="Error",
                                   message='Error: Changes not saved.\n\nIf you need to add or remove roles, '
                                           'please do so on the main menu by clicking "Add/Remove Roles."')
        else:
            tk.messagebox.showinfo(title="Saved!", message='Permissions Saved!')

    def generate_button_click(self):
        all_zero = True
        try:
            for line in self.lines:
                entry = self.entry_dict[f'{line}_entry'].get()
                entry_value = int(entry)

                if entry_value < 0:
                    messagebox.showinfo(title="Error",
                                        message="All role entries must contain valid integers (greater than or equal "
                                                "to 0).")
                    return
                elif entry_value > 0:
                    all_zero = False

        except ValueError:
            messagebox.showinfo(title="Error", message="All role entries must contain valid integers.")
            return

        if all_zero:
            messagebox.showinfo(title="Error",
                                message="All role entries are 0.\n\nPlease enter at least one role entry greater than "
                                        "0.")
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

        nums_dict = {line: int(self.entry_dict[f'{line}_entry'].get()) for line in self.lines}

        self.window.destroy()

        scheduled_associates = get_scheduled_associates(self.site, shift, date)

        if not scheduled_associates:  # if returned None due to a problem
            messagebox.showinfo(title='Timeout', message='There was a problem.\nIs your PIN correct?\nIs your '
                                                         'security key correct?\nIs your site ID correct?\nIs your '
                                                         'shift time correct?\nIf yes, SSPOT may have bugged '
                                                         'out.\nPlease try again.')
            DisplayManager()
            return

        permissions_dict = pm.get_permissions()

        am = AssignmentManager(permissions_dict, nums_dict, scheduled_associates)
        result_string, not_enough_string = am.assign_indirects()

        if not_enough_string:
            final_string = not_enough_string + '\n' + result_string
        else:
            final_string = result_string

        if not messagebox.askyesno(title="Koality Results", message=f'{final_string}\n Would you like to go back to '
                                                                    'the Main Menu?'):
            return
        DisplayManager()
