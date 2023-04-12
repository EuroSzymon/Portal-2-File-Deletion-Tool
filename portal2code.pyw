import os
import threading
import urllib.request

def check_updates():
    url = 'https://api.github.com/repos/EuroSzymon/Portal-2-File-Deletion-Tool/releases/latest'
    with urllib.request.urlopen(url) as response:
        data = response.read().decode()
        import json
        release = json.loads(data)
    latest_version = release['tag_name']
    if latest_version != 'v1.0.5':
        messagebox.showinfo("Info", "New version available! Please visit Github to download.")


from tkinter import Tk, Label, Button, messagebox, Menu

root = Tk()
root.title('Portal 2 Audio Fix Tool')
root.geometry('600x400')


def show_settings():
    messagebox.showinfo("Info", "Settings not available in this version.")


menu_bar = Menu(root)
root.config(menu=menu_bar)

update_menu = Menu(menu_bar, tearoff=0)
update_menu.add_command(label='Check updates')
menu_bar.add_cascade(label='Updates', menu=update_menu)

settings_menu = Menu(menu_bar, tearoff=0)
settings_menu.add_command(label='Settings', command=show_settings)
menu_bar.add_cascade(label='Settings', menu=settings_menu)

version_label = Label(root, text='v1.0.5', fg='gray')
version_label.pack(side='bottom')


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


start_button = Button(root, text='Start', width=8, command=start_action)
start_button.pack(pady=20)

root.mainloop()