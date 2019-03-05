import glob
import errno
import os
import shutil

# ----- Reading files from awaiting_documents folder -----

path = 'awaiting_documents/*.txt'
folder = glob.glob(path)
files = []
for name in folder:
    try:
        files.append(open(name))
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
for file in files:
    print(file.read())
    print()
    print("***************\n")

# ----- Moving files from awaiting_documents folder to retrieved_documents folder -----

source = 'awaiting_documents/'
dest = 'retrieved_documents/'
files = os.listdir(source)

for f in files:
    shutil.move(source+f, dest)