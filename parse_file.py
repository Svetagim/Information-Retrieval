import pymongo

def connectToDB():
    myClient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myClient["ir"]
    DocCol = mydb["docCollection"]
    return DocCol


def findMaxDocID(DocCol):
    max = 0
    for doc in DocCol.find():
        print(doc['id'])
        if (doc['id'] > max):
            max = doc['id']
    return max + 1

if __name__ == '__main__':
    DocCol = connectToDB()
    doc_id = findMaxDocID(DocCol) # new id for the new doc