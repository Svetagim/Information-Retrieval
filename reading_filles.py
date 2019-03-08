import glob
import errno
import os
import shutil
import nltk


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

# ----- Creating index files -----

nltk_tokens = []

for file in files:
    sentence_data = file.read()
    nltk_tokens += nltk.word_tokenize(sentence_data)
print(nltk_tokens)


# ----- Moving files from awaiting_documents folder to Documents folder -----

# source = 'awaiting_documents/'
# dest = 'Documents/'
# files = os.listdir(source)
#
# for f in files:
#     shutil.move(source+f, dest)