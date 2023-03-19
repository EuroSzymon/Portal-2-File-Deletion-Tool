from tkinter import Tk, Label, Button, messagebox
import os # importing the os library used to make code interactable with user operating system
import shutil # importing the shutil library used to execute tasks like deleting elements from PC

root = Tk()
root.title('Portal 2 Audio Fix Tool')
root.geometry('600x400')


def start_action():
    if messagebox.askyesno("Confirm", "Do you want to delete game folders?"):
        portal2_path = "C:\\Steam\\steamapps\\common\\Portal 2"
        folders = ["portal2", "sdk_content", "steam_input", "update"]
        if not os.path.exists(portal2_path):
            messagebox.showerror("Error", "Portal 2 is not installed.")
            return
        for i, folder in enumerate(folders):
            path = os.path.join(portal2_path, folder)
            if os.path.exists(path):
                print(f"Deleting {folder}... {(i + 1) / len(folders) * 100:.0f}%")
                shutil.rmtree(path, ignore_errors=True)
        messagebox.showinfo("Info", "Folders have been successfully deleted.")
    else:
        messagebox.showinfo("Info", "Process has been cancelled.")


label = Label(root, text="A tool for removing sound folders inside game folders", font=20, fg="black")
label.pack()

start_button = Button(root, text="Start", width=8, command=start_action)
start_button.pack()

version_label = Label(root, text="v1.0.4", fg="gray")
version_label.pack(side='bottom')

root.mainloop()