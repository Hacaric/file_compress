import math
def tobin(inpt, minimumlenght = None):
    if minimumlenght:
        return str(bin(int(inpt)))[2:].zfill(minimumlenght)
    return str(bin(inpt))[2:]
def todec(inpt):
    return int("0b" + str(inpt),2)
def get_list_of_different_chars(text):
    return sorted(set(list(text)))
def integer(input_):
    number = input_.split(".")
    return int(number[0]) + int(number[1])/(10**(len(number[1])))
def get_app_version():
    try:
        f = str(open("version.txt", "rb").read())
        version = integer(f[f.find("version:") + len("version:")  :  f.find(";")]) * 100 # multiplying by 100 for better convertion to binary
        return version
    except Exception as e:
        print("Error while reading app version(check version.txt): " + str(e))
def text_to_bin(text, use_min_len = False):
    if use_min_len:
        binary = ""
        for i in range(len(text)):
            binary += tobin(ord(text[i]), minimumlenght=use_min_len)
            #adds binary representation of character's index in ascii or unicade
        return binary
    binary = ""
    for i in range(len(text)):
        binary += tobin(ord(text[i]))
        #adds binary representation of character's index ascii or unicode
    return binary
def text_to_bin_comprime(text:str, key:list[str], debug_divider = "", use_min_len = False) -> str:
    if use_min_len:
        binary = ""
        for i in range(len(text)):
            binary.append(debug_divider + tobin(key.index(text[i]), minimumlenght=use_min_len))
            #adds binary representation of character's index in keys
        return binary
    binary = ""
    for i in range(len(text)):
        binary += debug_divider + tobin(key.index(text[i]))
        #adds binary representation of character's index in keys
    return binary
def tolendividableby8(binary):
    return binary.zfill(math.ceil(len(binary)/8)*8)
def force_text_from_binary(binary):
    text = ""
    for i in range(0, len(binary), 8):
        text += chr(todec(binary[i:i+8]))
    return text
def comprime(file, output_type, output_file = None, rewrite = False):
    text = open(file, "rt").read()
    different_chars_list = get_list_of_different_chars(text)
    len_of_comprimed_char = math.ceil(math.log2(len(different_chars_list)))
    chars_binary = text_to_bin("".join(different_chars_list))
    comprimed_text = text_to_bin_comprime(text, different_chars_list)
    comprimed_text_offset = (math.ceil(len(comprimed_text)/8)*8) - len(comprimed_text)
    comprimed_text = tolendividableby8(comprimed_text)
    version = get_app_version()
    final_bin = tobin(version, minimumlenght=8) + tobin(comprimed_text_offset, minimumlenght=8) + tobin(len_of_comprimed_char, minimumlenght=8) + tobin(len(chars_binary), minimumlenght=8) + chars_binary + comprimed_text
    final_text = force_text_from_binary(final_bin)
    

    if output_type == "console":
        print("Binary:", final_bin)
        print("Text:", final_text)
    elif output_type == "file":
        if not output_file:
            output_file = ".".join(file.split(".")[:-1]) + ".cpm"
        try:
            try:
                if rewrite:
                    ""+0
                while True:
                    open(output_file, "r")
                        #Throws error -> mean continue with filename you have, beacouse its free
                    print(f"Opperation failed: file {output_file} already exist. Saving results to {'_' + output_file}")
                    output_file = "_" + output_file
            except:
                print(f"Creating file: {output_file}")
                f = open(output_file, "w").write(final_text)
                #f = open(output_file + "b", "wb").write(final_bin)
        except Exception as e:
            exit("Error, quitting: " + e)
    return final_text