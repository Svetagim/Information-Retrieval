import pymongo
from nltk.corpus import stopwords


def connectToDB():
    myClient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myClient["ir"]
    DocCol = mydb["docCollection"]
    return DocCol


def findMaxDocID(DocCol):
    max = 0
    for doc in DocCol.find():
        if (doc['doc_id'] > max):
            max = doc['doc_id']
    return max + 1


if __name__ == '__main__':
    DocCol = connectToDB()
    doc_id = findMaxDocID(DocCol)  # new id for the new doc
    stopwords.words('english')
    exit(0)