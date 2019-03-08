from nltk.corpus import stopwords
import parse_file
import files_utils

docs_arr = []

if __name__ == '__main__':
    docs_arr = files_utils.Pull_Document()  # Retrieve the docs available in the wait folder
    for doc in docs_arr:
        files_utils.Create_Doc_Index(doc)
        DocCol = parse_file.connectToDB()
        doc_id = parse_file.findMaxDocID(DocCol)  # new id for the new doc
    #print(stopwords.words('english'))
    exit(0)