import pymongo
import nltk
import re


def connectToDB(collection):
    myClient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myClient["ir"]
    col = mydb[collection]
    return col


def findMaxDocID(DocCol):
    x = DocCol.find_one()
    if(x != "none"):
        max = 0
        for doc in DocCol.find():
            if (doc['id'] > max):
                max = doc['id']
        return max + 1
    else:
        return 0


def Create_Doc_Index(doc):
    sentence_data = doc.read()
    nltk_tokens = nltk.word_tokenize(sentence_data)
    return nltk_tokens


def Parsing(doc_index):
    left_border = doc_index.index(')') + 1
    new_doc_index = []
    for word_index in range(left_border, len(doc_index)):
        new_doc_index.append(doc_index[word_index])
    return new_doc_index

def Insert_New_Doc_Record_to_DB(doc_metadata, docCollection):
    myquery = {
        "id": doc_metadata[3],
        "name": doc_metadata[0],
        "author": doc_metadata[1],
        "date_of_create": doc_metadata[2]
    }
    docCollection.insert_one(myquery)


def Build_Invert_File(doc_index, doc_id):
    # Building the inverted table
    # - Filtering + Parsing
    invertColl = connectToDB("invertFile")
    index_to_delete = 0
    for word in doc_index:
        word = word.lstrip()
        word = word.rstrip()
        word = word.lower()

        if (str(re.findall(r'[a-zA-Z]', word)) == "[]"):
            del doc_index[index_to_delete]
        else:
            myquery = {
                "Term": word,
                "Doc Id": doc_id,
                "Hit": 0
            }
            invertColl.insert_one(myquery)
        index_to_delete += 1


def Sort_Invert_File():
    invertColl = connectToDB("invertFile")
    # - Sort the invertCollection in db
    pipeline = [
        {"$sort": {"Term": 1}},
        {"$out": "invertFile"}
    ]
    invertColl.aggregate(pipeline)


def Sort_Invert_File_Frequency(doc_index):
    counter = nltk.Counter(doc_index)
    print(counter)

    # invertColl = connectToDB("invertFile")
    # counter = 1
    # test_i = 1
    # for term in invertColl.find():
    #     print("first loop: " + str(term))
    #     myquery = {"_id": { "$ne": term['_id'] }, "Term": term['Term'], "Doc Id": term['Doc Id']}
    #     for x in invertColl.find(myquery):
    #         print("second loop: " + str(x))
    #         myquery = {
    #             "_id": x["_id"]
    #         }
    #         invertColl.delete_one(myquery)
    #         counter += 1
    #     myquery = {
    #         "_id": term['_id'],
    #         "Hit": term['Hit'],
    #     }
    #     newvalues = {
    #         "$set": {
    #             "_id": term['_id'],
    #             "Hit": counter
    #         }
    #     }
    #     invertColl.update_one(myquery, newvalues)
    #     counter = 1
    #     if ( test_i == 2):
    #         break
    #     test_i += 1