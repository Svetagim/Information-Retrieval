from nltk.corpus import stopwords
import parse_file
import files_utils


def Insert_New_Docs():
    docs_arr = files_utils.Pull_Documents()  # Retrieve the docs available in the wait folder
    for doc in docs_arr:
        doc_index = parse_file.Create_Doc_Index(doc)
        doc_metadata = files_utils.Get_Doc_MetaData(doc_index)
        docsCollection = parse_file.connectToDB("docCollection")
        doc_id = parse_file.findMaxDocID(docsCollection)  # new id for the new doc
        doc_metadata.append(doc_id)
        log("Processing: " + str(int(doc_id)) + " " + doc_metadata[0] + " " + doc_metadata[1] + " " + doc_metadata[2])
        parse_file.Insert_New_Doc_Record_to_DB(doc_metadata, docsCollection)
        log("The new doc has documented in the DB")
        parse_file.Build_Invert_File(doc_index, doc_id)
    log("Build the invert file")
    log("Parse + Sort the table")
    parse_file.Sort_Invert_File()
    # files_utils.moveDocsBetweenDirs()
    # print(stopwords.words('english'))


def log(msg):
    print("- " + msg)


if __name__ == '__main__':
    Insert_New_Docs()
    exit(0)