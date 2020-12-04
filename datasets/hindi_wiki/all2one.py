import glob
import os

read_files = glob.glob(os.path.join(os.path.join("/home/rahul/Videos/ex/archive", "valid/valid"), "*.txt"))

with open("result2.txt", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())
