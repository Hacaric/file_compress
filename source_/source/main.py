

import open_file_py
import compression
import decompression
import tkinter as tk
from tkinter import filedialog, ttk

def select_file():
    filename = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)
    if filename.endswith(".cmp"):
        option_var.set("Decompress")
    else:
        option_var.set("Compress")

def select_output_location():
    output_dir = filedialog.askdirectory()
    output_location_entry.delete(0, tk.END)
    output_location_entry.insert(0, output_dir)

def update_processing_info(message):
    processing_info.set(message)
    root.update_idletasks()

def process():
    if not output_file_entry.get():
        update_processing_info("Please enter an output file name")
        return
    elif not file_entry.get():
        update_processing_info("Please select a file")
        return
    
    try:
        update_processing_info("Processing...")
        selected_file = file_entry.get()
        selected_option = option_var.get()
        output_path = f"{output_location_entry.get()}/{output_file_entry.get()}"
        rewrite_option = rewrite_var.get() == "Yes"
        
        if selected_option == "Compress":
            compression.compress(selected_file, "file", output_path, rewrite_option)
            update_processing_info("Compression completed")
        elif selected_option == "Decompress":
            decompression.decompress(selected_file, "file", output_path, rewrite_option)
            update_processing_info("Decompression completed")
        else:
            update_processing_info("Please select an action")
    except Exception as e:
        update_processing_info(f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("File Processing")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
style.configure("TButton", font=("Arial", 10))
style.configure("TEntry", font=("Arial", 10))
style.configure("TOptionMenu", font=("Arial", 10))

# Create and pack widgets
frame = ttk.Frame(root, padding="10 10 10 10", style="TFrame")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Select a file:").grid(column=0, row=0, sticky=tk.W, pady=5)
file_entry = ttk.Entry(frame, width=50)
file_entry.grid(column=0, row=1, sticky=(tk.W, tk.E), padx=5)
ttk.Button(frame, text="Browse", command=select_file).grid(column=1, row=1, sticky=tk.W)

ttk.Label(frame, text="Select output location:").grid(column=0, row=2, sticky=tk.W, pady=5)
output_location_entry = ttk.Entry(frame, width=50)
output_location_entry.grid(column=0, row=3, sticky=(tk.W, tk.E), padx=5)
ttk.Button(frame, text="Browse", command=select_output_location).grid(column=1, row=3, sticky=tk.W)

ttk.Label(frame, text="Output file name:").grid(column=0, row=4, sticky=tk.W, pady=5)
output_file_entry = ttk.Entry(frame, width=50)
output_file_entry.grid(column=0, row=5, columnspan=2, sticky=(tk.W, tk.E), pady=5)

ttk.Label(frame, text="Select an option:").grid(column=0, row=6, sticky=tk.W, pady=5)
option_var = tk.StringVar(root)
option_var.set("Choose action")
option_menu = ttk.OptionMenu(frame, option_var, "Choose action", "Compress", "Decompress")
option_menu.grid(column=0, row=7, columnspan=2, sticky=(tk.W, tk.E), pady=5)

ttk.Label(frame, text="Rewrite file if exist?:").grid(column=0, row=8, sticky=tk.W, pady=5)
rewrite_var = tk.StringVar(root)
rewrite_var.set("No")
rewrite_option = ttk.OptionMenu(frame, rewrite_var, "No", "Yes")
rewrite_option.grid(column=0, row=9, columnspan=2, sticky=(tk.W, tk.E), pady=5)

processing_info = tk.StringVar()
processing_info.set("Ready to process")
ttk.Label(frame, textvariable=processing_info).grid(column=0, row=10, columnspan=2, pady=5)

ttk.Button(frame, text="Process", command=process).grid(column=0, row=11, columnspan=2, pady=10)

for child in frame.winfo_children():
    child.grid_configure(padx=5)

if __name__ == "__main__":
    root.mainloop()
