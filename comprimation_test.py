import compression
import decompression
#from testing import *
# print(comprimation.text_to_bin_comprime("hellolllll",["h","e","l","o"],debug_divider="\n"))
# print(comprimation.text_to_bin("a", use_min_len=8))
# print(comprimation.get_list_of_different_chars("abcdd"))
#
print(compression.compress("input.txt", "file", "output.cpm", rewrite = True))
print(decompression.decompress("output.cpm", "file", "output2.txt", rewrite = True))
#print(get_ascii_from_text(open("output.txt", "rt").read()))
#print(decompression.decomprime("output.txt", "file", "input.txt", rewrite = True))
