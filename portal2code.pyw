import threading
import webbrowser
import os
from tkinter import Tk, Label, Menu, messagebox, ttk
import customtkinter as ctk

app = ctk.CTk()
app.geometry("1200x600")
app.title("Portal 2 File Deletion Tool")
ctk.set_appearance_mode("dark")

title_label = ctk.CTkLabel(master=app, text="A tool for removing the Portal 2 sound files", text_color="gray")
title_label.pack(pady=20)

version_label = ctk.CTkLabel(master=app, text="v1.0.8", text_color="gray")
version_label.place(relx=0.5, rely=1.0, anchor='s')

start_button = ctk.CTkButton(master=app, text="Start", corner_radius=8)
start_button.pack(pady=10)

def start_action():
    if messagebox.askquestion("Confirm", "Do you want to delete game folders?") == "yes":
        portal2_path = "C:/Steam/steamapps/common/Portal 2"
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

def open_browser():
    url = "https://github.com/EuroSzymon/Portal-2-File-Deletion-Tool"
    webbrowser.open_new_tab(url)
browser_button = ctk.CTkButton(master=app, text="Open main GitHub repository", corner_radius=8)
browser_button.pack(pady=10)
browser_button.configure(command=open_browser)
def open_browser():
    url = "https://github.com/EuroSzymon/Portal-2-File-Deletion-Tool/blob/normal/LICENSE"
    webbrowser.open_new_tab(url)
browser_button = ctk.CTkButton(master=app, text="App license info", corner_radius=8)
browser_button.pack(pady=10)
browser_button.configure(command=open_browser)
def open_browser():
    url = "https://github.com/EuroSzymon/Portal-2-File-Deletion-Tool/releases"
browser_button = ctk.CTkButton(master=app, text="GitHub releases tab", corner_radius=8)
browser_button.pack(pady=10)
browser_button.configure(command=open_browser)
warning_label = ctk.CTkLabel(master=app, text="Keep in mind that feature requests are not accepted. Internet connection is required.",corner_radius=8, text_color="red")
warning_label.pack(pady=10)
about_label = ctk.CTkLabel(master=app, text="About this software: Portal 2 File Deletion Tool is a software supposed to fix the missing sound issue in Portal 2.",corner_radius=8, text_color="gray")
about_label.pack(pady=10)
about_label = ctk.CTkLabel(master=app, text="User is supposed after deletion process verify game integrity on Steam manually.",corner_radius=8, text_color="gray")
about_label.pack(pady=10)
about_label = ctk.CTkLabel(master=app, text="The development of this app is running and app is open-source so everyone can contribute.",corner_radius=8, text_color="gray")
about_label.pack(pady=10)
about_label = ctk.CTkLabel(master=app, text="If you want to support this project,",corner_radius=8, text_color="gray")
about_label.pack(pady=10)
about_label = ctk.CTkLabel(master=app, text="consider contributing into code of the program. The software is not supposed to be a tool to delete everything on a computer and it's not very recommended to modify software in that way.",corner_radius=8, text_color="gray")
about_label.pack(pady=10)
start_button.configure(command=start_action)

app.mainloop()
