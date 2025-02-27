import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import file_path


def change_site(display):
    """Opens entry box to allow user to change site ID"""
    try:
        display.site = simpledialog.askstring('Change Site', 'Please enter your site:').upper()
        if display.site:
            with open(file_path.get_txt(f'site.txt'), "w") as file:
                file.write(display.site)
            display.canvas.delete(display.site_text)
            display.site_text = display.canvas.create_text(435, 100, text=f'Site: {display.site}',
                                                           font=("Helvetica", 12, "bold"))
    except AttributeError:
        pass


def change_shifts(display):
    """Opens text box to allow user to change shift start times"""
    messagebox.showinfo(title="Shifts Input", message="Please ensure all shifts are entered as follows:\nHH-MM-00")
    with open(file_path.get_txt('saved_shifts.txt'), 'r') as file:
        shifts = ''
        text = file.read()
        shifts += text
        display.text_window = tk.Tk()
        display.text_window.title('Change Shifts')
        display.text_window.iconbitmap('images/image2.ico')
        text = tk.Text(display.text_window)
        text.insert(tk.END, chars=shifts)

        save_button = ttk.Button(display.text_window, text="Save", width=20,
                                 command=lambda: __save(display, text, 'saved_shifts.txt'))
        save_button.place(x=480, y=10)

        # Create a vertical scrollbar
        scrollbar = tk.Scrollbar(display.text_window, orient="vertical", command=text.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the Text widget to use the scrollbar
        text.config(yscrollcommand=scrollbar.set)

        text.pack()
        display.text_window.mainloop()


def add_remove_roles(display):
    """Opens text box to allow user to add/remove roles"""
    with open(file_path.get_txt(f'saved_roles.txt'), "r") as file:
        roles = ''
        text = file.read()
        roles += text

    display.text_window = tk.Tk()
    display.text_window.title("Add/Remove Roles")
    display.text_window.iconbitmap('images/image2.ico')
    text = tk.Text(display.text_window)
    text.insert(tk.END, chars=roles)

    save_button = ttk.Button(display.text_window, text="Save", width=20,
                             command=lambda: __save(display, text, 'saved_roles.txt'))
    save_button.place(x=480, y=10)

    # Create a vertical scrollbar
    scrollbar = tk.Scrollbar(display.text_window, orient="vertical", command=text.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the Text widget to use the scrollbar
    text.config(yscrollcommand=scrollbar.set)

    text.pack()
    display.text_window.mainloop()


def __save(display, text, txt):
    """Saves content in Add/Remove Roles text box"""
    saved_text = text.get("1.0", 'end-1c').split('\n')
    saved_text = [item for item in saved_text if item != '']
    with open(file_path.get_txt(txt), "w") as file:
        for role in saved_text:
            file.write(role + '\n')

    display.text_window.destroy()
    tk.messagebox.showinfo(title="Saved!",
                           message='Saved!')

    display.window.destroy()

    from display_manager import DisplayManager
    DisplayManager()
