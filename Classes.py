
#from Classes import RedditDocument
#from Classes import Document

# =============== CLASSE DOCUMENT ===============
class Document:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte="", texte_pertinent=""):
        self.id = None
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.texte_pertinent = texte_pertinent

# =============== REPRESENTATIONS ===============
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"


# =============== CLASSE AUTHOR ===============
class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []
# =============== ADD ===============
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"

# =============== RedditDocument =============== 
'''class RedditDocument(Document):
    def __init__(self,titre="", auteur="", date="", url="", texte="" ,Nb_Com=None):
        super().__init__(titre,auteur,date,url,texte)
        self.Nb_Com = Nb_Com

    def getNb_Com(self):
        return(self.Nb_Com)
   
    def setNb_Com(self, Nb_Com):
        self.Nb_Com=Nb_Com

    def __str__(self):
        return f"{super().__str__()} Nombre de commentaires : {self.Nb_Com}"

    def getType(self):
        return("Reddit")
    
# =============== ArxivDocument ===============
class ArxivDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="", co_auteurs=None):
        super().__init__(titre, auteur, date, url, texte)
        self.co_auteurs = co_auteurs if co_auteurs is not None else []

    def get_co_auteurs(self):
        return self.co_auteurs

    def set_co_auteurs(self, co_auteurs):
        self.co_auteurs = co_auteurs

    def __str__(self):
        co_auteurs_str = ", ".join(self.co_auteurs) if self.co_auteurs else "404 "
        return f"{super().__str__()} co-auteurs : {co_auteurs_str}"
    
    def getType(self):
        return("Arxiv")'''