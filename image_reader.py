from os import listdir
import re
import pytesseract

path = r"C:\Users\atz\Desktop\Python\marina\images\import data"

files = listdir(path)

for f in files:
    im = path + "\\" + f
    text = pytesseract.image_to_string(im, lang='eng')

lines = text.splitlines()
lines = list(filter(lambda x: x.strip(), lines))[2:]
print(lines)




"""
print(lines[0].split("Name", 1)[1])
print(lines[1].split("Type", 1)[1])
print(lines[2].split("LOA", 1)[1])
print(lines[3].split("Beam", 1)[1])
print(lines[4].split("Draft", 1)[1])
print(lines[5].split("Type", 1)[1])
print(lines[6].split("weight", 1)[1])
print(lines[7].split("Type", 1)[1])
print(lines[8].split("Spreader", 1)[1])
print(lines[9].split("Type", 1)[1])
print(lines[10].split("FWD", 1)[1])
print(lines[11].split("AFT", 1)[1])
print(lines[12].split("Type", 1)[1])
print(lines[13].split("Pos", 1)[1])
print(lines[14].split("Pos", 1)[1])
print(lines[15])
"""




"""
Boat Name
Class/Type
LOA
Beam
Draft
Keel Type
Dead Weight
Shaft Type

Spreader
Strop Type
Links FWD
Links AFT
Cradle Type
FWD Strop Pos
AFT Strop Pos
Mast Up/Down
"""