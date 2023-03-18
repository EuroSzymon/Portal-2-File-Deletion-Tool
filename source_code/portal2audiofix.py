import subprocess # importing the subprocess library used to make new processes, connecting with other processes and processing end of the process
import sys # importing the sys library used to access functions and variables which they can make interactable with Python interpeter
import os # importing the os library used to make code interactable with user operating system
import shutil # importing the shutil library used to execute tasks like deleting elements from PC
# Path of Portal 2 needed to function with other code lines
portal2_path = "C:\\Steam\\steamapps\\common\\Portal 2"  
# Game folders to delete by the code, needed to function with other code lines
folders = ["portal2", "sdk_content", "steam_input", "update"]
# Error message when program detects that user is not installed Portal 2
if not os.path.exists(portal2_path):
    print("Portal 2 is not installed.")
    exit()

# Command line visibility config code
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
if sys.stdout.isatty():
    startupinfo.dwFlags ^= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE

# Process of deleting game folders
for i, folder in enumerate(folders):
    path = os.path.join(portal2_path, folder)
    if os.path.exists(path):
        print(f"Deleting {folder}... {(i + 1) / len(folders) * 100:.0f}%")
        shutil.rmtree(path)

# This message appears when game folders has been deleted without any issues
print("Folders have been successfully deleted.")