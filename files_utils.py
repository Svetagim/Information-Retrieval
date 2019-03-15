import glob
import errno
import os
import shutil


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
    doc_metadata = []
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
    doc_metadata.append(doc_name)
    # END doc name

    # Find occurrence of the char ':'
    # For doc author
    left_border = 0

    doc_author = ""
    for word in doc_index:
        if (word == ':'):
            break
        left_border = left_border + 1
    left_border = left_border + 1
    right_border = left_border
    for word in range(right_border, right_border+5):
        if (doc_index[word] == '('):
            break
        right_border = right_border + 1
    for word in range(left_border, right_border):
        doc_author += " " + doc_index[word]
    # remove the space after the last word
    doc_author = doc_author.rstrip()
    doc_author = doc_author.lstrip()
    doc_metadata.append(doc_author)
    # END doc author

    # Find occurrence of the char ':'
    # For doc date of creation
    left_border = right_border + 1
    doc_metadata.append(doc_index[left_border])
    # END doc author

    return doc_metadata


    # ----- Creating index files -----


# ----- Moving files from awaiting_documents folder to documents folder -----
def moveDocsBetweenDirs():
    source = 'awaiting_documents/'
    dest = 'documents/'
    files = os.listdir(source)

    for f in files:
         shutil.move(source+f, dest+f)
    return True