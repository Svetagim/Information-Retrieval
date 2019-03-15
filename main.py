from nltk.tokenize import word_tokenize
import parse_file2
import files_utils


# def Insert_New_Docs():
#     docs_arr = files_utils.Pull_Documents()  # Retrieve the docs available in the wait folder
#     for doc in docs_arr:
#         doc_index = parse_file.Create_Doc_Index(doc)
#         doc_metadata = files_utils.Get_Doc_MetaData(doc_index)
#         docsCollection = parse_file.connectToDB("docCollection")
#         doc_id = parse_file.findMaxDocID(docsCollection)  # new id for the new doc
#         doc_metadata.append(doc_id)
#         log("Processing: " + str(int(doc_id)) + " " + doc_metadata[0] + " " + doc_metadata[1] + " " + doc_metadata[2])
#         parse_file.Insert_New_Doc_Record_to_DB(doc_metadata, docsCollection)
#         log("The new doc has documented in the DB")
#         doc_index = parse_file.Parsing(doc_index)
#         print(doc_index)
#         exit(1)
#         parse_file.Build_Invert_File(doc_index, doc_id)
#     log("Build the invert file")
#     log("Parse + Sort the table")
#     parse_file.Sort_Invert_File()
#     parse_file.Sort_Invert_File_Frequency()
#     # files_utils.moveDocsBetweenDirs()
    # print(stopwords.words('english'))


def Insert_New_Docs2():
    docs_arr = files_utils.Pull_Documents()  # Retrieve the docs available in the wait folder
    mash_index_file = []
    for doc in docs_arr:
        doc_index = parse_file2.Create_Doc_Index(doc)
        doc_metadata = parse_file2.Get_Doc_Metadata(doc_index)
        docCol = parse_file2.connectToDB("docs")
        parse_file2.Insert_New_Doc_Record_to_DB(doc_metadata, docCol)
        doc_index = parse_file2.Filter_Index(doc_index)
        parse_file2.Parse_Index(doc_index, doc_metadata[0], "indexCollection")
    parse_file2.Sort_Index_File("indexCollection")
    parse_file2.Create_Inverted_File("indexCollection")


def log(msg):
    print("- " + msg)


def Clear_Old_Record_in_DB():
    col_to_del = parse_file2.connectToDB("docs")
    col_to_del.delete_many({})
    col_to_del = parse_file2.connectToDB("indexCollection")
    col_to_del.delete_many({})
    col_to_del = parse_file2.connectToDB("indexCollection_new")
    col_to_del.delete_many({})
    col_to_del = parse_file2.connectToDB("inverted")
    col_to_del.delete_many({})

if __name__ == '__main__':
    #Insert_New_Docs()
    Clear_Old_Record_in_DB()
    Insert_New_Docs2()
    exit(0)