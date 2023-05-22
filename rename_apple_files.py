import os
import pathlib
from os import walk

folder_path = "C:/Users/aemig/OneDrive - Buro Happold/00_apple_swift/apple_swift_karl_markup/LP2"

for (dirpath, dirnames, filenames) in walk(folder_path):
    for filename in filenames:
        print(filename, "len", len(filename))
        if len(filename) > 30:
            os.rename(src=os.path.join(folder_path, filename), dst=os.path.join(folder_path, filename[36:]))
