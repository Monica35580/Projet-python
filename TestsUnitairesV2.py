import unittest
from Classes import Document, Author
from Corpus import Corpus
from CodeV2 import *

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
        self.assertEqual(texte_propre, "les jeux olympiques sont un vnement sportif mondial")
    
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
        collection_documents = []

        # Appeler la fonction
        creer_document(collection_documents)

        # Vérifier si la liste contient un document
        self.assertTrue(len(collection_documents) > 0, "La liste de documents devrait contenir au moins un document.")
    
    # Test de la fonction creer_auteur
    def test_creer_auteur(self):
        # Initialiser les données de test
        collection = [Document("Titre", "Auteur1", "2022/01/01", "https://fr.wikipedia.org/wiki/Jeux_olympiques", "Texte")]
        aut2id = {}
        num_auteurs_vus = 0

        auteurs_crees, aut2id, num_auteurs_vus = creer_auteur(collection, aut2id, num_auteurs_vus, collection[0])

        # Vérifier les résultats
        self.assertEqual(len(auteurs_crees), 1, "La création de l'auteur a échoué.")
        self.assertEqual(len(aut2id), 1, "Le mapping aut2id est incorrect.")
        self.assertEqual(num_auteurs_vus, 1, "Le nombre d'auteurs vus est incorrect.")

    # Test de la fonction creer_corpus
    def test_creer_corpus(self):
        collection = [Document("Titre", "Auteur", "2022/01/01", "https://fr.wikipedia.org/wiki/Jeux_olympiques", "Texte")]
        corpus = creer_corpus(collection)
        self.assertEqual(corpus.nom, "Corpus 2024", "La création du corpus a échoué.")
    
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

    '''La fonction test ne marche pas''' 
    # Test de la fonction test_trier_resultats_par_similarite
    def test_trier_resultats_par_similarite(self):
        # Créer des données de test
        vectoriseur = TfidfVectorizer(min_df=1)
        matrice_tfidf = vectoriseur.fit_transform(["Document1", "Document2", "Document3"])
        termes_recherche = ["olympic", "texte", "valeur"]
        collection_documents = ["Document 1", "Document 2", "Document 3"]

        # Appeler la fonction avec les mêmes paramètres
        resultats_tries = trier_resultats_par_similarite(matrice_tfidf, termes_recherche, vectoriseur, collection_documents)

        # Vérifier les résultats
        self.assertEqual(len(resultats_tries), len(collection_documents))

        # Afficher les résultats triés
        for document, similarite in resultats_tries:
            print(f"Similarite : {similarite[0]:.4f}")
            print(document)


if __name__ == '__main__':
    unittest.main()
