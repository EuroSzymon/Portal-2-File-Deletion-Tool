import webbrowser
import os
import shutil
import json
import time
import concurrent.futures
from tkinter import Tk, Menu, ttk, filedialog, messagebox
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

app = ctk.CTk()
app.geometry("1200x600")
app.title("Portal 2 File Deletion Tool")
ctk.set_appearance_mode("system")

is_process_interrupted = False
has_backup = False
is_second_run = False
backup_folder_path = ""

def create_config_file():
    if not os.path.exists("config.json"):
        config_data = {}
        with open("config.json", "w") as config_file:
            json.dump(config_data, config_file)

def create_state_file():
    if not os.path.exists("state.json"):
        state_data = {}
        with open("state.json", "w") as state_file:
            json.dump(state_data, state_file)

def load_application_state():
    global has_backup, is_second_run, backup_folder_path

    try:
        with open("state.json", "r") as state_file:
            state_data = json.load(state_file)
            has_backup = state_data.get("has_backup", False)
            is_second_run = state_data.get("is_second_run", False)
            backup_folder_path = state_data.get("backup_folder_path", "")
    except Exception as e:
        print("Failed to load application state:", e)

def save_application_state():
    try:
        state_data = {
            "has_backup": has_backup,
            "is_second_run": is_second_run,
            "backup_folder_path": backup_folder_path
        }
        with open("state.json", "w") as state_file:
            json.dump(state_data, state_file)
    except Exception as e:
        print("Failed to save application state:", e)

def open_backup_folder():
    global backup_folder_path
    if backup_folder_path:
        webbrowser.open(backup_folder_path)
    else:
        messagebox.showinfo("Open Backup Folder", "Backup folder not loaded.")

def load_backup_folder():
    global backup_folder_path, has_backup
    backup_folder = filedialog.askdirectory(title="Select Backup Folder")
    if backup_folder:
        backup_folder_path = backup_folder
        has_backup = True
        with open("config.json", "w") as config_file:
            config_data = {"backup_folder_path": backup_folder_path}
            json.dump(config_data, config_file)
    else:
        messagebox.showinfo("Load Backup Folder", "Backup folder not selected.")

def start_action():
    global has_backup, is_second_run

    if is_second_run:
        is_second_run = False
    else:
        load_application_state()
        if backup_folder_path:
            has_backup = True

    portal2_path = get_portal2_path()
    if portal2_path:
        if not os.path.exists(portal2_path):
            CTkMessagebox.showerror("Error", "The selected directory does not exist.")
            return

        backup_folder = os.path.join(os.path.expanduser("~"), "Portal2Backup")
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)

        progress_label = ttk.Label(app, text="Copying files...")
        progress_label.pack()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(create_backup, portal2_path, backup_folder)
            app.after(100, update_progress_label, future, progress_label)

def update_progress_label(future, progress_label):
    if not future.done():
        app.after(100, update_progress_label, future, progress_label)
        return

    try:
        result = future.result()
        if result:
            progress_label.config(text="Backup completed!")
            messagebox.showinfo("Backup Completed", "Backup of Portal 2 has been created successfully.")
            save_application_state()
            display_backup = messagebox.askyesno("Display Backup", "Do you want to display the backup folder?")
            if display_backup:
                webbrowser.open(backup_folder_path)
            if os.path.exists(backup_folder_path):
                delete_backup_button = ctk.CTkButton(master=app, text="Delete Backup", fg_color="red", hover_color="purple", corner_radius=8, command=delete_backup)
                delete_backup_button.pack(pady=10)
        else:
            progress_label.config(text="Process interrupted")
    except Exception as e:
        print("Error occurred:", e)

def get_portal2_path():
    portal2_path = filedialog.askdirectory(title="Select Portal 2 Installation Folder")
    if not portal2_path:
        return None
    return portal2_path

def create_backup(portal2_path, backup_folder):
    global is_process_interrupted
    print("Creating backup...")
    try:
        total_files = sum(1 for root, _, files in os.walk(portal2_path) for file in files if not root.endswith('puzzles'))
        progress = 0
        start_time = time.time()
        for root, _, files in os.walk(portal2_path):
            if root.endswith('puzzles'):
                continue
            for file in files:
                src_path = os.path.join(root, file)
                dst_path = os.path.join(backup_folder, os.path.relpath(src_path, portal2_path))
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)
                progress += 1
                
                if is_process_interrupted:
                    break

        if not is_process_interrupted:
            shutil.copytree(portal2_path, os.path.join(backup_folder, "Portal2"))
            
            elapsed_time = time.time() - start_time
            average_time_per_file = elapsed_time / progress if progress > 0 else 0
            total_files_to_copy = total_files - progress
            estimated_time_left = total_files_to_copy * average_time_per_file
            estimated_time_left_minutes = int(estimated_time_left / 60)
            print(f"Backup completed! Estimated time left: {estimated_time_left_minutes} minutes.")
            return True
        else:
            return False
    except Exception as e:
        print("Backup creation failed:", e)
        return False

def delete_portal2(portal2_path, progress_label):
    global is_process_interrupted
    print("Deleting Portal 2 folders...")
    folders_to_delete = ["portal2", "sdk_content", "steam_input", "update"]
    total_folders = len(folders_to_delete)
    progress = 0
    for folder in folders_to_delete:
        folder_path = os.path.join(portal2_path, folder)
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"Deleted {folder}")
                progress += 1
            except Exception as e:
                print(f"Failed to delete {folder}: {e}")
                is_process_interrupted = True
                break

    progress_percent = (progress / total_folders) * 100
    progress_label.config(text=f"Deleting Portal 2 folders... {progress}/{total_folders}  Progress: {progress_percent:.2f}%")

    if progress == total_folders:
        progress_label.config(text="Portal 2 folders have been successfully deleted.")

def delete_backup():
    global backup_folder_path

    if backup_folder_path:
        try:
            shutil.rmtree(backup_folder_path)
            messagebox.showinfo("Backup Deleted", "Backup folder has been successfully deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete backup folder: {e}")

def save_state_action():
    save_application_state()
    messagebox.showinfo("Save State", "Application state saved successfully.")

def on_closing():
    global is_process_interrupted
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        is_process_interrupted = True
        save_application_state()
        app.destroy()

create_config_file()
create_state_file()
load_application_state()

start_button = ctk.CTkButton(master=app, text="Start", fg_color="green", hover_color="purple", corner_radius=8)
start_button.pack(pady=10)
start_button.configure(command=start_action)

open_backup_folder_button = ctk.CTkButton(master=app, text="Open Backup Folder", fg_color="blue", hover_color="purple", corner_radius=8, command=open_backup_folder)
open_backup_folder_button.pack(pady=10)

load_backup_folder_button = ctk.CTkButton(master=app, text="Load Backup Folder", fg_color="blue", hover_color="purple", corner_radius=8, command=load_backup_folder)
load_backup_folder_button.pack(pady=10)

save_state_button = ctk.CTkButton(master=app, text="Save State", fg_color="orange", hover_color="purple", corner_radius=8, command=save_state_action)
save_state_button.pack(pady=10)

app.protocol("WM_DELETE_WINDOW", on_closing)

app.mainloop()
