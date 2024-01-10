from Classes import Author
import pandas as pd
import re



def singleton(cls):
    instance = [None]
    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]
    return wrapper



# =============== 2.7 : CLASSE CORPUS ===============

@singleton

class Corpus:

    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

# =============== 2.8 : REPRESENTATION ===============

    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]
        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))
        return "\n".join(list(map(str, docs)))

    def search(self, mot_cle):
        p = re.compile(mot_cle, re.IGNORECASE)
        from TPs import longueChaineDeCaracteres
        ch= longueChaineDeCaracteres
        res= p.finditer(ch)
        for r in res:
            (i,j) = r.span()
            print("Trouver en position {a} : {b}".format(a=i, b=ch[i:j]))

    def concorde(self, contexte,expression):
        p = re.compile("(.{0,"+str(contexte)+"})"+expression+"(.{0,"+str(contexte)+"})", re.IGNORECASE)
        from TPs import longueChaineDeCaracteres
        ch = longueChaineDeCaracteres
        matches = p.finditer(ch)
        
        results = []

        for match in matches:
            gauche, droit = match.groups()
            result = {
                'contexte gauche': gauche.strip(),
                'motif trouvee': expression,
                'contexte droit': droit.strip()
            }
            results.append(result)
        df = pd.DataFrame(results)
        return print(df)
    
    def construire_tableau_freq(texte):   

        #Séparation du texte par délimitateur 
        mots = re.split(r'\s+|[.,;\'"()]+',''.join(texte))

        #Transformation du vocabulaire en form de liste
        vocabulaire2=[]
        for i in vocabulaire2:
                vocabulaire2.append(i)

        #Calcul de l'occurence de chaque mot
        frequences_mots = []
        document_freq=[]
        c=0
        for doc in texte:
            if mot in vocabulaire2:
                c+=1

                pass
        for mot in vocabulaire2:

            frequences_mots.append(mots.count(mot))

        return(print(vocabulaire2,frequences_mots))
    
    def construire_vocabulaire(texte):
        vocabulaire_set = set()

        # Diviser le texte en mots en utilisant plusieurs délimitations
        mots = re.split(r'\s+|[.,;\'"()]+', texte)
        # Ajouter les mots à l'ensemble

        vocabulaire_set.update(mots)
        # Construire un dictionnaire de vocabulaire avec des fréquences initiales à zéro
        vocabulaire = {mot: 0 for mot in vocabulaire_set}

        # Mettre à jour les fréquences en parcourant à nouveau les documents
        mots = re.split(r'\s+|[.,;\'"()]+',texte)
        for mot in mots:

            vocabulaire[mot] += 1

        return set(vocabulaire)
    
    def nettoyer_texte(texte):

        cleaned_text = texte.lower()

        cleaned_text = cleaned_text.replace('\n', ' ')

        cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)

        cleaned_text = re.sub(r'\d', '', cleaned_text)

        return cleaned_text


obj=Corpus("crp")
obj.concorde(6,"theDirichlet-Multinomial")
print(obj)

from Classes import RedditDocument, ArxivDocument
class DocumentGenerator:

    def factory (type,titre, auteur, date, url, texte, Nb_Com=None, co_auteurs=None):

        if type == "Reddit": return RedditDocument (titre, auteur, date, url, texte, Nb_Com)
        if type == "Arxiv": return ArxivDocument (titre, auteur, date, url, texte, co_auteurs)


'''crp=Corpus("nom_crp")
crp.add(DocumentGenerator.factory("Reddit","Titre Reddit", "Auteur Reddit", "Date Reddit", " url Reddit", "Texte Reddit", Nb_Com=10000000))

crp.add(DocumentGenerator.factory("Arxiv", "Titre Arxiv", "Auteur Arxiv", "Date Arxiv"," url Reddit","Texte Arxiv",co_auteurs=["Auteur1", "Auteur2"]))

print(crp)'''


#crp=Corpus("nom_crp")

#r=RedditDocument(titre="titre reddit", auteur="auteur reddit",date="date reddit",url=" reddit",texte="texte reddit",Nb_Com=15)

#co_aut = ["Auteur1", "Auteur2", "Auteur3"]

#a=ArxivDocument(titre="titre arxiv", auteur="auteur arxiv", date="date arxiv", url="url arxiv", texte="texte arxiv", co_auteurs=co_aut)

#crp.add(r)

#crp.add(a)

#crp.show()

#print(crp)





