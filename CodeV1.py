# =============== LISTE DES IMPORTATIONS ===============
import datetime
import pandas as pd
import pickle
import praw
import re
import requests
import urllib, urllib.request
import xmltodict
from bs4 import BeautifulSoup
from Classes import Document, Author
from Corpus import Corpus
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =============== RECUPERER CONTENU ET TRAITEMENT DU DOCUMENT ===============
def obtenir_contenu_web():
    # Identification
    reddit = praw.Reddit(client_id='hOyL_L3Pir_9uU18wGBJkQ', client_secret='wBb7Zld_tKlDb9MDHyApFWZHK74VpA', user_agent='lucilecpp')

    # Requête
    limit = 100
    hot_posts = reddit.subreddit('all').hot(limit=limit)

    # Récupération du texte
    docs = []
    for i, post in enumerate(hot_posts):
        if i % 10 == 0:
            print("Reddit:", i, "/", limit)

        if post.selftext != "":
            docs.append(post.selftext.replace("\n", " "))
    return docs

def recuperer_contenu_web():
    # Paramètres
    query_terms = ["olympic"]
    max_results = 100

    # Requête ArXiv
    url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
    data = urllib.request.urlopen(url)

    # Format dict (OrderedDict)
    data = xmltodict.parse(data.read().decode('utf-8'))

    # Initialisation des listes
    docs = []
    docs_bruts = []

    # Ajout résumés à la liste
    for i, entry in enumerate(data["feed"]["entry"]):
        if i % 10 == 0:
            print("ArXiv:", i, "/", max_results)

        docs.append(entry["summary"].replace("\n", ""))
        docs_bruts.append(("ArXiv", entry))
    return docs, docs_bruts

def nettoyer_texte(texte):
    # Supprimer les caractères spéciaux et les chiffres
    texte_sans_html = re.sub(r'[^a-zA-Z\s]', '', texte)
    texte_propre = texte_sans_html.lower()
    texte_propre = texte_propre.replace('\n', ' ')
    return texte_propre

# =============== EXTRAIRE ET EXTRAIRE TEXTE PERTINENT ===============
def extraire_texte_pertinent(contenu_web, termes_recherche):
    texte_pertinent = []

    if isinstance(contenu_web, list):
        print("liste")
        for element in contenu_web:
            if isinstance(element, tuple):
                print("tuple")
                # Si l'élément est un tuple, traiter chaque élément du tuple
                for sub_element in element:
                    if isinstance(sub_element, str):
                        print("str")
                        texte_nettoye = nettoyer_texte(sub_element)
                        if texte_nettoye and texte_nettoye not in texte_pertinent:
                            texte_pertinent.append(texte_nettoye) 
            elif isinstance(element, str):
                texte_nettoye = nettoyer_texte(element)
                if texte_nettoye and texte_nettoye not in texte_pertinent:
                    texte_pertinent.append(texte_nettoye)
    else :
        # Traitement si contenu_web est une chaîne de caractères (str)
        texte_nettoye = nettoyer_texte(contenu_web)
        if texte_nettoye and texte_nettoye not in texte_pertinent:
            texte_pertinent.append(texte_nettoye)
            print("ajoute str !!!!!")
        else:
            print("déjà dans la liste str")
    return texte_pertinent

def traiter_texte_pertinent(texte_pertinent):
    print(f"# docs avec doublons : {len(texte_pertinent)}")
    # Convertir chaque ensemble en chaîne pour éviter l'erreur "unhashable type: 'set'"
    texte_pertinent_str = [' '.join(doc) for doc in texte_pertinent]

    # Supprimer les doublons tout en préservant l'ordre d'origine
    texte_pertinent_sans_doublons_str = list(dict.fromkeys(texte_pertinent_str))
    print(f"# docs sans doublons : {len(texte_pertinent_sans_doublons_str)}")

    # Convertir à nouveau les chaînes en ensembles si nécessaire
    texte_pertinent_sans_doublons = [set(doc.split()) for doc in texte_pertinent_sans_doublons_str]

    for i, doc in enumerate(texte_pertinent_sans_doublons):
        print(f"Document {i}\t# caracteres : {len(doc)}\t# mots : {len(doc)}\t# phrases : {len(doc)}")
        if len(doc) < 100:
            texte_pertinent_sans_doublons.remove(doc)
    longue_chaine_de_caracteres = " ".join(texte_pertinent_sans_doublons_str)
    return longue_chaine_de_caracteres

