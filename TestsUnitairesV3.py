import unittest
from Classes import Document, Author
from Corpus import Corpus
from CodeV3 import *

class TestFunctions(unittest.TestCase):
    
    # Test de la fonction obtenir_contenu_web venant d'un lien URL
    def test_obtenir_contenu_web(self):
        # Identification
        reddit = praw.Reddit(client_id='hOyL_L3Pir_9uU18wGBJkQ', client_secret='wBb7Zld_tKlDb9MDHyApFWZHK74VpA', user_agent='lucilecpp')

        # Requête
        limit = 100
        hot_posts = reddit.subreddit('all').hot(limit=limit)

        # Récupération du texte
        docs = []
        for i, post in enumerate(hot_posts):
            if i % 10 == 0:
                print("Reddit:", i, "/", limit)
            if post.selftext != "":
                docs.append(post.selftext.replace("\n", " "))
        self.assertIsNotNone(docs, "La récupération du contenu a échoué.")
    
    # Test de la fonction recuperer_contenu_web
    def test_recuperer_contenu_web(self):
        contenu_web = recuperer_contenu_web()
        self.assertIsNotNone(contenu_web, "La récupération du contenu web a échoué.")
    
    # Test de la fonction nettoyer_texte
    def test_nettoyer_texte(self):
        texte = "Les Jeux Olympiques sont un événement sportif mondial."
        texte_propre = nettoyer_texte(texte)
        self.assertEqual(texte_propre, "les jeux olympiques sont un vnement sportif mondial.")
    
    # Test de la fonction test_extraire_texte_pertinent
    def test_extraire_texte_pertinent(self):

        # Cas avec une liste contenant des chaînes de caractères
        contenu_web_liste = ["Texte sur les Jeux olympiques", "Autre texte sur les Jeux Olympiques", "Encore un texte"]
        termes_recherche = ["olympiques"]
        resultat_liste = extraire_texte_pertinent(contenu_web_liste, termes_recherche)

        print(f"Resultat pour la liste : {resultat_liste}")
        self.assertTrue(all(isinstance(texte, str) for texte in resultat_liste),
                        "Tous les éléments du résultat pour la liste doivent être des chaînes de caractères.")
        self.assertEqual(resultat_liste, ["texte sur les jeux olympiques", "autre texte sur les jeux olympiques", "encore un texte"],
                         "Le résultat pour la liste ne correspond pas à ce qui est attendu.")

        # Cas avec une chaîne de caractères
        contenu_web_str = "Texte unique sur les Jeux olympiques"
        resultat_str = extraire_texte_pertinent(contenu_web_str, termes_recherche)

        print(f"Resultat pour la chaine de caracteres : {resultat_str}")
        self.assertTrue(isinstance(resultat_str, list),
                        "Le résultat pour la chaîne de caractères doit être une liste.")
        self.assertEqual(resultat_str, ["texte unique sur les jeux olympiques"],
                         "Le résultat pour la chaîne de caractères ne correspond pas à ce qui est attendu.")

    # Test de la fonction traiter_texte_pertinent
    def test_traiter_texte_pertinent(self):
        texte_pertinent = ['Jeux olympiques 2024 à Paris.', 'Les Jeux olympiques sont un événement mondial.']
        texte_traite = traiter_texte_pertinent(texte_pertinent)
        self.assertTrue(len(texte_traite) > 0, "Le traitement du texte pertinent a échoué.")

    # Test de la fonction creer_document
    def test_creer_document(self):
        # Simuler du contenu web
        contenu_web_arxiv = [("ArXiv", {"summary": "Contenu ArXiv 1"}), ("ArXiv", {"summary": "Contenu ArXiv 2"})]
        contenu_web_reddit = [("Reddit", "Contenu Reddit 1"), ("Reddit", "Contenu Reddit 2")]

        # Utiliser la liste pour stocker les documents
        collection_document = creer_document()

        # Vérifier si la liste contient un document
        self.assertTrue(len(collection_document) > 0, "La liste de documents devrait contenir au moins un document.")
    
    # Test de la fonction creer_corpus
    def test_creer_corpus(self):
        collection = [Document("Titre", "Auteur", "2022/01/01", "https://fr.wikipedia.org/wiki/Jeux_olympiques", "Texte")]
        corpus = creer_corpus(collection)
        self.assertEqual(corpus.nom, "Corpus Web Paris 2024", "La création du corpus a échoué.")
    
    # Test de la fonction sauvegarder_et_charger_corpus
    def test_sauvegarder_et_charger_corpus(self):
        collection = [Document("Titre", "Auteur", "2024/01/01", "https://fr.wikipedia.org/wiki/Jeux_olympiques", "Texte")]
        corpus_cree = creer_corpus(collection)
        corpus_sauvegarde_charge = sauvegarder_et_charger_corpus(corpus_cree)
        self.assertIsInstance(corpus_sauvegarde_charge, Corpus, "La sauvegarde et le chargement du corpus ont échoué.")
    
    # Test de la fonction obtenir_matrice_tfidf
    def test_obtenir_matrice_tfidf(self):
        texte = "Ceci est un exemple de texte à utiliser pour le test de la matrice TF-IDF."

        # Appeler la fonction avec le texte
        matrice_tfidf = obtenir_matrice_tfidf([texte])

        # Vérifier si la matrice TF-IDF est créée avec succès
        self.assertIsNotNone(matrice_tfidf, "L'obtention de la matrice TF-IDF a échoué.")
        
        # Afficher la matrice TF-IDF
        print("Matrice TF-IDF :")
        print(matrice_tfidf)
    
    # Test de la fonction comparer_nombres_mots_longueur
    def test_comparer_nombres_mots_longueur(self):
        # Cas où le texte est vide
        texte_vide = ""
        resultat_vide = comparer_nombres_mots_longueur(texte_vide)
        self.assertEqual(resultat_vide, (0, 0), "Le résultat pour le texte vide devrait être (0, 0).")

        # Cas avec un texte non vide
        texte_non_vide = "Ceci est un exemple de texte."
        resultat_non_vide = comparer_nombres_mots_longueur(texte_non_vide)

        # Calculer manuellement le nombre de mots et la longueur du texte
        mots_manuels = len(re.split(r'\s+|[.,;\'"()]+', texte_non_vide))
        longueur_manuelle = len(texte_non_vide)
        print(f"Calcul - Nombre de mots : {mots_manuels}, Longueur du texte : {longueur_manuelle}")

        # Vérifier si les résultats correspondent aux calculs manuels
        self.assertEqual(resultat_non_vide, (mots_manuels, longueur_manuelle),
                         "Les résultats ne correspondent pas aux calculs manuels.")

    # Test de la fonction compter_phrases
    def test_compter_phrases(self):
        texte_1 = "C'est une phrase. Et voici une autre phrase!"
        texte_2 = "Une seule phrase ici."
        texte_3 = "Pas de mal du tout. C'est la dernière fois !! Attention a toi."
        
        self.assertEqual(compter_phrases(texte_1), 2)
        self.assertEqual(compter_phrases(texte_2), 1)
        self.assertEqual(compter_phrases(texte_3), 3)

    # Test de la fonction compter_mots
    def test_compter_mots(self):
        texte_1 = "Ceci est un exemple de phrase."
        texte_2 = "Python est un langage de programmation puissant."
        texte_3 = "   Il   est  présent   plusieurs    espaces."
        
        self.assertEqual(compter_mots(texte_1), 6)
        self.assertEqual(compter_mots(texte_2), 7)
        self.assertEqual(compter_mots(texte_3), 5)

    # Test de la fonction compter_caracteres
    def test_compter_caracteres(self):
        texte_1 = "Ceci est une phrase."
        texte_2 = "Python est un langage de programmation."
        texte_3 = "   Il   y a   des    espaces   supplémentaires.   "
        
        self.assertEqual(compter_caracteres(texte_1), 20) 
        self.assertEqual(compter_caracteres(texte_2), 39)
        self.assertEqual(compter_caracteres(texte_3), 50)  

    # Test de la fonction  creation_df
    def test_creation_df(self):
        # Données de test
        contenu = ["premier texte", "autre exemple de texte."]
        auteurs = ["Auteur1", "Auteur2"]
        dates = ["2022-01-01", "2022-01-02"]
        titres = ["Titre1", "Titre2"]
        nom_var = "OrigineTest"

        # Appeler la fonction à tester
        result_df = creation_df(contenu, auteurs, dates, titres, nom_var)

        # Vérifier si le DataFrame a été créé correctement
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertEqual(len(result_df), len(contenu))
        self.assertListEqual(result_df['Auteur'].tolist(), auteurs)
        self.assertListEqual(result_df['Date'].tolist(), dates)
        self.assertListEqual(result_df['Titre'].tolist(), titres)
        self.assertListEqual(result_df['Origine'].tolist(), [nom_var] * len(contenu))

        # Vérifier si le contenu a été correctement nettoyé
        for i, cleaned_text in enumerate(result_df['Contenu']):
            self.assertEqual(cleaned_text, nettoyer_texte(contenu[i]))

if __name__ == '__main__':
    unittest.main()
