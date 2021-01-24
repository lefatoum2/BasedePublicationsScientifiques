import pymongo
from pymongo import MongoClient
import json
import tkinter as tk

client = MongoClient('mongodb://localhost:27017/')
db = client["DBLP"]
collection = db["publis"]


def onOpen(self):
    ftypes = [('Python files', '*.py'), ('All files', '*')]
    dlg = tk.FileDialog.Open(self, filetypes=ftypes)
    fl = dlg.show()

    if fl != '':
        text = self.readFile(fl)
        self.txt.insert(END, text)


def readFile(self, filename):
    f = open(filename, "r")
    text = f.read()
    return text


def test1():
    x = collection.aggregate([{"$unwind": "$authors"}])
    for i in x:
        print(i)


# Importer .json dans la base de données
def opendocjson():
    list_dblp = list(
        open('datas/dblp.json', 'r'))

    percent_count = 0
    absolute_count = 0
    error_count = 0

    for line in list_dblp:
        try:
            collection.insert_one(json.loads(line))
        except:
            error_count += 1
            print(error_count, "error(s)")
            pass
        absolute_count += 1
    if int((absolute_count / len(list_dblp)) * 100) > percent_count:
        percent_count += 1
        print(percent_count, "%")

    print("done")


# 2) Lister tous les livres (type “Book”) :
def all_book_type():
    liste_livres = collection.find({"type": "Book"})
    for i in liste_livres:
        print(i)
        print()


# 3) Lister les livres depuis 2014 :
def all_book_2014():
    liste_livres = collection.find({"year": {"$gte": 2014}})
    for i in liste_livres:
        print(i)
        print()


# Compter le nombre de documents
def all_book():
    return collection.count_documents({})


# Liste des publications de Toru Ishida
def all_publis_ishida():
    result = collection.find({"authors": "Toru Ishida"})
    for r in result:
        print(r)


# Liste des auteurs distincts
def all_autors():
    result = collection.distinct("authors")
    for r in result:
        print(r)


# Trier les publications de Toru Ishida par titre de livre
def all_publis_title_ishida():
    result = collection.find({"$query": {"authors": "Toru Ishida"}, "$orderby": {"title": 1}})
    for r in result:
        print(r)


# Compter le nombre de publications par auteur et trier le résultat par ordre croissant
def authors_publis_resultat():
    result = collection.find({"$query": {}, "$orderby": {"title": 1}}).count()


# Compter le nombre de  publication de Toru Ishida
def numbers_publis_ishida():
    resultat = db.count_documents({"authors": "Toru Ishida"})
    print("Toru Ishida a fait", resultat, "publications")


# Compter le nombre de publications depuis 2011 et par type
def numbers_publis_2011():
    compteuranneetype = db.find({"year": {"$gte": 2011}})
    liste_types = compteuranneetype.distinct("type")

    for type in liste_types:
        print("Depuis 2011,", db.count_documents({"type": type}), type, "ont été publiées")


if __name__ == '__main__':
    test1()
