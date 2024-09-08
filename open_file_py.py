import tkinter as tk
from tkinter import filedialog

def open_file_explorer():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()
    return file_path
def check_file(file):
    try:
        open(file, 'r')
    except FileNotFoundError:
        return False
    return True
def select_file(selected):
    if not selected:
        print("No file selected, opening explorer.")
        selected = open_file_explorer()
    filename_valid = check_file(selected)
    while not filename_valid:
        print("Invalid file, please select a valid file.")
        selected = open_file_explorer()
        filename_valid = check_file(selected)
    return selected