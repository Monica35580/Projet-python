# =============== LISTE DES IMPORTATIONS ===============
import requests
import pickle
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from Classes import Document
from Classes import Author
from Corpus import Corpus
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


# =============== RECUPERER CONTENU ET TRAITEMENT DU DOCUMENT ===============
def obtenir_contenu_web(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération du contenu web : {e}")
        return None

def recuperer_contenu_web(url):
    contenu_web = obtenir_contenu_web(url)

    # Vérification si le contenu a été récupéré avec succès
    if contenu_web:
        print("Le contenu a ete recupere.")
    else:
        print("Le contenu n'a pas ete recupere.")
        exit()

    return contenu_web

def extraire_texte_pertinent(contenu_web, termes_recherche):
    soup = BeautifulSoup(contenu_web, 'html.parser', from_encoding='utf-8')

    texte_pertinent = []
    for terme in termes_recherche:
        elements = soup.find_all(lambda tag: tag.name and terme in tag.get_text().lower())
        for element in elements:
            texte_pertinent.append(element.get_text().strip())

    return texte_pertinent

def traiter_texte_pertinent(texte_pertinent):
    print(f"# docs avec doublons : {len(texte_pertinent)}")
    texte_pertinent = list(set(texte_pertinent))
    print(f"# docs sans doublons : {len(texte_pertinent)}")

    for i, doc in enumerate(texte_pertinent):
        print(f"Document {i}\t# caracteres : {len(doc)}\t# mots : {len(doc.split(' '))}\t# phrases : {len(doc.split('.'))}")
        if len(doc) < 100:
            texte_pertinent.remove(doc)

    longue_chaine_de_caracteres = " ".join(texte_pertinent)

    return longue_chaine_de_caracteres

# =============== CREER DOCUMENT ET AUTEUR =============
def creer_document(collection, url, longue_chaine_de_caracteres):
    titre = "Paris 2024 - Page Web"
    auteur = "N/A"
    date = datetime.datetime.now().strftime("%Y/%m/%d")
    url = url
    texte = longue_chaine_de_caracteres

    # Instanciation de la classe Document
    doc_classe = Document(titre, auteur, date, url, texte)
    collection.append(doc_classe)

def creer_auteur(collection, aut2id, num_auteurs_vus, doc):
    if doc.auteur not in aut2id:
        num_auteurs_vus += 1
        auteurs[num_auteurs_vus] = Author(doc.auteur)
        aut2id[doc.auteur] = num_auteurs_vus

    auteurs[aut2id[doc.auteur]].add(doc.texte)

# =============== CREATION ET SAUVEGARDE DU CORPUS ===============
def creer_corpus(collection):
    corpus = Corpus("Corpus Web Paris 2024")
    for doc in collection:
        corpus.add(doc)
    return corpus

def sauvegarder_et_charger_corpus(corpus):
    # Ouverture d'un fichier, puis écriture avec pickle
    with open("corpus_moteur_recherche.pkl", "wb") as f:
        pickle.dump(corpus, f)

    # Suppression de la variable "corpus"
    del corpus

    # Ouverture du fichier, puis lecture avec pickle
    with open("corpus_moteur_recherche.pkl", "rb") as f:
        corpus = pickle.load(f)
    return corpus

# =============== OBTENIR MATRICE TF-IDF ===============
def obtenir_matrice_tfidf(corpus):
    # Vérifier si l'attribut 'id2doc' existe dans l'objet Corpus
    if not hasattr(corpus, 'id2doc'):
        print("L'objet Corpus ne contient pas d'attribut 'id2doc'.")
        return None

    # Extraire les textes des documents dans le corpus
    textes = [doc.texte for doc in corpus.id2doc.values()]

    # Utiliser TfidfVectorizer pour obtenir la matrice TF-IDF
    vectoriseur = TfidfVectorizer()
    matrice_tfidf = vectoriseur.fit_transform(textes)

    return matrice_tfidf, vectoriseur.get_feature_names_out()

# =============== OBTENIR MATRICE DE FREQUENCE DES MOTS ===============
def frequence_mots(corpus):
    # Vérifier si l'attribut 'id2doc' existe dans l'objet Corpus
    if not hasattr(corpus, 'id2doc'):
        print("L'objet Corpus ne contient pas d'attribut 'id2doc'.")
        return None

    # Extraire les textes des documents dans le corpus
    textes = [doc.texte for doc in corpus.id2doc.values()]

    # Utiliser CountVectorizer pour obtenir la matrice de fréquence des mots
    vectoriseur = CountVectorizer()
    matrice_frequence_mots = vectoriseur.fit_transform(textes)

    return matrice_frequence_mots, vectoriseur.get_feature_names_out()

# =============== APPELS DES FONCTIONS ===============
# URL de la page web
url_test = 'https://www.paris2024.org/fr/'

#récupérer le contenu web
contenu_web = recuperer_contenu_web(url_test)

# extraire le texte pertinent
termes_recherche = ["jeux", "olympique"]
texte_pertinent = extraire_texte_pertinent(contenu_web, termes_recherche)

# traiter le texte pertinent extrait
longue_chaine_de_caracteres = traiter_texte_pertinent(texte_pertinent)

# créer un document
collection_documents = []
creer_document(collection_documents, url_test, longue_chaine_de_caracteres)

# créer un auteur
auteurs = {}
aut2id = {}
num_auteurs_vus = 0
creer_auteur(collection_documents, aut2id, num_auteurs_vus, collection_documents[0])

# créer un corpus
corpus_cree = creer_corpus(collection_documents)

# sauvegarder et charger un corpus avec pickle
corpus_sauvegarde_charge = sauvegarder_et_charger_corpus(corpus_cree)

# obtenir la matrice TF-IDF
matrice_tfidf, noms_caracteristiques = obtenir_matrice_tfidf(corpus_sauvegarde_charge)

print(matrice_tfidf)
print(noms_caracteristiques)

# obtenir la matrice de fréquence des mots
matrice_frequence_mots, noms_mots = frequence_mots(corpus_sauvegarde_charge)

# Créer un DataFrame pour afficher la matrice de fréquence des mots
df_frequence_mots = pd.DataFrame(matrice_frequence_mots.toarray(), columns=noms_mots)
print(df_frequence_mots)


