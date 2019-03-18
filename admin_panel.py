import glob
import errno
import os
import shutil


def WaitingFiles():
    path = 'awaiting_documents/*.txt'
    docs_path = glob.glob(path)
    docs_arr = []
    #Read each doc that located in the wait docs folder
    #and put them inside 'docs_arr' array
    for doc_name in docs_path:
        try:
            with open(doc_name) as inf:
                txt = inf.readline()
                docs_arr.append(txt)
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    return docs_arr


def retrievedFiles():
    path = 'documents/*.txt'
    docs_path = glob.glob(path)
    docs_arr = []
    #Read each doc that located in the wait docs folder
   # and put them inside 'docs_arr' array
    for doc_name in docs_path:
        try:
            with open(doc_name) as inf:
                txt = inf.readline()
                docs_arr.append(txt)
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    return docs_arr
