import math
def tobin(inpt, minimumlenght = None):
    if minimumlenght:
        return str(bin(int(inpt)))[2:].zfill(minimumlenght)
    return str(bin(inpt))[2:]
def todec(inpt): # from binary to decimal
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
def decode_by_pattern(text):
    # Test file version
    version = todec(text[0:8])/100
    if not version == get_app_version():
        if not "y" == input(f"Your file's version({version}) is not the right. App version is {get_app_version()}. This can cause not right decompression of file. Try downloading older app version from github.\n\nDo you want to continue?(y/n) >> ")
            exit("Wrong version.")
    text_offset = todec(text[8:16])
    len_of_comprimed_char = todec(text[16:24])
    len_of_diff_char = todec(text[24:32])
    different_chars_list = []
    for i in range(32, len_of_diff_char + 32):
        different_chars_list.append(text[i*8:(i+1)*8])
    comprimed_text = (text[len_of_diff_char * 8 + 32:])[text_offset-1:]
    return different_chars_list, comprimed_text
def decode(len_of_comprimed_char, comprimed_text, different_chars_list):
    text = ""
    for i in range(0, len(comprimed_text), len_of_comprimed_char):
        text += different_chars_list[todec(comprimed_text[i:i+len_of_comprimed_char])]
    return text
def decomprime(file, output_type, output_file = None, rewrite = False):
    try:    
        text = open(file, "rt").read()
    except Exception as e:
        print("Error opening file. Aborting.")
        exit("Ext message: File_error")
    len_of_comprimed_char, different_chars_list, comprimed_text = decode_by_pattern(text)
    decomprimed_text = decode(len_of_comprimed_char, comprimed_text, different_chars_list)
    if output_type == "console":
        print("Text:", decomprimed_text)
    elif output_type == "file":
        if not output_file:
            output_file = ".".join(file.split(".")[:-1]) + ".txt"
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
                f = open(output_file, "w").write(decomprimed_text)
                #f = open(output_file + "b", "wb").write(final_bin)
        except Exception as e:
            exit("Error, quitting: " + e)
    return final_text