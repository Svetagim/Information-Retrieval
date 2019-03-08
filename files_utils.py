import glob
import errno
import os
import shutil
import nltk


# ----- Reading files from awaiting_documents folder -----
path = 'awaiting_documents/*.txt'
awaiting_docs_path = glob.glob(path)

# ----- Pull Document from 'awaiting_documents' and start handle him -----
def Pull_Documents():
    docs_arr = []
    # Read each doc that located in the wait docs folder
    # and put them inside 'docs_arr' array
    for doc_name in awaiting_docs_path:
        try:
            docs_arr.append(open(doc_name))
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    return docs_arr


    # ----- Creating index files -----
def Create_Doc_Index(doc):
    sentence_data = doc.read()
    nltk_tokens = nltk.word_tokenize(sentence_data)
    return nltk_tokens


# ----- Moving files from awaiting_documents folder to Documents folder -----
def moveDocBetweenDirs(doc):
    source = 'awaiting_documents/'
    dest = 'Documents/'
    shutil.move(source+doc, dest)