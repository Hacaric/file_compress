def get_ascii_from_text(text:str) -> list[int]:
    if text[0:2] == "0b":
        text = text[2:]
    indexes = []
    for i in range(len(text)-3):
        if text[i] == "\x":
            indexes.append(int(text[i:i+3]))
            i += 3
        else:
            indexes.append(ord(text[i]))
    return indexes
