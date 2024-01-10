import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import os

def obtenir_matrice_tfidf(textes):
    # Si le texte est de type
    if isinstance(textes, str):
        # On convertit en liste
        textes = [textes]


    # Utiliser TfidfVectorizer avec un seuil minimum de documents
    vectoriseur = TfidfVectorizer(min_df=1)  # Réglez min_df en fonction de vos besoins
    matrice_tfidf = vectoriseur.fit_transform(textes)
    return matrice_tfidf

def nettoyer_texte(texte):

    # Supprimer les caractères spéciaux
    texte_sans_html = re.sub(r'[^a-zA-Z\s.]+', '', texte) 

    # Passage du texte en minuscule   
    texte_propre = texte_sans_html.lower()

    # Remplacement des sauts de lignes par du vide
    texte_propre = texte_propre.replace('\n', ' ')    

    return texte_propre

## Ouverture du csv en df

chemin_fichier_csv = 'corpus.csv' #  A changer si ça fonctionne pas
# Vérification que le csv existe bien 
if os.path.exists(chemin_fichier_csv):

# Pour obtenir le corpus en df sans interroger l'API
    df = pd.read_csv(chemin_fichier_csv, delimiter=';')
else : 
    chemin_fichier_csv='Projet-python-master/corpus.csv' #  A changer si ça fonctionne pas
    if os.path.exists(chemin_fichier_csv):

        # Pour obtenir le corpus en df sans interroger l'API
        df = pd.read_csv(chemin_fichier_csv, delimiter=';')
    else : 
        print ("Le fichier .csv n'a pas été trouvé et sera crée ici : ", {os.getcwd()})



