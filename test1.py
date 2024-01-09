# =============== LISTE DES IMPORTATIONS ===============
import re
import requests
import pickle
import praw
import datetime
import pandas as pd
import urllib, urllib.request
import xmltodict
from bs4 import BeautifulSoup
from Classes import Document, Author
from Corpus import Corpus
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8') # Pour configurer la sortie des articles en UTF-8 Sinon une erreurs dans le terminal car il ne peut pas décoder


# =============== RECUPERER CONTENU ET TRAITEMENT DU DOCUMENT ===============
########### Pour Récupérer Reddit
def obtenir_contenu_web():
    # Identification
    reddit = praw.Reddit(client_id='hOyL_L3Pir_9uU18wGBJkQ', client_secret='wBb7Zld_tKlDb9MDHyApFWZHK74VpA', user_agent='lucilecpp')

    # Requête
    limit = 100
    hot_posts = reddit.subreddit('olympic').hot(limit=limit)

    # Initialisation de listes vides pour récupérer le texte, l'auteur et la date
    docs = []
    auteurs = []
    dates = []

    # Affichage de la récupération en temps réel
    for i, post in enumerate(hot_posts):
        if i % 10 == 0:
            print("Reddit:", i, "/", limit)
        # Si texte on remplace le saut de ligne par vide
        if post.selftext != "":
            docs.append(post.selftext.replace("\n", " "))
            
            # Vérifier si l'auteur existe
            if post.author is not None:
                # Ajout de l'auteur à la liste
                auteurs.append(post.author.name)
            else:
                # Ajout auteur inconnu si on connaît pas l'auteur
                auteurs.append("Auteur inconnu")
            
            # Récupération de la date
            date_utc = datetime.utcfromtimestamp(post.created_utc)

            # Formatage de la date au format année-mois-jour
            date_format = formate_date(date_utc)

            # Ajout de la date formaté à la liste
            dates.append(date_format)

    # Affichage du nombre d'article récupérés
    print(f"Nombre d'articles récupérés: {len(docs)}")
    return docs, auteurs, dates

################### Pour Arxiv
def recuperer_contenu_web():
    # Paramètres
    query_terms = ["olympic", "game"]
    max_results = 100

    # Requête ArXiv
    url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
    data = urllib.request.urlopen(url)

    # Format dict (OrderedDict)
    data = xmltodict.parse(data.read().decode('utf-8'))

    # Initialisation des listes
    docs = []
    auteurs = []
    dates = []

    # Ajout résumés, auteurs et dates à la liste
    for i, entry in enumerate(data["feed"]["entry"]):
        if i % 10 == 0:
            print("ArXiv:", i, "/", max_results)

        ## Extraction des textes
        doc = entry["summary"].replace("\n", "")

        # Ajout du texte à la liste document
        docs.append(doc)

        ## Extraction des auteurs

        # Si author est de type list
        if isinstance(entry["author"], list):
            
            # On ajoute tous les auteurs à liste_auteurs
            liste_auteurs = [auteur["name"] for auteur in entry["author"]]

        # Si author est de type dict
        elif isinstance(entry["author"], dict):

            # On ajoute tous les auteurs à liste_auteurs
            liste_auteurs = [entry["author"]["name"]]
        else:
            # Si pas author n'est ni list ou dict on met auteur inconnu
            liste_auteurs = ["Auteur inconnu"]

        # Ajout des auteurs du document à la liste des auteurs
        auteurs.append(liste_auteurs)

        ##  Extraction de la date

        # Si la variable published est dans les informations récupérées par la requête
        if "published" in entry:
            # On stocke published
            date_1 = entry["published"]

            # On récupère le format
            date_2 = datetime.strptime(date_1, "%Y-%m-%dT%H:%M:%SZ")

            # On ajoute le bon format à la liste
            dates.append(formate_date(date_2))
        else:
            # On ajoute une date inconnue si pas de published pur le texte
            dates.append("Date inconnue")

    # Affichage du nombre de document
    print(f"Nombre d'articles récupérés: {len(docs)}")
    return docs, auteurs, dates
