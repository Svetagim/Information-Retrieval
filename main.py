import parse_file
import files_utils
import server
import shutil


def Insert_New_Docs():
    docs_arr = files_utils.Pull_Documents()  # Retrieve the docs available in the wait folder
    print(docs_arr)
    for doc in docs_arr:
        doc_index = parse_file.Create_Doc_Index(doc)
        doc_metadata = parse_file.Get_Doc_Metadata(doc_index)
        print(doc)
        log("Handeling file: " + doc_metadata[1])
        docCol = parse_file.connectToDB("docs")
        log("Insert doc metadata into the DB")
        parse_file.Insert_New_Doc_Record_to_DB(doc_metadata, docCol)
        doc_index = parse_file.Filter_Index(doc_index)
        print(doc_index)
        log("Parsing the index")
        parse_file.Parse_Index(doc_index, doc_metadata[0], "indexCollection")
        doc.close()
    print()
    parse_file.Sort_Index_File("indexCollection")
    log("Creating the Invert File")
    parse_file.Create_Inverted_File("indexCollection")
    files_utils.moveDocsBetweenDirs()


def Ignore_Document(doc_name):
    docsCol = parse_file.connectToDB("docs")
    query = {
        "name": doc_name
    }
    document = docsCol.find_one(query)
    try:
        print(document['name'])
        query = {
            "_id": document['_id'],
            "ignore": "false"
        }
        newquery = {
            "$set":{
                "_id": document['_id'],
                "ignore": "true"
            }
        }
        docsCol.update_one(query,newquery)

        dest = 'ignore_documents/'
        source = 'documents/'
        shutil.move(source + doc_name + ".txt", dest + doc_name + ".txt")
        return True
    except:
        print("No record!")

def UnIgnore_Document(doc_name):
    docsCol = parse_file.connectToDB("docs")
    query = {
        "name": doc_name
    }
    document = docsCol.find_one(query)
    try:
        print(document['name'])
        query = {
            "_id": document['_id'],
            "ignore": "true"
        }
        newquery = {
            "$set":{
                "_id": document['_id'],
                "ignore": "false"
            }
        }
        docsCol.update_one(query,newquery)

        source = 'ignore_documents/'
        dest = 'documents/'
        shutil.move(source + doc_name + ".txt", dest + doc_name + ".txt")
        return True
    except:
        print("No record!")


def log(msg):
    print("- " + msg)


def Clear_Old_Record_in_DB():
    col_to_del = parse_file.connectToDB("docs")
    col_to_del.delete_many({})
    col_to_del = parse_file.connectToDB("indexCollection")
    col_to_del.delete_many({})
    col_to_del = parse_file.connectToDB("indexCollection_new")
    col_to_del.delete_many({})
    col_to_del = parse_file.connectToDB("inverted")
    col_to_del.delete_many({})



def Clear_One_Record_in_DB(file):
    col_to_del = parse_file.connectToDB("docs")
    col_to_del.remove({"name": file})
    # col_to_del = parse_file.connectToDB("indexCollection_new")
    # col_to_del.delete_many({})
    files_utils.moveBackBetweenDirs(file)


if __name__ == '__main__':
    #Clear_Old_Record_in_DB()
    #Insert_New_Docs()

    server.app.run()
    exit(0)