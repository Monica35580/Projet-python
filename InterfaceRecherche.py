import tkinter as tk
from tkinter import ttk
import requests

def search(query):
    url = "https://www.google.com/search"
    params = {'q': query}
    response = requests.get(url, params=params)

    # Vous pouvez traiter la réponse ici selon vos besoins
    # Pour cet exemple, nous imprimons simplement l'URL de la requête
    print("URL de la requête:", response.url)

def on_search_button_click():
    query = entry.get()
    search(query)

# Création de la fenêtre principale
window = tk.Tk()
window.title("Moteur de Recherche")

# Obtenir la moitié de la taille de l'écran
screen_width = window.winfo_screenwidth() 
screen_height = window.winfo_screenheight() 

# Définir la taille de la fenêtre en conséquence
window.geometry(f"{screen_width}x{screen_height}+{screen_width//4}+{screen_height//4}")

# Création des widgets
label = tk.Label(window, text="Entrez votre requête:")
entry = ttk.Entry(window, width=30)
search_button = ttk.Button(window, text="Rechercher", command=on_search_button_click)

# Placement des widgets dans la fenêtre
label.grid(row=0, column=0, padx=10, pady=10)
entry.grid(row=0, column=1, padx=10, pady=10)
search_button.grid(row=1, column=0, columnspan=2, pady=10)

# Lancement de la boucle principale
window.mainloop()
