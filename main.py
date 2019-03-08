from nltk.corpus import stopwords
import parse_file
import reading_filles

if __name__ == '__main__':
    reading_filles.Pull_Document()
    DocCol = parse_file.connectToDB()
    doc_id = parse_file.findMaxDocID(DocCol)  # new id for the new doc
    #print(stopwords.words('english'))
    exit(0)