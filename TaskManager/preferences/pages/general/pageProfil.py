# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame, Button as TkButton
from shutil import move

from json import load, dumps # Pour la lecture/écriture de JSON
from preferences.dialog.askProfil import *

from ..AbstractPage import *

NOMFICHIER = "Ressources/prefs/profils.json"


class PageProfil(AbstractPage):
    def __init__(self, master, **kwargs):
        # Note : self.master renvoie a ParametrageZone
       super().__init__(master, nom = "Profil", iid_parent ="-General", **kwargs)

       ## Widgets
       self.__lbProfil = Label(self._mFrame, text="Profil :")
       self.__cbProfil = Combobox(self._mFrame, state="readonly")
       # Folder location
       self.__lbPathCustomFile = Label(self._mFrame, text = "Chemin d'enregistrement de vos fichiers de préférences")
       self.__varEntryPath = StringVar()
       self.__entryPathCustomFile = Entry(self._mFrame, state="normal", textvariable = self.__varEntryPath)
       self.__btnParcourir = Button(self._mFrame, text = "...", command = self.__parcourir, width=3)


       # Affichage
       self.__lbProfil.grid(column = 0, row = 0, sticky = "w")
       self.__cbProfil.grid(column = 1, row = 0, sticky="we")
       self.__lbPathCustomFile.grid(column = 0, row = 1, sticky = "w")
       self.__entryPathCustomFile.grid(column = 0, row = 2, sticky = "we")
       self.__btnParcourir.grid(column = 1, row = 2, sticky = "w")

       # Fonction de parametrage
       self.__chargeProfil()

    def __parcourir(self):
       """
       fonction qui demande où stocker les fichier ET vérifie si le dossier est bien vide
       """
       path = askFolder(vide=True)
       # On bouge les fichiers en place
       #move(self.__varEntryPath.get(), path) Pas en place à cause d'un soucis de première location d'enregistrement

       # on set le nouveau path
       if path is not None:
           self.__varEntryPath.set(path)

    def __chargeProfil(self):
        """
        Fonction qui va chercher la position de sauvegarde des fichiers
        Pour : parametrer le combobox des profils
               remplir le champs du dossier d'enregistrement
        """
        ## Lecture
        # On test si le fichier existe, sinon on le crée

        try: # TODO : retravailler pour prendre en compte plusieurs utilisateurs
            with open(NOMFICHIER,"r") as f:
                data = load(f)
                data["user"]
        except:
            nom, folder = askProfil(True, self.getApplication())
            data = {"user" : {os.getlogin() : nom}, "folder":{nom : folder}}
            with open(NOMFICHIER, "w") as f:
                f.write(dumps(data, indent=4))

    def appliqueEffet(self, application):
       pass