# ==================================================================Fonction pour le traitement du corpus=========================
def nettoyer_texte(texte):
    # Retirer les balises HTML
    #texte_sans_html = BeautifulSoup(texte, 'html.parser').get_text()

    # Imprimer le texte après suppression des balises HTML
    #print("Texte sans HTML :", texte_sans_html)

    # Supprimer les caractères spéciaux et les chiffres
    texte_sans_html = re.sub(r'[^a-zA-Z\s.]+', '', texte)    
    texte_propre = texte_sans_html.lower()
    texte_propre = texte_propre.replace('\n', ' ')

    # Imprimer le texte après suppression des caractères spéciaux et chiffres
    #print("Texte après suppression des caractères spéciaux :", texte_sans_html)
    '''
    # Diviser le texte en mots en utilisant plusieurs délimitations
    mots = re.split(r'\s+|[.,;\'"()]+', texte_propre)
    # Imprimer le texte après suppression des caractères spéciaux et chiffres
    #print("Texte après suppression des caractères spéciaux :", texte_sans_html)

    # Diviser le texte en mots en utilisant plusieurs délimitations
    mots = re.split(r'\s+|[.,;\'"()]+', texte_sans_html)

    # Imprimer les mots après la division du texte
    #print("Mots après division du texte :", mots)

    # Filtrer les mots vides
    mots_filtrés = [mot for mot in mots if mot]

    # Imprimer les mots filtrés
    #print("Mots filtrés :", mots_filtrés)

    # Ajouter les mots à l'ensemble
    vocabulaire_set = set(mots_filtrés)

    # Construire un dictionnaire de vocabulaire avec des fréquences initiales à zéro
    vocabulaire = {mot: 0 for mot in vocabulaire_set}

    for mot in mots_filtrés:
        vocabulaire[mot] += 1'''
    return texte_propre

# Pour avoir la date au bon format
def formate_date(date_utc):

    # Formater la date en gardant seulement le jour, l'année et le mois
    return date_utc.strftime('%Y-%m-%d')

# =============== TRIER LES RESULTATS PAR PERTINENCE ===============
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

def stat(corpus):
    for doc in corpus:
        # nombre de phrases
        print("Nombre de phrases : " + str(len(doc.split("."))))
        print("Nombre de mots : " + str(len(doc.split(" "))))

# =============== CREER DOCUMENT ET AUTEUR =============
# Définition de la fonction creer_document
def creer_document():

     # Création d'une liste pour stocker les instances de la classe Document
    liste_documents = []

    # Itéreration  sur les lignes du df
    for index, ligne in df.iterrows():

        # Créer une instance de la classe Document pour chaque document du df
        document = Document(  
            auteur=ligne['Auteur'],
            date=ligne['Date'],
            texte=ligne['Contenu'],
            origine=ligne['Origine'] 
        )
        
        # Ajoute de l'instance à la classe
        liste_documents.append(document)
    print("Document créé avec succès.")
    return liste_documents


'''def creer_auteur(collection, aut2id, num_auteurs_vus, doc):

    auteurs = {}
    aut2id = {}
    num_auteurs_vus = 0

    if doc.auteur not in aut2id:
        num_auteurs_vus += 1
        auteurs[num_auteurs_vus] = Author(doc.auteur)
        aut2id[doc.auteur] = num_auteurs_vus
    auteurs[aut2id[doc.auteur]].add(doc.texte)'''

# =============== CREATION ET SAUVEGARDE DU CORPUS ===============
def creer_corpus(collection):
    corpus = Corpus("Corpus Web Paris 2024")
    for doc in collection:
        corpus.add(doc)
    return corpus

def sauvegarder_et_charger_corpus(corpus):
    # Sauvegarde du corpus
    with open("corpus_moteur_recherche.pkl", "wb") as f:
        pickle.dump(corpus, f)

    # Lecture du corpus depuis le fichier
    with open("corpus_moteur_recherche.pkl", "rb") as f:
        nouveau_corpus = pickle.load(f)
    return nouveau_corpus

