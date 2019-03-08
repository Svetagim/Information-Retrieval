import glob
import errno
import os
import shutil
import nltk


# ----- Reading files from awaiting_documents folder -----
path = 'awaiting_documents/*.txt'
docs_path = glob.glob(path)

# ----- Pull Document from 'awaiting_documents' and start handle him -----
def Pull_Documents():
    docs_arr = []
    # Read each doc that located in the wait docs folder
    # and put them inside 'docs_arr' array
    for doc_name in docs_path:
        try:
            docs_arr.append(open(doc_name))
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    return docs_arr

def Get_Doc_MetaData(doc_index):
    # Find occurrence of the word 'by'
    # For doc name
    index = 0
    doc_name=""
    for word in doc_index:
        if(word == 'by'):
            break
        index = index + 1
    for word in range(index):
        doc_name += doc_index[word] + " "
    # remove the space after the last word
    doc_name = doc_name.rstrip()
    # END doc name

    # Find occurrence of the char ':'
    # For doc author
    index = 0
    doc_name = ""
    for word in doc_index:
        if (word == ':'):

            break
        index = index + 1
    for word in range(index):
        doc_name += doc_index[word] + " "
    # remove the space after the last word
    doc_name = doc_name.rstrip()
    # END doc author

    return doc_name


    # ----- Creating index files -----
def Create_Doc_Index(doc):
    sentence_data = doc.read()
    nltk_tokens = nltk.word_tokenize(sentence_data)
    return nltk_tokens


# ----- Moving files from awaiting_documents folder to documents folder -----
def moveDocsBetweenDirs():
    source = 'awaiting_documents/'
    dest = 'documents/'
    files = os.listdir(source)

    for f in files:
        shutil.move(source+f, dest+f)
    return True