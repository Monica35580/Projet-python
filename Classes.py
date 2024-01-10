# Correction de G. Poux-Médard, 2021-2022



# =============== 2.1 : La classe Document ===============

class Document:

    # Initialisation des variables de la classe

    def __init__(self, titre="", auteur="", date="", url="", texte="", origine=""):

        self.titre = titre

        self.auteur = auteur

        self.date = date

        self.url = url

        self.texte = texte

        self.origine=origine



# =============== 2.2 : REPRESENTATIONS ===============

    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)

    def __repr__(self):

        return f"Provient de {self.getType()}, Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t Origine : {self.origine}\t"



    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)

    def __str__(self):

        return f"Provient de {self.getType()}, {self.titre}, par {self.auteur}"



    def getType(self):

        pass



# =============== 2.4 : La classe Author ===============

class Author:

    def __init__(self, name):

        self.name = name

        self.ndoc = 0

        self.production = []

# =============== 2.5 : ADD ===============

    def add(self, production):

        self.ndoc += 1

        self.production.append(production)

    def __str__(self):

        return f"Auteur : {self.name}\t# productions : {self.ndoc}"





class RedditDocument(Document):

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

    



from Classes import RedditDocument

from Classes import Document



#doc=Document(titre="titre", auteur="auteur",date="date",url="url",texte="texte")

#print("b",doc.__repr__)

#print("a",doc)



#reddit_doc = RedditDocument(titre="titre", auteur="auteur",date="date",url="url",texte="texte",Nb_Com=10)

#reddit_doc = RedditDocument(Nb_Com=10)

#print(reddit_doc)





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

        return("Arxiv")

#co_auteurs = ["Auteur1", "Auteur2", "Auteur3"]

#arxiv_article = ArxivDocument(titre="titre", auteur="auteur", date="date", url="url", texte="texte", co_auteurs=co_auteurs)

#print(arxiv_article)
