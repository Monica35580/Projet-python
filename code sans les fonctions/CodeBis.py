import re
import praw
import pickle
import datetime
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from Classes import Document, Author
from Corpus import Corpus
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
from sklearn.metrics.pairwise import cosine_similarity


# =============== RECUPERER LES DOCUMENTS DEPUIS ARXIV ===============
def fetch_arxiv_documents(query_terms, max_results):
    url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'xml')
    entries = soup.find_all('entry')

    documents = []
    for entry in entries:
        title = entry.title.text
        authors = ', '.join([author.text for author in entry.find_all('author')])
        date = entry.published.text
        link = entry.link['href']
        summary = entry.summary.text

        document_text = f"{title} {authors} {date} {summary}"
        documents.append(document_text)
    return documents

# Identification
reddit = praw.Reddit(client_id='IjkA0AvuxykNf-oKFXhhDQ', client_secret='bKxr8svtJScKaYp9FSo7F6tU_KNQUQ', user_agent='monica56580')

# Charger les stop words de nltk
stop_words = set(stopwords.words('english'))

# Requête pour ArXiv
query_terms = ["clustering", "Dirichlet"]
max_results = 100
arxiv_documents = fetch_arxiv_documents(query_terms, max_results)

# =============== NETTOYER TEXTE =============== 
textes = []

for i, document_text in enumerate(arxiv_documents):
    if i % 10 == 0:
        print("ArXiv:", i, "/", max_results)

    # Utiliser nltk pour le nettoyage et l'extraction des mots significatifs
    mots = word_tokenize(document_text)
    mots = [mot.lower() for mot in mots if mot.isalpha() and mot.lower() not in stop_words]

    # Ajouter les mots à l'ensemble
    texte_nettoye = ' '.join(mots)
    textes.append(texte_nettoye)

# =============== OBTENIR MATRICE TF-IDF ===============
vectoriseur = TfidfVectorizer()
matrice_tfidf = vectoriseur.fit_transform(textes)

# Obtenir les noms des caractéristiques
noms_caracteristiques = vectoriseur.get_feature_names_out()

print(matrice_tfidf)
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(list(noms_caracteristiques)))

# =============== TRIER LES RESULTATS PAR PERTINENCE ===============
termes_recherche = ["clustering", "Dirichlet"]
texte_pertinent = []

# Vectoriser les termes de recherche
vecteur_termes_recherche = vectoriseur.transform([" ".join(termes_recherche)])

# Calculer la similarité cosinus entre le vecteur des termes de recherche et chaque document
similarites = cosine_similarity(matrice_tfidf, vecteur_termes_recherche)

# Ajouter la similarité comme colonne dans les résultats
resultats_tries = list(zip(arxiv_documents, similarites))

# Trier les résultats par similarité (du plus au moins similaire)
resultats_tries = sorted(resultats_tries, key=lambda x: x[1], reverse=True)

# Afficher les résultats triés
for document, similarite in resultats_tries:
    print(f"Similarite : {similarite[0]:.4f}")
    print(document)
'''
# =============== TRIER LES RESULTATS PAR DATE =============== marche pas tout a fait
# Créer une liste pour stocker les tuples (document, date)
resultats_date = []

# Parcourir chaque document
for document in arxiv_documents:
    # Supposer que la date est au début du texte (vous devrez ajuster cela selon votre format)
    date_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', document)
    
    if date_match:
        # Extraire la date de publication du document
        date_publication = datetime.datetime.strptime(date_match.group(), "%Y-%m-%d %H:%M:%S")

        # Ajouter le tuple (document, date) à la liste
        resultats_date.append((document, date_publication))
    else:
        # Gérer le cas où la date n'est pas trouvée
        print(f"Avertissement : Pas de date trouvée pour le document {document}")

# Trier les résultats par date de publication (du plus récent au moins récent)
resultats_date = sorted(resultats_date, key=lambda x: x[1], reverse=False)

# Afficher les résultats triés
for document, date_publication in resultats_date:
    print(f"Date de publication : {date_publication.strftime('%Y-%m-%d %H:%M:%S')}")
    print(repr(document))'''

# =============== CREER DOCUMENT ET AUTEUR =============
titre = "ArXiv - Articles populaires"
auteur = "N/A"
date = datetime.datetime.now().strftime("%Y/%m/%d")
url = "N/A"
texte = ' '.join(texte_pertinent)

# Instanciation de la classe Document
doc_classe = Document(titre, auteur, date, url, texte)

# =============== CREATION ET SAUVEGARDE DU CORPUS ===============
corpus = Corpus("Corpus ArXiv")
corpus.add(doc_classe)

# Sauvegarde et chargement du corpus avec pickle
with open("corpus_moteur_recherche.pkl", "wb") as f:
    pickle.dump(corpus, f)

del corpus

with open("corpus_moteur_recherche.pkl", "rb") as f:
    corpus = pickle.load(f)
