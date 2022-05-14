# *-* coding:utf-8 *-*
from json import *
import os

NOMFICHIER = "clavier"

class BindingManager:
    def __init__(self, app):
        """
        Classe qui s'occupe d'enregistrer les bindings au format json
        """
        self.__app = app

        self.__donneePref = None
        self.__donneeUtil = None
        self.__donnee = None # Addition des 2 précédents

        self.__load()

    "" # Marque pour le repli
    #############
    # Getters : #
    #############
    ""
    def getApplication(self):
        return self.__app

    def getBind(self, path, section, bindingVirtuel):
        """
        Fonction qui va lire une ligne précise du fichier indiqué par path

        @param path : <str> chemin ver le fichier
        @param section : <str> nom du dictionnaire à consulter
        @param bindingVirtuel : <str> nom du binding virtuel à consulter

        @return bind : <str> contient le bind
        """
#        with open(path + NOMFICHIER + ".json", "r", encoding="utf-8") as f:
#            donnee = load(f)

        return self.__donnee[section][bindingVirtuel]["bindings"]

    def getBindings(self):
        """
        @return une copie self.__donnee : <dict> qui contient tous les binds de l'application
        """
        return self.__donnee.copy()

    def getProfilFolder(self):
        return self.getApplication().getProfilManager().getProfilFolder(None)

    ""
    #############
    # Setters : #
    #############
    ""
    def __load(self, lireCfg = True, lireDef = True):
        """
        Permet de lire les fichiers
        @param lireCfg = <bool> lit ou pas le json de l'utilisateur
        @param liredef = <bool> lit ou pas le json par défaut
        """
        if lireCfg:
            if os.path.exists(self.getProfilFolder() + NOMFICHIER + ".json"):
                with open(self.getProfilFolder() + NOMFICHIER + ".json", "r", encoding="utf-8") as f:
                    self.__donneeUtil = load(f)
            else:
                self.__donneeUtil = {}

        if lireDef:
            if os.path.exists("Ressources/prefs/" + NOMFICHIER + ".json"):
                with open("Ressources/prefs/" + NOMFICHIER + ".json", "r", encoding="utf-8") as f:
                    self.__donneePref = load(f)
            else:
                with open("Ressources/prefs/" + NOMFICHIER + ".json", "w", encoding="utf-8") as f:
                    f.write(dumps({"user":{}, "profil":{}}, indent=4))
                with open("Ressources/prefs/" + NOMFICHIER + ".json", "r", encoding="utf-8") as f:
                    self.__donneePref = load(f)

        ## TODO : Il y a maintenant une syntaxe en python pour faire cette opération.
        ## Fusion des 2 dicts
        # Pour les section manquante
        for section in self.__donneePref:
            # Si elle n'y est pas, on la rajoute entièrement et c'est fini
            if not section in self.__donneeUtil:
                self.__donneeUtil[section] = self.__donneePref[section]
                continue
            # Pour les binds manquants :
            for bind in self.__donneePref[section]:
                if not bind in self.__donneeUtil[section]:
                    # On les rajoute un à un
                    self.__donneeUtil[section][bind] = self.__donneePref[section][bind]

        # Trie alphabétique
        temp = dict(sorted(self.__donneeUtil.items(), key=lambda t:t[0]))
        for dicti in temp:
            temp[dicti] = dict(sorted(temp[dicti].items(), key=lambda t:t[0]))

        self.__donnee = temp

    ""
    ## Setter lié au fichier
    ""
    def save(self, dico):
        """
        Fonction qui va écrire le json de l'utilisateur
        @param dico : <dict> qui contient les nouvelles données
        """
        with open(self.getProfilFolder() + NOMFICHIER + ".json", "w", encoding="utf-8") as f:
            f.write(dumps(dico, indent=4))

        self.__load()

