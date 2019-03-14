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


def Get_Doc_Metadata(doc_index):
    doc_metadata = []
    doc_id = findMaxDocID(connectToDB("docsCollection"))
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
            left = tokens[i - 1]
            left += t
            tokens[i - 1] = left
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
    bad_chars = [",",".","--",";","#","!"]
    for i in range(index, len(doc_index)):
        if(doc_index[i] not in bad_chars):
            doc_index_new.append(doc_index[i])
    print(doc_index_new)