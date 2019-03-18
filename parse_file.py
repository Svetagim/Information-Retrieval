import pymongo
import nltk
from collections import Counter
#from nltk.corpus import stopwords


def connectToDB(collection):
    myClient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myClient["ir"]
    col = mydb[collection]
    return col


def findMaxDocID(DocCol):
    x = DocCol.find().count()
    return x


def Insert_New_Doc_Record_to_DB(doc_metadata, docCollection):
    myquery = {
        "id": doc_metadata[0],
        "name": doc_metadata[1],
        "author": doc_metadata[2],
        "date_of_create": doc_metadata[3]
    }
    docCollection.insert_one(myquery)


def Get_Doc_Metadata(doc_index):
    doc_metadata = []
    doc_id = findMaxDocID(connectToDB("docs"))
    doc_metadata.append(doc_id)
    # Find occurrence of the word 'by'
    # For doc name
    index = 0
    doc_name = ""
    for word in doc_index:
        if (word == 'by'):
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
    for word in range(right_border, right_border + 5):
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
def Create_Doc_Index(doc):
    sentence_data = doc.read()
    tokens = nltk.word_tokenize(sentence_data)
    for i, t in enumerate(tokens):
        if "'" in t:
            if(t[-2] == "'"):
                left = tokens[i - 1]
                left += t
                tokens[i - 1] = str(left)
                del tokens[i]
                i += 1
    return tokens


def Filter_Index(doc_index):
    doc_index_new = []
    index = 0
    for word in doc_index:
        if(word == ")"):
            break
        index += 1
    index += 1

    #trim bad chars + lower case
    bad_chars = [",",".","--",";","#","!",":","?"]
    #stopword =
    for i in range(index, len(doc_index)):
        doc_index[i] = doc_index[i].lower()
        if((doc_index[i] not in bad_chars)):
            doc_index_new.append(doc_index[i])
    return doc_index_new


def Parse_Index(doc_index, doc_id, indexCollection):
    indexCol = connectToDB("indexCollection")
    counter = Counter(doc_index)
    for key, val in counter.items():
        myquery = {
            "term": key,
            "doc": doc_id,
            "hit": val
        }
        indexCol.insert_one(myquery)

def Sort_Index_File(collection_name):
    indexColl = connectToDB(collection_name)
    # - Sort the invertCollection in db
    pipeline = [
        {"$sort": {"term": 1}},
        {"$out": collection_name}
    ]
    indexColl.aggregate(pipeline)


def Create_Posting_File(doc_id, doc_index):
    postCol = connectToDB("inverted")
    counter = Counter(doc_index)
    query = {
        "doc": doc_id,
        "terms": counter
    }
    postCol.insert_one(query)


def sdx(st):
    soundex=st[0]
    s=1
    letters= ["AEHIOUWYaehiouwy",
    "BFPVbfpv",
    "CGJKQSXZcgjkqsxz",
    "DTdt",
    "Ll",
    "MNmn",
    "Rr"]

    i=1
    while i < len(st):
        j = 0
        while j<len(letters):
            if letters[j].find(st[i]) != -1:
                soundex+=str(j)
                break
            j+=1
        i+=1

    sound=soundex[0]
    i=1
    while i < len(soundex):
        if soundex[i]!='0':
            sound+=soundex[i]
        i+=1
    i=1
    soundex=sound[0]
    while i < len(sound):
        if sound[i] != sound[i-1]:
            soundex+=sound[i]
        i+=1

    while len(soundex)<4:
        soundex+="0"

    return(soundex)


def Create_Inverted_File(indexCollection):
    indexCol = connectToDB(indexCollection)
    newindexCol = connectToDB(indexCollection+"_new")
    length = indexCol.find().count()
    terms = indexCol.find()
    indicator = 0
    locations = []

    for i in range(0, length):
        try:
            if(indicator > length-1):
                break
            locations.append({'doc': terms[indicator]['doc'], 'hit': terms[indicator]['hit']})
            term = terms[indicator]['term']
            counter = 1
            while True:
                indicator += 1
                if(indicator >= length):
                    break
                elif(terms[indicator]['term'] != term):
                    break
                locations.append({'doc': terms[indicator]['doc'], 'hit': terms[indicator]['hit']})
                counter += 1
            query = {
                "term": term,
                "soundex": sdx(term),
                "num_of_docs": counter,
                "locations": locations
            }
            newindexCol.insert_one(query)
            locations = []
        except():
            print("Error!")
            for i in range(0, length):
                print(terms[i]['term'])
            print("indicator: " + str(indicator))
            print("Doc: " + str(terms[indicator-1]['doc']))