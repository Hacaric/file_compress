#code cleaned with cody

import math
import sys
import os
import tkinter as tk
from tkinter import filedialog, ttk

BYTE_LEN = 7

def resource_path(relative_path):
    """Get the absolute path to a resource. Works for dev and PyInstaller-compiled mode."""
    try:
        # If running in a PyInstaller bundle
        base_path = sys._MEIPASS
    except AttributeError:
        # If running in development (script mode)
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def to_len_divisible_by_byte_len(binary):
    return binary.zfill(math.ceil(len(binary) / BYTE_LEN) * BYTE_LEN)

def ceil_log2(num):
    num = math.ceil(math.log2(num))
    return 1 if num == 0 else num

def to_bin(input_, minimum_length=None):
    if isinstance(minimum_length, int):
        return bin(int(input_))[2:].zfill(minimum_length)
    return bin(input_)[2:]

def to_dec(input_):
    return int(f"0b{input_}", 2)

def get_list_of_different_chars(text):
    return sorted(set(text))

def get_app_version():
    return 1.0
    # try:
    #     with open(resource_path("version.txt"), "rb") as f:
    #         content = f.read().decode()
    #         version_str = content[content.find("version:") + len("version:"):content.find(";")]
    #         return int(float(version_str) * 100)
    # except Exception:
    #     return 1.0

def text_to_bin(text, use_min_len=BYTE_LEN):
    if use_min_len:
        return ''.join(to_bin(ord(char), minimum_length=use_min_len) for char in text)
    return ''.join(to_bin(ord(char)) for char in text)

def text_to_bin_compress(text: str, key: list[str], min_len: int) -> str:
    return ''.join(to_bin(key.index(char), minimum_length=min_len) for char in text)

def force_text_from_binary(binary):
    return ''.join(chr(to_dec(binary[i:i+BYTE_LEN])) for i in range(0, len(binary), BYTE_LEN))

def compress(file, output_type, output_file=None, rewrite=False):
    with open(resource_path(file), "rt") as f:
        text = f.read()
    
    if not text:
        raise ValueError("File is empty")

    different_chars_list = get_list_of_different_chars(text)
    len_of_compressed_char = ceil_log2(len(different_chars_list))
    chars_binary = text_to_bin("".join(different_chars_list))
    compressed_text = text_to_bin_compress(text, different_chars_list, len_of_compressed_char)
    compressed_text_offset = (math.ceil(len(compressed_text) / BYTE_LEN) * BYTE_LEN) - len(compressed_text)
    compressed_text = to_len_divisible_by_byte_len(compressed_text)

    version = get_app_version()
    final_bin = (
        to_bin(version, minimum_length=BYTE_LEN) +
        to_bin(compressed_text_offset, minimum_length=BYTE_LEN) +
        to_bin(len_of_compressed_char, minimum_length=BYTE_LEN) +
        to_bin(len(different_chars_list), minimum_length=BYTE_LEN) +
        chars_binary +
        compressed_text
    )

    final_text = force_text_from_binary(final_bin)

    if output_type == "file":
        if not output_file.endswith(".cpm"):
            output_file = f"{output_file.rstrip('.')}.cpm"
        
        if not rewrite:
            while True:
                try:
                    open(resource_path(output_file), "r").close()
                    output_file = f"_{output_file}"
                except FileNotFoundError:
                    break

        with open(resource_path(output_file), "w") as f:
            f.write(final_text)

    return final_text

def decode_by_pattern(text):
    version = to_dec(text[0:BYTE_LEN]) / 100
    app_version = get_app_version() / 100
    # if version != app_version:
    #     if input(f"Your file's version ({version}) does not match the app version ({app_version}). "
    #              f"This may cause incorrect decompression. "
    #              f"Do you want to continue? (y/n) >> ").lower() != "y":
    #         raise ValueError("Version mismatch")

    text_offset = to_dec(text[BYTE_LEN:BYTE_LEN*2])
    len_of_compressed_char = to_dec(text[BYTE_LEN*2:BYTE_LEN*3])
    len_of_diff_char = to_dec(text[BYTE_LEN*3:BYTE_LEN*4])
    
    different_chars_list = [
        chr(to_dec(text[i:i + BYTE_LEN]))
        for i in range(BYTE_LEN*4, len_of_diff_char*BYTE_LEN + (4*BYTE_LEN), BYTE_LEN)
    ]
    
    compressed_text = text[len_of_diff_char*BYTE_LEN + (4*BYTE_LEN) + text_offset:]
    return len_of_compressed_char, different_chars_list, compressed_text

def decode(len_of_compressed_char, compressed_text, different_chars_list):
    return ''.join(
        different_chars_list[to_dec(compressed_text[i:i+len_of_compressed_char])]
        for i in range(0, len(compressed_text), len_of_compressed_char)
    )

def decompress(file, output_type, output_file=None, rewrite=False):
    try:
        with open(resource_path(file), "rt") as f:
            text = f.read()
    except Exception as e:
        raise IOError(f"File error: {str(e)}")

    text = ''.join(to_bin(ord(char), minimum_length=BYTE_LEN) for char in text)
    len_of_compressed_char, different_chars_list, compressed_text = decode_by_pattern(text)
    decompressed_text = decode(len_of_compressed_char, compressed_text, different_chars_list)

    if output_type == "file":
        if not output_file:
            output_file = f"{'.'.join(file.split('.')[:-1])}.txt"
        
        if not rewrite:
            while True:
                try:
                    open(resource_path(output_file), "r").close()
                    output_file = f"_{output_file}"
                except FileNotFoundError:
                    break

        with open(resource_path(output_file), "w") as f:
            f.write(decompressed_text)

    return decompressed_text

def select_file():
    filename = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)
    option_var.set("Decompress" if filename.endswith(".cmp") else "Compress")

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
    if not file_entry.get():
        update_processing_info("Please select a file")
        return
    
    try:
        update_processing_info("Processing...")
        selected_file = file_entry.get()
        selected_option = option_var.get()
        output_path = resource_path(f"{output_location_entry.get()}/{output_file_entry.get()}")
        rewrite_option = rewrite_var.get() == "Yes"
        
        if selected_option == "Compress":
            compress(selected_file, "file", output_path, rewrite_option)
            update_processing_info("Compression completed")
        elif selected_option == "Decompress":
            decompress(selected_file, "file", output_path, rewrite_option)
            update_processing_info("Decompression completed")
        else:
            update_processing_info("Please select an action")
    except Exception as e:
        update_processing_info(f"An error occurred: {str(e)}")

root = tk.Tk()
root.title("File Processing")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
style.configure("TButton", font=("Arial", 10))
style.configure("TEntry", font=("Arial", 10))
style.configure("TOptionMenu", font=("Arial", 10))

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
