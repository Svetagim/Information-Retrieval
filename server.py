import bs4
from flask import Flask, render_template, request, redirect
import retrieve
import parse_file
import admin_panel
import main
import files_utils
import nltk

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index.html')
@app.route('/index.html')
def search():
    data = request.args.get('search')
    if data == "":
        return render_template('index.html')
    indexCol = parse_file.connectToDB("indexCollection_new")
    if(indexCol.find().count() > 0):
        col = retrieve.showCollection("indexCollection_new")
        words = retrieve.findWords(data, col)
        docs = retrieve.query(words, len(words))
        col = retrieve.showCollection("docs")
        documents = retrieve.showDocs(docs, col)
        if documents == "":
            return render_template('index.html')
        with open("templates/index.html") as inf:
            txt = inf.read()
            soup = bs4.BeautifulSoup(txt, features="html.parser")
        for document in documents:
            #PASS the words to mark them
            #data2 = retrieve.findWordsToQuery(data)
            #print(data2[0])
            #END PASS words
            new_link = soup.new_tag("a", target="_blank", href="/documents/{0}".format(document[0]))
            soup.section.append(new_link)

            p = soup.new_tag("p")
            p['class'] = "meta"
            p.string = document[0] + " / " + document[1] + " / " + document[2]
            new_link.append(p)

            div = soup.new_tag("div")
            div['class'] = "clear"
            soup.section.append(div)


        return str(soup)
    else:
        return render_template('index.html')


@app.route('/documents/<name>')
def displayDoc(name):
    text = []
    data = ""
    with open("documents/{}.txt".format(name)) as fp:
        line = fp.readline()
        while line:
            data += line
            text.append(line)
            line = fp.readline()

    with open("templates/song.html") as inf:
        template = inf.read()
        soup = bs4.BeautifulSoup(template, features="html.parser")
        p = soup.new_tag("p")
        p['class'] = "res"
        body = soup.body
        h1 = soup.new_tag("h1")
        h1['class'] = "res"
        body.append(h1)
        h2 = soup.new_tag("h2")
        h2['class'] = "res"
        body.append(h2)
        body.append(p)
        i = 0
        for line in text:
            if i == 0:
                body.h1.append(line)
            elif i == 1:
                body.h2.append(line)
            else:
                body.p.append(line)
                body.p.append(soup.new_tag("br"))
            i += 1
    return str(soup)


@app.route('/admin.html')
def admin():
    aFiles = admin_panel.WaitingFiles()
    rFiles = admin_panel.retrievedFiles()
    iFiles = admin_panel.ignoredFiles()
    with open("templates/admin.html") as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt, features="html.parser")
        new_link = soup.new_tag("h3")
        new_link['class'] = "header"
        new_link.string = "Awaiting Files"
        soup.section.append(new_link)
    for file in aFiles:
        new_link = soup.new_tag("a", href="admin.html/{}/wait".format(file))
        new_link['class'] = "awaiting"
        new_link['id'] = "awaiting_documents/{}".format(file)
        new_link.string = file
        soup.section.append(new_link)
        new_link = soup.new_tag("p")
        new_link['class'] = "awaiting"
        new_link.string = "|"
        soup.section.append(new_link)
    new_link = soup.new_tag("a", href="admin.html/ret/n")
    new_link['class'] = "retrieve"
    new_link.string = "RETRIEVE ALL"
    soup.section.append(new_link)
    new_link = soup.new_tag("div")
    new_link['class'] = "clear"
    soup.section.append(new_link)
    new_link = soup.new_tag("h3")
    new_link['class'] = "header"
    new_link.string = "Retrieved Files"
    soup.section.append(new_link)
    for file in rFiles:
        new_link = soup.new_tag("a", href="admin.html/{}/ignore".format(file))
        new_link['class'] = "awaiting"
        new_link['id'] = "documents/{}".format(file)
        new_link.string = file
        soup.section.append(new_link)
        new_link = soup.new_tag("p")
        new_link['class'] = "awaiting"
        new_link.string = "|"
        soup.section.append(new_link)
    new_link = soup.new_tag("a", href="admin.html/rem/n")
    new_link['class'] = "retrieve"
    new_link.string = "REMOVE ALL"
    soup.section.append(new_link)
    new_link = soup.new_tag("div")
    new_link['class'] = "clear"
    soup.section.append(new_link)
    new_link = soup.new_tag("h3")
    new_link['class'] = "header"
    new_link.string = "Ignored Files"
    soup.section.append(new_link)
    for file in iFiles:
        new_link = soup.new_tag("a", href="admin.html/{}/unignore".format(file))
        new_link['class'] = "awaiting"
        new_link['id'] = "documents/{}".format(file)
        new_link.string = file
        soup.section.append(new_link)
        new_link = soup.new_tag("p")
        new_link['class'] = "awaiting"
        new_link.string = "|"
        soup.section.append(new_link)
    new_link = soup.new_tag("div")
    new_link['class'] = "clear"
    soup.section.append(new_link)

    return str(soup)


@app.route('/admin.html/<param>/<state>')
def adminParam(param, state):
    if param == "rem":
        main.Clear_Old_Record_in_DB()
        files_utils.RemoveAllDocs()
    elif param == "ret":
        main.Clear_Old_Record_in_DB()
        files_utils.RemoveAllDocs()
        main.Insert_New_Docs()
    else:
        if state == "ignore":
            main.log("ignoring: " + param)
            main.Ignore_Document(param)
            print("done")
        elif state == "unignore":
            main.log("Unignoring: " + param)
            main.UnIgnore_Document(param)
            print("done")
        else:
            print("wait")



    return redirect("/admin.html")


@app.route('/help.html')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
