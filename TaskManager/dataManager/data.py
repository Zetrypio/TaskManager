# *-* coding:utf-8 *-*
from configparser import *
import os

from util.widgets.TextWidget import *
from util.util import adaptTextColor
from affichages.gantt.liens.AbstractLink import *

# Dictionnaires de couleurs
from preferences.themes.themeLoader import WIN_COLORS
from PIL.ImageColor import colormap

class Data(ConfigParser):
    def __init__(self):
        super().__init__(self)
        # Création des attributs
        self.__profilFolder = None
        self.__palette = {"background"        : "#dedede",
                          "foreground"        : "#000000",
                          "selected"          : "#91c9f7",
                          "jour"              : "#ffffa0",
                          "highlightedWidget" : "#cccccc",
                          "normalInnerLink"   : "#808080", # (= "grey" = "gray")
                          "addLink"           : "#ffaf00",
                          "deleteLink"        : "#ff3f3f"
                          }

    def endInit(self):
        """
        Méthode qui doit être appelé pour finir la construction de l'appli
        """
        # Donner une référence à data
        TextWidget.giveData(self)
        AbstractLink.giveData(self)

        ## Couleur du jour sélectionné
        if self.testDataExist("General", "Thème", "today's color"):
            couleur = self.getOneValue("General", "Thème", "today's color")
        else :
            couleur = self.getPalette()["jour"]
        self.changePalette("jour", couleur)

    "" # Marque pour le repli
    ################
    # Utilitaire : #
    ################
    ""
    def read(self, fichier, add = False):
        """
        On efface ce qu'on avait en mémoire
        et on relie tout
        """
        if not add:
            self.clear()
        super().read(fichier, encoding="utf-8")

    def readFile(self, nom, lireDef = True, lireCfg = True):
        """
        Fonction qui va lire les fichiers de préférences avec Data
        @param nom : <str> nom du fichier à lire (sans l'extension)
        """
        self.clear()
        if lireDef and lireCfg:
            self.read("Ressources/prefs/"+nom+".def")
            if os.path.exists(self.getProfilFolder() + nom + ".cfg"):
                self.read(self.getProfilFolder() + nom + ".cfg", add=True) # Prise de conscience de ce qu'il y a dedans

        # On ne met pas le add sinon
        elif not lireDef and lireCfg:
            if os.path.exists(self.getProfilFolder() + nom + ".cfg"):
                self.read(self.getProfilFolder() + nom + ".cfg") # Prise de conscience de ce qu'il y a dedans
        elif lireDef and not lireCfg:
            self.read("Ressources/prefs/"+nom+".def")

    def sauv(self, fichier):
        """
        Ecrit dans le fichier puis
        @param fichier : <str> contient le path + nom + extension du fichier dans lequel Data doit écrire
        # Note : une lecture de ce fichier est conseillé avant afin de ne pas supprimer tout le contenu inutilement
        """
        with open(fichier, "w", encoding="utf-8") as tfile:
            self.write(tfile)

    ""
    #############
    # Testeur : #
    #############
    ""
    def testBool(self, value):
       """ Test pour savoir si value est un Booléen """
       if not isinstance(value, bool):
           raise TypeError("Exptected a boolean")

    def testDataExist(self, nomFichier, nomSection = None, nomCle = None):
        """
        Méthode qui True si la valeur existe dans le fichier et la section indiqué
        @param nomFichier : <str> contient le nom du fichier dans lequel se trouve notre valeur
        @param nomSection : <str> contient le nom de la section dans laquelle se trouve notre valeur
        @param nomCle     : <str> contient le nom de la clé pour ainsi obtenir la valeur
        @return : True = la clé exsite, False = la clé, la section ou le fichier n'existe pas
        """
        self.readFile(nomFichier)
        # Le fichier existe ?
        if nomSection is None and nomCle is None:
            return True if self.sections() != [] else False
        # La section du fichier existe ?
        elif nomSection is not None and nomCle is None:
            return True if nomSection in self.sections() else False
        # J'ai mis la clé mais pas la section, c'est grave ? (ERROR)
        elif nomSection is None and nomCle is not None:
            raise ValueError("Une clé doit être lié a une section pour être trouvé")
        # La clé existe dans la section du fichier spécifié ?
        else :
            return True if nomSection in self.sections() and nomCle in self[nomSection] else False

    def testString(self, value):
       """ Test pour savoir si value est un String """
       if not isinstance(value, str):
           raise TypeError("Exptected a string")

    ""
    ###########
    # Getters #
    ###########
    ""
    def getOneValue(self, nomFichier, nomSection, nomCle):
        """
        Méthode qui renvoie une valeur précise
        @param nomFichier : <str> contient le nom du fichier dans lequel se trouve notre valeur
        @param nomSection : <str> contient le nom de la section dans laquelle se trouve notre valeur
        @param nomCle     : <str> contient le nom de la clé pour ainsi obtenir la valeur
        @return : la value
        """
        if not self.testDataExist(nomFichier, nomSection, nomCle):
            raise ValueError("%s n'existe pas dans %s du fichier %s.\n utiliser la méthode data.testDataExist() pour éviter l'erreur"%(nomCle, nomSection, nomFichier))
        return self[nomSection][nomCle]

    def getPalette(self):
        """
        Méthode qui retourne une copie de la palette de couleur
        @return <dict> self.__palette.copy()
        """
        return self.__palette.copy()

    def getProfilFolder(self):
        return self.__profilFolder

    ""
    ###########
    # Setters #
    ###########
    ""
    def changePalette(self, cle, value):
        """
        Permet de changer une valeur de la palette
        @param cle   : <str> contient le nom de la clé
        @param value : <str> couleur au format tkinter
        """
        if cle in self.getPalette():
            if value.startswith("System"):
                self.__palette[cle] = WIN_COLORS[value]
            elif value[0] != "#":
                self.__palette[cle] = colormap[value.lower()]
            else:
                self.__palette[cle] = value
        else:
            raise ValueError('"%s" not in data#__palette')
    def setCurrentTheme(self, style):
        """
        Setter pour un nouveau thème et donc change la palette
        @param style : <ttk.style> pour récuperer toutes les valeurs adéquates
        """
        def couleurAdaptative(native, accentuation, cle):
            """
            Fonction embarqué qui permet de mettre une couleur asé sur une autre
            avec une acctentuation différence
            @param native       : <str> couleur a tester (clair/foncé) et à modifier
            @param accentuation : <str> valeur de l'acctentuation en hexa. exemple : "121212"
            @param cle          : <str> nom de la clé de la nouvelle couleur
            """
            # Si c'est clair
            if adaptTextColor(native) == "#000000":
                self.changePalette(cle, "#" + hex(int(native[1:], 16) - int(accentuation, 16))[2:])
            # Si c'es foncé
            else :
                self.changePalette(cle, "#" + hex(int(native[1:], 16) + int(accentuation, 16))[2:])

        # On récup les valeurs pour les mettre dans le dico __palette
        self.changePalette("background", style.lookup(".", "background"))
        self.changePalette("foreground", style.lookup(".", "foreground"))
        if style.lookup(".", "selectbackground") != "":
            self.changePalette("selected", style.lookup(".", "selectbackground"))
        else: # Aquativo n'a pas de couleur de sélection
            self.changePalette("selected", "#85cafc")

        # Pour les TextWidget
        couleurAdaptative(self.getPalette()["background"], "121212", "highlightedWidget")
        # Pour les liens
        couleurAdaptative(self.getPalette()["background"], "555555", "normalInnerLink")

        return

    def setProfilFolder(self, value):
        """
        Setter du path du profil en cours
        @param value : <str> contient le path
        """
        self.testString(value)
        self.__profilFolder = value
        return