# =============== CREER DOCUMENT ET AUTEUR =============
def creer_document(collection_documents):
    # Récupération du contenu web et de l'URL depuis recuperer_contenu_web
    contenu_web_arxiv, contenu_web_reddit = recuperer_contenu_web()

    # Traitement du texte pertinent
    termes_recherche = ["olympic"]
    texte_pertinent = extraire_texte_pertinent(contenu_web_arxiv, termes_recherche)

    # Ajout du texte pertinent à la collection de documents
    document = Document(
        titre="",  
        auteur="",
        date="",
        url="",  
        texte="",  
        texte_pertinent=texte_pertinent 
    )
    collection_documents.append(document)
    print("Document cree avec succes.")

def creer_auteur(collection, aut2id, num_auteurs_vus, doc):
    auteurs = {}

    if doc.auteur not in aut2id:
        num_auteurs_vus += 1
        auteurs[num_auteurs_vus] = Author(doc.auteur)
        aut2id[doc.auteur] = num_auteurs_vus
    auteurs[aut2id[doc.auteur]].add(doc.texte)
    return auteurs, aut2id, num_auteurs_vus

# =============== CREATION ET SAUVEGARDE DU CORPUS ===============
def creer_corpus(collection_documents):
    # Créer une instance de Corpus
    corpus = Corpus("Corpus 2024")

    # Ajouter chaque document à la collection dans le corpus
    for document in collection_documents:
        corpus.add(document)
    return corpus

def sauvegarder_et_charger_corpus(corpus):
    # Sauvegarde du corpus
    with open("corpus_moteur_recherche.pkl", "wb") as f:
        pickle.dump(corpus, f)

    # Lecture du corpus depuis le fichier
    with open("corpus_moteur_recherche.pkl", "rb") as f:
        nouveau_corpus = pickle.load(f)
    return nouveau_corpus

# =============== APPELS DES FONCTIONS ===============

# Récupérer le contenu web
contenu_web_arxiv, contenu_web_reddit = recuperer_contenu_web()
contenu_web_arxiv_str = ' '.join(contenu_web_arxiv)
#print(contenu_web_reddit)
#print(contenu_web_arxiv)

# Nettoyer le texte
contenu_propre=[]
for i in contenu_web_arxiv:
    resultat_nettoye = nettoyer_texte(i)
    contenu_propre.append(resultat_nettoye)
#print(f"Texte_nettoye :", resultat_nettoye)
for i in contenu_propre:
    print("contenu :",type(i))

# Récupérer le texte pertinent
termes_recherche = ["olympic"]
texte_pertinent = extraire_texte_pertinent(contenu_propre, termes_recherche)
#print("Texte pertinent sans duplication:", texte_pertinent)

# Traiter le texte pertinent extrait
longue_chaine_de_caracteres = traiter_texte_pertinent(texte_pertinent)

# Creer un document
collection_documents = []
creer_document(collection_documents)

# Creer un auteur
aut2id = {}
num_auteurs_vus = 0

for doc in collection_documents:
    auteurs, aut2id, num_auteurs_vus = creer_auteur(collection_documents, aut2id, num_auteurs_vus, doc)
if auteurs:
    print("Auteurs crees avec succes.")
else:
    print("Aucun auteur créé.")

# Creer un corpus
corpus_cree = creer_corpus(collection_documents)
print(corpus_cree)

# Sauvegarder le corpus
mon_corpus = Corpus("Mon_corpus")
sauvegarder_et_charger_corpus(mon_corpus)
corpus_charge = sauvegarder_et_charger_corpus(mon_corpus)
