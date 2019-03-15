import parse_file2
import files_utils
import multiprocessing

def Insert_New_Docs():
    docs_arr = files_utils.Pull_Documents()  # Retrieve the docs available in the wait folder
    for doc in docs_arr:
        doc_index = parse_file2.Create_Doc_Index(doc)
        doc_metadata = parse_file2.Get_Doc_Metadata(doc_index)
        print()
        log("Handeling file: " + doc_metadata[1])
        docCol = parse_file2.connectToDB("docs")
        log("Insert doc metadata into the DB")
        parse_file2.Insert_New_Doc_Record_to_DB(doc_metadata, docCol)
        doc_index = parse_file2.Filter_Index(doc_index)
        log("Parsing the index")
        parse_file2.Parse_Index(doc_index, doc_metadata[0], "indexCollection")
        doc.close()
    print()
    parse_file2.Sort_Index_File("indexCollection")
    log("Creating the Invert File")
    parse_file2.Create_Inverted_File("indexCollection")
    files_utils.moveDocsBetweenDirs()

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
    #Clear_Old_Record_in_DB()
    Insert_New_Docs()
    exit(0)