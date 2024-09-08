import math
bytelen = 7
def tolendividablebybytelen(binary):
    return binary.zfill(math.ceil(len(binary)/bytelen)*bytelen)
def ceillog2(num):
    num = math.ceil(math.log2(num))
    if num == 0:
        return 1
    return num
def tobin(inpt, minimumlenght = None):
    if type(minimumlenght) == int:
        value = str(bin(int(inpt)))[2:].zfill(minimumlenght)
    else:
        value = str(bin(inpt))[2:]
    # print("Debug:",len(value), value, minimumlenght)
    return value
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
        # print("Error while reading app version(check version.txt): " + str(e))
        pass
def text_to_bin(text, use_min_len = bytelen):
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
def text_to_bin_comprime(text:str, key:list[str], min_len) -> str:
    # if use_min_len:
    #     binary = ""
    #     for i in range(len(text)):
    #         binary.append(debug_divider + tobin(key.index(text[i]), minimumlenght=use_min_len))
    #         #adds binary representation of character's index in keys
    #     return binary
    binary = ""
    for i in range(len(text)):
        # print("   Adding", text[i], "index:", key.index(text[i]), "binary:", tobin(key.index(text[i]), minimumlenght=min_len))
        binary += tobin(key.index(text[i]), minimumlenght=min_len)
        #adds binary representation of character's index in keys
    return binary
def force_text_from_binary(binary):
    text = ""
    for i in range(0, len(binary), bytelen):
        text += chr(todec(binary[i:i+bytelen]))
    return text
def compress(file, output_type, output_file = None, rewrite = False):
    text = open(file, "rt").read()
    if not text:
        # print("File is empty. Aborting.")
        exit("Ext message: File_empty")
    different_chars_list = get_list_of_different_chars(text)
    print(different_chars_list)
    # print("diff:", different_chars_list)
    len_of_comprimed_char = ceillog2(len(different_chars_list))
    chars_binary = text_to_bin("".join(different_chars_list))
    # print("Text::::", text)
    comprimed_text = text_to_bin_comprime(text, different_chars_list, len_of_comprimed_char)
    comprimed_text_offset = (math.ceil(len(comprimed_text)/bytelen)*bytelen) - len(comprimed_text)
    # print("Comprimed text:::", comprimed_text)
    comprimed_text = tolendividablebybytelen(comprimed_text)
    version = get_app_version()
    final_bin = tobin(version, minimumlenght=bytelen) + tobin(comprimed_text_offset, minimumlenght=bytelen) + tobin(len_of_comprimed_char, minimumlenght=bytelen) 
    #print("Vesrion", version, tobin(version, minimumlenght=bytelen))
    #print("Comprimed text offset:", comprimed_text_offset, tobin(comprimed_text_offset, minimumlenght=bytelen))
    #print("Len of comprimed char:", len_of_comprimed_char, tobin(len_of_comprimed_char, minimumlenght=bytelen))
    final_bin += tobin(len(different_chars_list), minimumlenght=bytelen)
    #print("Len of diff_chr_list chars:", len(different_chars_list), tobin(len(different_chars_list), minimumlenght=bytelen*2))
    # print("\n\nChars binary:", len(different_chars_list))
    # print(f"\n\n\nFINAL_BIN IS LONG:{(len(final_bin))} and it % bytelen is: {(len(final_bin))%bytelen}\n")
    final_bin += chars_binary
    final_bin += comprimed_text
    # if len(final_bin) % bytelen != 0:
    #     exit("Error: final_bin is not dividable by bytelen (line 83)")
    # print("Vesrion:", version)
    final_text = force_text_from_binary(final_bin)
    if not "".join([tobin(ord(i),minimumlenght=bytelen) for i in list(final_text)]) == final_bin:
        exit("Error: final_text is not equal to final_bin")
    print("Comprimed text:", final_text)

    if output_type == "console" or True:
        # print("Binary final:", final_bin)
        # print("Text:", final_text)
        pass
    if output_type == "file":
        if output_file[-4] != ".cpm":
            if output_file[-4] == ".":
                output_file = output_file[:-4] + ".cpm"
            else:
                output_file += ".cpm"
        print("Saving to file:", output_file)
        try:
            try:
                if rewrite:
                    ""+0
                while True:
                    open(output_file, "r")
                        #Throws error -> mean continue with filename you have, beacouse its free
                    # print(f"Opperation failed: file {output_file} already exist. Saving results to {'_' + output_file}")
                    output_file = "_" + output_file
            except:
                # print(f"Writing to file: {output_file}")
                # print(f"Binary: {final_bin}")
                f = open(output_file, "w")
                f.write(final_text)
                #f = open(output_file, "wb").write(final_text.encode("ascii"))
                #f = open(output_file + "b", "wb").write(final_bin)
        except Exception as e:
            exit("Error, quitting:" + str(e))
    #return final_text
    return 0