# =============== OBTENIR MATRICE TF-IDF ===============
def obtenir_matrice_tfidf(textes):
    # Imprimer les textes avant la vectorisation
    # print("Textes pour la matrice TF-IDF :")
    #for i, texte in enumerate(textes):
    #    print(f"Document {i} : {texte}")

    # Si le texte est de type
    if isinstance(textes, str):
        # On convertit en liste
        textes = [textes]


    # Utiliser TfidfVectorizer avec un seuil minimum de documents
    vectoriseur = TfidfVectorizer(min_df=1)  # Réglez min_df en fonction de vos besoins
    matrice_tfidf = vectoriseur.fit_transform(textes)
    return matrice_tfidf


# =============== Calculs pour comparer les textes ===============
def comparer_nombres_mots_longueur(texte):
    # Si le texte est vide, renvoyer (0, 0)
    if not texte:
        return 0, 0

    # Diviser le texte en mots en utilisant plusieurs délimitations
    mots = re.split(r'\s+|[.,;\'"()]+', texte)

    # Calculer le nombre de mots
    nombre_mots = len(mots)

    # Calculer la longueur du texte
    longueur_texte = len(texte)
    return nombre_mots, longueur_texte

# Pour compter le nombre de phrases dans un texte
def compter_phrases(texte):

    # Séparation des phrases avec la ponctuation
    phrases = re.split(r'[.!?]', texte)

    # Filtrer les éléments vides
    phrases = [phrase for phrase in phrases if phrase] 

    # Retour de la longueur de la phrase
    return len(phrases)

# Pour compter le nombre de mots dans un texte
def compter_mots(texte):

    # Sépraration des mots à chaque espace
    mots = texte.split()
    return len(mots)

# Pour compter le nombre de caractères dans un texte
def compter_caracteres(texte):
    return len(texte)

# =============== APPELS DES FONCTIONS ===============
# URL de la page web
#url_test = 'https://www.paris2024.org/fr/'

#récupérer le contenu web de Arxiv
contenu_web_arxiv, auteurs_ar, dates_ar = recuperer_contenu_web()

# Récupération de la fonction pour obtenir les articles de Reddit
contenu_web_reddit, auteurs_red, dates_red = obtenir_contenu_web()

# Concaténer les éléments de la liste
#contenu_web_arxiv_str = ' '.join(contenu_web_arxiv)

# Appliquer la fonction nettoyer_texte
#resultat_nettoye = nettoyer_texte(contenu_web_arxiv)

#print(contenu_web_reddit)
#print(contenu_web_arxiv)

#========================================================== Obtenir Dataframe ======================================
def creation_df(contenu, auteurs, dates, nom_var):
    contenu_propre=[]
    # Nettoyer le texte
    for i in contenu:
        # Application de la fonction nettoyer
        resultat_nettoye = nettoyer_texte(i)

        # Ajout du contenu nettoyer 
        contenu_propre.append(resultat_nettoye)

    # Création d'un DataFrame à partir des données récupérées
    df = pd.DataFrame({'Contenu': contenu, 'Auteur': auteurs, 'Date': dates})
    # Ajout d'une variable pour connaître l'origine du texte
    df['Origine'] = nom_var
    return df






#========================================================== Reddit ====================================================
'''contenu_propre=[]
# Nettoyer le texte
for i in contenu_web_reddit:
    # Application de la fonction nettoyer
    resultat_nettoye = nettoyer_texte(i)

    # Ajout du contenu nettoyer 
    contenu_propre.append(resultat_nettoye)

# Comparer le nombre de mots et la longueur du document
resultat_nettoye_str = ' '.join(contenu_web_reddit)
nombre_mots, longueur_texte = comparer_nombres_mots_longueur(resultat_nettoye_str)
print(f"Nombre de mots : {nombre_mots}")
print(f"Longueur du texte : {longueur_texte} caracteres")

# Récupérer le texte pertinent
termes_recherche = ["olympic", "game"]
#texte_pertinent = extraire_texte_pertinent(contenu_propre, termes_recherche)

# Affichage des résultats
#print("Texte pertinent sans duplication:", texte_pertinent)

# Traiter le texte pertinent extrait
longue_chaine_de_caracteres = traiter_texte_pertinent(contenu_propre)
#print(stat(contenu_propre))

# Utilisation de la fonction avec le texte pertinent traité
matrice_tfidf = obtenir_matrice_tfidf(contenu_propre)
#print(matrice_tfidf)

# Création d'un DataFrame à partir des données récupérées
df = pd.DataFrame({'Contenu': contenu_web_reddit, 'Auteur': auteurs_red, 'Date': dates_red})


# Ajout de colonne pour le df pour compter les phrases, les mots et les caractères
df['Origine'] = 'Reddit'
#df['Nombre de Phrases'] = df['Contenu'].apply(compter_phrases)
#df['Nombre de Mots'] = df['Contenu'].apply(compter_mots)
#df['Nombre de Caracteres'] = df['Contenu'].apply(compter_caracteres)


# Afficher le DataFrame
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
#print(df)

#Convertir le df en csv
#df.to_csv('corpus.csv', index=False, sep='\t')
'''


