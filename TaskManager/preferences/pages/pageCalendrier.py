# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from .AbstractPage import *

NOMFICHIER = "duree.cfg"

class PageCalendrier(AbstractPage):
    def __init__(self, master, **kwargs):
        super().__init__(master, nom = "Calendrier", **kwargs)
        # Note : self.master renvoie a ParametrageZone
        ## Widget
        self.__varBtnAncienneConfig = BooleanVar()
        # TODO : changer le texte en un truc plus mieux
        self.__btnAncienneConfig = Checkbutton(self._mFrame, text = "Recharger la durée d'affichage du dernier lancement", variable = self.__varBtnAncienneConfig)

        ## Frame options de durée custom du combobox
        self.__frameLbCombo = LabelFrame(self._mFrame, text = "Gérez les durées d'affichages personnalisées")
        self.__lbNbJour = Label(self.__frameLbCombo, text = "Nombre de jour à afficher :")
        self.__sbNbJour = Spinbox(self.__frameLbCombo, from_=0, to=31)
        self.__btnAjouter = Button(self.__frameLbCombo, text = "Ajouter", command = self.__ajouter)
        self.__listebDureeCree = Listbox(self.__frameLbCombo)
        self.__btnSupprimer = Button(self.__frameLbCombo, text = "Supprimer", command = self.__supprimer)


        # Affichage
        self.__btnAncienneConfig.pack(side=TOP, fill=X)

        self.__frameLbCombo.pack(side = TOP, fill = X, pady = 2)
        self.__lbNbJour.grid(column = 0, row = 0, sticky = "w")
        self.__sbNbJour.grid(column = 1, row = 0, sticky = "we")
        self.__btnAjouter.grid(column = 2, row = 0, sticky = "e", padx = 2)
        self.__listebDureeCree.grid(column = 0, row = 2, sticky = "we", columns=2, pady = 0, padx = 2)
        self.__btnSupprimer.grid(column = 2, row = 2, sticky = "n", pady = 2)

        # Fonctions
        self.__chargerListBox()

    def __ajouter(self):
        """
        Enregistre la nouvelle durée crée
        """
        self.getData().read(NOMFICHIER)

        nom = self.__sbNbJour.get()
        duree = self.__sbNbJour.get()
        self.getData()[nom.upper()] = {"Nom":nom, "Duree en jour":duree}

        self.getData().sauv(NOMFICHIER)
        self.__chargerListBox()

    def __supprimer(self):
        """
        Supprime la durée sélectionné du combobox
        """
        self.getData().read(NOMFICHIER)

        section = self.__listebDureeCree.get(self.__listebDureeCree.curselection()).upper()
        self.getData().remove_section(section)

        self.getData().sauv(NOMFICHIER)
        self.__chargerListBox()

    def __chargerListBox(self):
        """
        Permet de mettre toutes les durée dans le listBox
        """
        self.getData().read(NOMFICHIER)
        self.getData().read("duree.def", add = True)


        # On supprime toutes options
        self.__listebDureeCree.delete(0,END)

        listName = [] # Pour mettre toutes les options possible
        for section in self.getData().sections():
            listName.append(self.getData().get(section, "Nom"))

        # TODO : Trie de la liste

        for duree in listName:
            self.__listebDureeCree.insert(END, duree)

    def appliqueEffet(self, application):
        pass
