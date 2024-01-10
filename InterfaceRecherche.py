import ctypes
import CodeV3 as t
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from sklearn.metrics.pairwise import cosine_similarity


# Fonction de recherche
def recherche():

    # Obtenir la requête de l'utilisateur
    requete_utilisateur = champ_recherche.get()
    verif=requete_vide(requete_utilisateur)

    if verif==True:

        # Nettoyage
        requete_traitee = t.nettoyer_texte(requete_utilisateur)

        # Concatenation tous les textes du df et on transforme le contenu en liste pour passer dans matrice tdidf (De la ligne 21 à 31 le code provient de chatGPT)
        textes_concatenes = [requete_traitee] + t.df['Contenu'].tolist()

        # Utilisation TF-IDF pour la représentation vectorielle
        matrice_tfidf_resultat = t.obtenir_matrice_tfidf(textes_concatenes)

        # Calcul de la similarité pour les articles
        similarites = cosine_similarity(matrice_tfidf_resultat)[0, 1:]

         #Trie des résultats par similarité
        resultats_tries = sorted(zip(t.df['Contenu'], t.df['Auteur'],t.df['Date'], t.df['Origine'], t.df['Titre'],similarites), key=lambda x: x[5], reverse=True)
        
        # Récupération du nombre de résultats entre par l'utilisateur
        nombre_resultats = verif_nb(champ_nombre_resultats.get())

        if nombre_resultats != False:
            top = resultats_tries[:nombre_resultats]
        
            # Afficher le menu déroulant de tri
            menu_tri_results.grid(row=2, column=503)
            bouton_tri_results.grid(row=2, column=504)

            ## Afficher les résultats triés
            # Passage de la zone de texte en écriture
            resultat_texte.config(state=tk.NORMAL)

            # Efface le texte dans le zone d'affichage
            resultat_texte.delete(1.0, tk.END)

            # Ecriture du message
            resultat_texte.insert(tk.END, "Résultats de la recherche :\n")

            # On affiche tous les éléments pour chaque article
            for i, (resultat, auteur, date, origine, titre, similarites) in enumerate(top):
                resultat_texte.insert(tk.END, f"{i + 1}.\n")
                resultat_texte.insert(tk.END, f"Auteur : {auteur}\n")
                resultat_texte.insert(tk.END, f"Date : {date}\n")
                resultat_texte.insert(tk.END, f"Origine : {origine}\n\n")
                resultat_texte.insert(tk.END, f"Titre : {titre}\n\n")
                resultat_texte.insert(tk.END, f"{resultat}\n\n")

            # Passage de la zone de recherche en lecture seul
            resultat_texte.config(state=tk.DISABLED)
    else :
        print("requête vide")

# Fonction pour vérifer que le requête utilisateur n'est pas vide
def requete_vide(requete):

    # Déclaration d'un indice
    indice=False
    if requete=="":
        # Affichage d'un message si la requête est vide
        messagebox.showerror("Requête vide","Veuillez entrer une information avant de lancer la recherche")
        indice=False
    else : 
        # Passage à True si la requête n'est pas vide
        indice=True

    # Retour de l'indice
    return indice


def trier_resultats(critere):
    # Fonction de tri des résultats à implémenter
    # Ici, nous affichons simplement un exemple de texte trié dans la zone de résultats
    resultat_texte.config(state=tk.NORMAL)
    resultat_texte.delete(1.0, tk.END)
    resultat_texte.insert(tk.END, f"Résultats triés par {critere} :\n")
    resultat_texte.insert(tk.END, "1. Résultat A\n")
    resultat_texte.insert(tk.END, "2. Résultat B\n")
    resultat_texte.insert(tk.END, "3. Résultat C\n")
    resultat_texte.config(state=tk.DISABLED)

def verif_nb(nb):
    # Création d'indice pour connaître statut de la fonction
    indice = False

    # Vérification de si nb est un nombre
    if nb.isdigit():

        # Convertion de nb_res en int
        nb_res = int(nb)

        # Création d'un message pour gérer les erreurs
        message="Veuillez entrer un nombre entre 0 et "

        # Vérification que le nb_res soit bien entre 0 et le nb d'articles
        if  nb_res > 0 and nb_res <= len(t.df):
            return nb_res
        else:
            # Sinon affiche le message concaténer avec le nb d'articles
            messagebox.showerror("Erreur", message + str(len(t.df)))
            return indice
    else:
        # Affiche message entrer un nombre
        messagebox.showerror("Erreur", "Veuillez entrer un nombre entier")
        return indice

def taille_ecran(fenetre):

    taille = ctypes.windll.user32
    largeur = taille.GetSystemMetrics(0)
    hauteur = taille.GetSystemMetrics(1)
    return fenetre.geometry(f"{largeur}x{hauteur}")

# Création de la fenêtre principale
fenetre = tk.Tk()

# Titre de la fenêtre
fenetre.title("Moteur de recherche")

# Définir la taille de la fenêtre
taille_ecran(fenetre)

# Création du champ de recherche
champ_recherche = ttk.Entry(fenetre, width=50)
champ_recherche.grid(row=0, column=500, padx=10, pady=10)

# Bouton de recherche
bouton_recherche = ttk.Button(fenetre, text="Rechercher", command=recherche) # Lancement de la fonction recherche
bouton_recherche.grid(row=0, column=504, padx=10, pady=10)

# Texte informatif
info_texte = ttk.Label(fenetre, text="Entrez votre requête de recherche ci-dessus : \nPour de meilleur résultat, il est conseillé que la requête soit en anglais")
info_texte.grid(row=1, column=500, columnspan=2, pady=(0, 10))

# Résultats de la recherche (zone de texte déroulante)
resultat_texte = scrolledtext.ScrolledText(fenetre, wrap=tk.WORD, width=80, height=30)
resultat_texte.grid(row=2, column=500, columnspan=2, padx=10, pady=10)
resultat_texte.config(state=tk.DISABLED)  # Pour rendre la zone de texte en lecture seule

# Menu déroulant de tri 
critere_tri_var = tk.StringVar(fenetre)
critere_tri_var.set("Pertinence")  # Valeur par défaut
menu_tri_results = tk.OptionMenu(fenetre, critere_tri_var, "Pertinence", "Date", "Auteur", "Origine")
menu_tri_results.grid_remove()  # Pour cacher le menu déroulant 

# Bouton de tri des résultats
bouton_tri_results = ttk.Button(fenetre, text="Trier les résultats", command=lambda: trier_resultats(critere_tri_var.get()))
bouton_tri_results.grid(row=3, column=500, columnspan=2, pady=(10, 0))
bouton_tri_results.grid_remove()  # Pour cacher le bouton 

# Champ de saisie pour le nombre de résultats
info_texte_nb = ttk.Label(fenetre, text="Entrez le nombre de résultats que vous voulez avoir : ")
info_texte_nb.grid(row=0, column=501, columnspan=2, pady=(0, 10))
champ_nombre_resultats = ttk.Entry(fenetre, width=5)
champ_nombre_resultats.grid(row=0, column=503, padx=10, pady=10)
champ_nombre_resultats.insert(0, "10")  # Valeur par défaut

# Exécution de la boucle principale
fenetre.mainloop()