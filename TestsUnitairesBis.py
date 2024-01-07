import unittest
from Classes import Document, Author
from Corpus import Corpus
from CodeBis import *
'''from Code import obtenir_contenu_web, recuperer_contenu_web, extraire_texte_pertinent, traiter_texte_pertinent, nettoyer_texte
from Code import creer_document, creer_auteur, creer_corpus, sauvegarder_et_charger_corpus, obtenir_matrice_tfidf'''
class TestFunctions(unittest.TestCase):
    
    # Test de la fonction obtenir_contenu_web venant d'un lien URL
    def test_obtenir_contenu_web(self):
        url = 'https://fr.wikipedia.org/wiki/Jeux_olympiques'
        contenu = obtenir_contenu_web(url)
        self.assertIsNotNone(contenu, "La récupération du contenu a échoué.")

    # Test de la fonction recuperer_contenu_web
    def test_recuperer_contenu_web(self):
        url = 'https://fr.wikipedia.org/wiki/Jeux_olympiques'
        contenu_web = recuperer_contenu_web(url)
        self.assertIsNotNone(contenu_web, "La récupération du contenu web a échoué.")
    
    # Test de la fonction nettoyer_texte
    def test_nettoyer_texte(self):
        texte_sale = 'Jeux olympiques 2024 à <div>Paris</div>.'
        texte_nettoye = nettoyer_texte(texte_sale)
        texte_attendu = {'', 'Paris', 'Jeux', 'olympiques', 'à', '2024'}
        self.assertEqual(texte_nettoye, texte_attendu, "Le nettoyage du texte a échoué.")
        
    def test_extraire_texte_pertinent(self):
        #url_test = 'https://fr.wikipedia.org/wiki/Jeux_olympiques'
        contenu_web = "Les jeux olympiques rassemblent des athletes du monde entier dans un esprit de competition saine et de fraternite."
        termes_recherche = ["jeux", "olympique"]
        texte_pertinent = extraire_texte_pertinent(contenu_web, termes_recherche)
        textes_attendus = [{'frate', 'rassemblent', 'les', 'dans', 'de', 'esprit', 'monde', 'saine', 'du', 'un', 'et', 'entier', 'athletes', 'jeux', 'des', 'olympiques', 'competition'}, {'', 'rassemblent', 'les', 'dans', 'de', 'esprit', 'monde', 'saine', 'du', 'un', 'et', 'fraternite', 'entier', 'athletes', 'jeux', 'des', 'olympiques', 'competition'}]
        print("Contenu web:", contenu_web)
        print("Termes de recherche:", termes_recherche)
        print("Texte extrait:", texte_pertinent)
        print("Texte attendu:", textes_attendus)
        self.assertListEqual(texte_pertinent, textes_attendus, "L'extraction du texte pertinent a échoué.")
    
    # Test de la fonction traiter_texte_pertinent
    def test_traiter_texte_pertinent(self):
        texte_pertinent = ['Jeux olympiques 2024 à Paris.', 'Les Jeux olympiques sont un événement mondial.']
        texte_traite = traiter_texte_pertinent(texte_pertinent)
        self.assertTrue(len(texte_traite) > 0, "Le traitement du texte pertinent a échoué.")

    # Test de la fonction creer_document
    def test_creer_document(self):
        collection = []
        url = 'https://fr.wikipedia.org/wiki/Jeux_olympiques'
        longue_chaine = 'Jeux olympiques 2024 à Paris.'
        creer_document(collection, url, longue_chaine)
        self.assertEqual(len(collection), 1, "La création du document a échoué.")
    
    # Test de la fonction creer_auteur
    '''def test_creer_auteur(self):
        collection = [Document("Titre", "Auteur1", "2022/01/01", "https://fr.wikipedia.org/wiki/Jeux_olympiques", "Texte")]
        auteurs = {'Lyon2 Universite'}
        aut2id = {}
        num_auteurs_vus = 0
        creer_auteur(collection, aut2id, num_auteurs_vus, collection[0])
        self.assertEqual(len(auteurs), 1, "La création de l'auteur a échoué.")'''
    
    # Test de la fonction creer_corpus
    def test_creer_corpus(self):
        collection = [Document("Titre", "Auteur", "2022/01/01", "https://fr.wikipedia.org/wiki/Jeux_olympiques", "Texte")]
        corpus = creer_corpus(collection)
        self.assertEqual(corpus.nom, "Corpus Web Paris 2024", "La création du corpus a échoué.")

    # Test de la fonction sauvegarder_et_charger_corpus
    def test_sauvegarder_et_charger_corpus(self):
        collection = [Document("Titre", "Auteur", "2022/01/01", "https://fr.wikipedia.org/wiki/Jeux_olympiques", "Texte")]
        corpus_cree = creer_corpus(collection)
        corpus_sauvegarde_charge = sauvegarder_et_charger_corpus(corpus_cree)
        self.assertIsInstance(corpus_sauvegarde_charge, Corpus, "La sauvegarde et le chargement du corpus ont échoué.")

    # Test de la fonction obtenir_matrice_tfidf
    def test_obtenir_matrice_tfidf(self):
        collection = [Document("Titre", "Auteur", "2022/01/01", "https://fr.wikipedia.org/wiki/Jeux_olympiques", "Texte")]
        corpus = creer_corpus(collection)
        matrice_tfidf, noms_caracteristiques = obtenir_matrice_tfidf(corpus)
        self.assertIsNotNone(matrice_tfidf, "L'obtention de la matrice TF-IDF a échoué.")
    
    # Test de la fonction comparer_nombres_mots_longueur
    def test_comparer_nombres_mots_longueur(self):
        # Cas de test avec un texte simple
        texte_simple = "Ceci est un exemple de texte."
        resultat = comparer_nombres_mots_longueur(texte_simple)
        print(resultat)
        self.assertEqual(resultat, (7, len(texte_simple)))

        # Cas de texte vide
        texte_vide = ""
        resultat_vide = comparer_nombres_mots_longueur(texte_vide)
        print(resultat_vide)
        self.assertEqual(resultat_vide, (0, 0))

        # Cas de texte spécial (vide ou contenant seulement des espaces)
        texte_special = "          "
        resultat_special = comparer_nombres_mots_longueur(texte_special)
        print(resultat_special)
        self.assertEqual(resultat_special, (0, len(texte_special.strip())))  # Utilisez strip pour supprimer les espaces inutiles


if __name__ == '__main__':
    unittest.main()
