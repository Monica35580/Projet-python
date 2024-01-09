import tkinter as tk
from tkinter import ttk, scrolledtext
import test1 as t
from sklearn.metrics.pairwise import cosine_similarity


# Fonction de recherche
def recherche():
    # Obtenir la requête de l'utilisateur
    requete_utilisateur = champ_recherche.get()

    # Prétraitement de la requête
    requete_traitee = t.nettoyer_texte(requete_utilisateur)

    # Concaténer tous les textes du DataFrame (Reddit + ArXiv)
    textes_concatenes = [requete_traitee] + t.df['Contenu'].tolist()

    # Utiliser TF-IDF pour la représentation vectorielle
    matrice_tfidf_resultat = t.obtenir_matrice_tfidf(textes_concatenes)

    # Calcul de la similarité avec chaque texte du corpus
    similarites = cosine_similarity(matrice_tfidf_resultat)[0, 1:]

    # Trier les résultats par similarité
    resultats_tries = sorted(zip(t.df['Contenu'], similarites), key=lambda x: x[1], reverse=True)

    # Afficher les résultats triés
    resultat_texte.config(state=tk.NORMAL)
    resultat_texte.delete(1.0, tk.END)
    resultat_texte.insert(tk.END, "Résultats de la recherche :\n")
    for i, (resultat) in enumerate(resultats_tries):
        resultat_texte.insert(tk.END, f"{i + 1}.\n")
        resultat_texte.insert(tk.END, f"{resultat}\n\n")
    resultat_texte.config(state=tk.DISABLED)


'''def recherche():

    # Fonction de recherche à implémenter
    # Ici, nous affichons simplement un exemple de texte dans la zone de résultats
    resultat_texte.config(state=tk.NORMAL)
    resultat_texte.delete(1.0, tk.END)
    resultat_texte.insert(tk.END, "Résultats de la recherche :\n")
    resultat_texte.insert(tk.END, "1. Résultat 1\n")
    resultat_texte.insert(tk.END, "2. Résultat 2\n")
    resultat_texte.insert(tk.END, "3. Résultat 3\n")
    resultat_texte.config(state=tk.DISABLED)

    # Afficher le menu déroulant de tri
    menu_tri_results.grid(row=3, column=0, columnspan=2, pady=(10, 0))
'''
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

# Création de la fenêtre principale
fenetre = tk.Tk()

# Titre de la fenêtre
fenetre.title("Moteur de recherche")

# Définir la taille de la fenêtre
fenetre.geometry("800x600")

# Centrer la fenêtre sur l'écran
largeur_ecran = fenetre.winfo_screenwidth()
hauteur_ecran = fenetre.winfo_screenheight()
x_pos = (largeur_ecran - 800) // 2
y_pos = (hauteur_ecran - 600) // 2
fenetre.geometry(f"800x600+{x_pos}+{y_pos}")

# Création du champ de recherche
champ_recherche = ttk.Entry(fenetre, width=50)
champ_recherche.grid(row=0, column=0, padx=10, pady=10)

# Bouton de recherche
bouton_recherche = ttk.Button(fenetre, text="Rechercher", command=recherche)
bouton_recherche.grid(row=0, column=1, padx=10, pady=10)

# Texte informatif
info_texte = ttk.Label(fenetre, text="Entrez votre requête de recherche ci-dessus : \n /!\ La requête doit être en anglais")
info_texte.grid(row=1, column=0, columnspan=2, pady=(0, 10))

# Résultats de la recherche (zone de texte déroulante)
resultat_texte = scrolledtext.ScrolledText(fenetre, wrap=tk.WORD, width=80, height=10)
resultat_texte.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
resultat_texte.config(state=tk.DISABLED)  # Pour rendre la zone de texte en lecture seule

# Menu déroulant de tri (initiallement caché)
critere_tri_var = tk.StringVar(fenetre)
critere_tri_var.set("Pertinence")  # Valeur par défaut
menu_tri_results = tk.OptionMenu(fenetre, critere_tri_var, "Pertinence", "Date", "Auteur", "Ordre alphabétique")
menu_tri_results.grid_remove()  # Cacher le menu déroulant initialement

# Bouton de tri des résultats
bouton_tri_results = ttk.Button(fenetre, text="Trier les résultats", command=lambda: trier_resultats(critere_tri_var.get()))
bouton_tri_results.grid(row=3, column=0, columnspan=2, pady=(10, 0))
bouton_tri_results.grid_remove()  # Cacher le bouton initialement

# Exécution de la boucle principale
fenetre.mainloop()
