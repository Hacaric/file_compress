def tobin(inpt, minimumlenght = None):
    if minimumlenght:
        return str(bin(inpt))[2:].zfill(minimumlenght)
    return str(bin(inpt))[2:]
def todec(inpt):
    return int("0b" + str(inpt),2)
def get_list_of_different_chars(text):
    return sorted(set(list(text)))
def text_to_bin(text, key, divider = "", use_max_len = False):
    if use_max_len:
        binary = []
        for i in range(len(text)):
            binary.append(divider + tobin(key.index(text[i])))
            #adds binary representation of character's index in keys
        return binary
    binary = ""
    for i in range(len(text)):
        binary += divider + tobin(key.index(text[i]))
        #adds binary representation of character's index in keys
    return binary
def comprime(file):
    text = open(file, "rb").read()
    diff_chars = get_list_of_different_chars(text)
    chars_binary = text_to_bin()