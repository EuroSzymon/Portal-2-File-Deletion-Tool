import os
import threading
from tkinter import Tk, Label, Button, Widget, messagebox, Menu
import webbrowser
from tkinter import ttk

root = Tk()
root.title('Portal 2 Audio Fix Tool')
root.geometry('600x400')
root.config(bg='gray10')


title_label = ttk.Label(root, text='A tool for removing the Portal 2 sound files', background='gray10', foreground='white')
title_label.pack(pady=20)

def download_action():
    messagebox.showinfo("Opening the browser...", "Please wait patiently. Depending on your hardware and on the internet it may be take long to load or may be take very fast to load. When you close this window or you click the OK button, the browser will be loaded.")
    url = "https://github.com/EuroSzymon/Portal-2-File-Deletion-Tool"
    webbrowser.open_new(url)

menu_bar = Menu(root, bg='gray20', fg='white')
root.config(menu=menu_bar)

update_menu = Menu(menu_bar, tearoff=0, bg='gray20', fg='white')
update_menu.add_command(label='Download or Update', command=download_action)
menu_bar.add_cascade(label='Updates', menu=update_menu)

version_label = ttk.Label(root, text='v1.0.6', background='gray10', foreground='gray80')
version_label.place(relx=0.5, rely=1.0, anchor='s')

start_button = ttk.Button(root, text='Start')
start_button.pack(pady=10)

def start_action():
    if messagebox.askquestion("Confirm", "Do you want to delete game folders?") == "yes":
        portal2_path = "C:\\Steam\\steamapps\\common\\Portal 2"
        folders = ["portal2", "sdk_content", "steam_input", "update"]
        if not os.path.exists(portal2_path):
            messagebox.showerror("Error", "Portal 2 is not installed.")
            return
        t = threading.Thread(target=remove_folders, args=(portal2_path, folders))
        t.start()
    else:
        messagebox.showinfo("Info", "Process has been cancelled.")

def remove_folders(portal2_path, folders):
    for i, entry in enumerate(os.scandir(portal2_path)):
        if entry.is_dir() and entry.name in folders:
            path = entry.path
            print(f"Deleting {entry.name}... {(i + 1) / len(folders) * 100:.0f}%")
            os.system(f"rmdir /s /q \"{path}\"")
    messagebox.showinfo("Info", "Folders have been successfully deleted.")

start_button.configure(command=start_action)

root.mainloop()

