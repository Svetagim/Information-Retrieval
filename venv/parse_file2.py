import re

def Parsing(doc_index):
    regex = re.compile('[@_!\'#$\-%,^&*()<>?/\|}{~:\.]')
    index_to_delete = 0
    left_border = doc_index.index(')') + 1
    new_doc_index = []
    for word_index in range(left_border, len(doc_index)):
        new_doc_index.append(doc_index[word_index])
    for word in new_doc_index:
        word = word.lstrip()
        word = word.rstrip()
        word = word.lower()
        if (regex.search(word) != None):
            del new_doc_index[index_to_delete]
        index_to_delete += 1
    print(new_doc_index)
    return new_doc_index

def Sorting(doc_index):
    doc_index.sort()
    print(doc_index)