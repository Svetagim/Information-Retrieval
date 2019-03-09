from nltk.corpus import stopwords
import parse_file
import files_utils
import time


def Insert_New_Docs():
    docs_arr = files_utils.Pull_Documents()  # Retrieve the docs available in the wait folder
    for doc in docs_arr:
        doc_index = files_utils.Create_Doc_Index(doc)
        print(doc_index)
        doc_name = files_utils.Get_Doc_MetaData(doc_index)
        DocCol = parse_file.connectToDB()
        doc_id = parse_file.findMaxDocID(DocCol)  # new id for the new doc
        print(str(int(doc_id)) + " " + doc_name[0])
    # files_utils.moveDocsBetweenDirs()
    # print(stopwords.words('english'))


def log(msg):
    print("- " + msg + "\n")


if __name__ == '__main__':
    Insert_New_Docs()
    exit(0)