########################################################### Arxiv #########################################################

# Création du corpus pour Arxiv
arxiv=creation_df(contenu_web_arxiv, auteurs_ar, dates_ar, 'Arxiv')

# Création du corpus pour Reddit
reddit=creation_df(contenu_web_reddit, auteurs_red, dates_red, 'Reddit')

# Combiner les deux dataframes
df = pd.concat([arxiv, reddit], ignore_index=True)

# Ajout ID unique par texte
df.insert(loc=0, column="id", value=df.index)

# Calcul de différents indicateurs pour les textes
df['Nombre_phrases'] = df['Contenu'].apply(compter_phrases)
df['Nombre_mots'] = df['Contenu'].apply(compter_mots)
df['Nombre_caracteres'] = df['Contenu'].apply(compter_caracteres)
df['Comparer_mot']=df['Contenu'].apply(comparer_nombres_mots_longueur)
df['Matrice tf-idf']=df['Contenu'].apply(obtenir_matrice_tfidf)


# Afficher le DataFrame combiné
#pd.set_option('display.max_columns', None)
#pd.set_option('display.expand_frame_repr', False)
print(df)

## Calcul matrice tf-idf
# Extraction de la colonne avec les textes
textes_colonne = df['Contenu']

# Application de la fonction
matrice_tfidf_resultat = obtenir_matrice_tfidf(textes_colonne)

# Affichage des résultats
print(matrice_tfidf_resultat)

# Convertir le df en csv
df.to_csv('corpus.csv', index=False, sep=';')

# Inititalisation des documents du corpus
corpus_liste=creer_document()

# Affichage des documents de la classe
#for document in corpus_liste:
#    print(Document.__repr__(document))




'''# Création d'un corpus à partir de la liste de documents
corpus = creer_corpus(corpus_liste)

# Afficher les documents dans le corpus
corpus.show(n_docs=5, tri="abc")

# Sauvegarder et charger le corpus
nouveau_corpus = sauvegarder_et_charger_corpus(corpus)'''











'''contenu_propre_ar=[]
#nettoyer le texte
for i in contenu_web_arxiv:
    resultat_nettoye = nettoyer_texte(i)
    contenu_propre_ar.append(resultat_nettoye)


# Comparer le nombre de mots et la longueur du document
resultat_nettoye_str = ' '.join(contenu_web_arxiv)
nombre_mots, longueur_texte = comparer_nombres_mots_longueur(resultat_nettoye_str)
print(f"Nombre de mots : {nombre_mots}")
print(f"Longueur du texte : {longueur_texte} caracteres")

# Récupérer le texte pertinent
termes_recherche = ["olympic", "game"]
texte_pertinent_ar = extraire_texte_pertinent(contenu_propre_ar, termes_recherche)

# Affichage des résultats
#print("Texte pertinent sans duplication:", texte_pertinent)

# Traiter le texte pertinent extrait
longue_chaine_de_caracteres = traiter_texte_pertinent(texte_pertinent_ar)

# Utilisation de la fonction avec le texte pertinent traité
matrice_tfidf = obtenir_matrice_tfidf(texte_pertinent_ar)
print(matrice_tfidf)

# créer un document
liste_documents = []

# Ajout du document à la liste
liste_documents.append(Document())'''

