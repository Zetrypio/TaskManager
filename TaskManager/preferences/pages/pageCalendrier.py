# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label
from tkinter.messagebox import showerror

from .AbstractPage import *

NOMFICHIER = "duree.cfg"

class PageCalendrier(AbstractPage):
    def __init__(self, master, **kwargs):
        super().__init__(master, nom = "Calendrier", **kwargs)
        # Note : self.master renvoie a ParametrageZone

        def changeMode(v): # Fonction d'assignement qu'un certain lambda sait pas faire
            self.__mode = v

        self.__lastValSbNbJour = None # Dernière valeur du spinbox pour savoir si on ajoute ou retire dans formatSpinBox()
        self.__mode = None
        ## Widget
        self.__varBtnAncienneConfig = BooleanVar()
        # TODO : changer le texte en un truc plus mieux
        self.__btnAncienneConfig = Checkbutton(self._mFrame, text = "Recharger la durée d'affichage du dernier lancement", variable = self.__varBtnAncienneConfig)

        ## Frame options de durée custom du combobox
        self.__frameLbCombo = LabelFrame(self._mFrame, text = "Gérez les durées d'affichages personnalisées")
        self.__lbNbJour = Label(self.__frameLbCombo, text = "Nombre de jour à afficher :")
        self.__sbNbJour = Spinbox(self.__frameLbCombo, from_=1, to=31, command = self.__formatSpinBox)
        self.__sbNbJour.bind("<<Increment>>", lambda e : changeMode("Ajouter"))
        self.__sbNbJour.bind("<<Decrement>>", lambda e : changeMode("Retirer"))
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
        self.getData()[nom.upper()] = {"Nom":nom}

        self.getData().sauv(NOMFICHIER)
        self.__chargerListBox()

    def __supprimer(self):
        """
        Supprime la durée sélectionné du combobox
        """
        self.getData().read(NOMFICHIER)

        section = self.__listebDureeCree.get(self.__listebDureeCree.curselection()).upper()
        if section in self.getData().sections():
            self.getData().remove_section(section)
        else:
            showerror("Action incorrect", "Vous ne pouvez pas retirer ce choix.")

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

    def __formatSpinBox(self):
        """
        Applique un formatage du texte
        """
        def changeVal(val):
            if self.__mode == "Retirer":
                return val - 1
            elif self.__mode == "Ajouter":
                return val + 1
        def semaine(v, nb):
            if nb > 1 :
                self.__sbNbJour.set(v + " semaines")
            else:
                self.__sbNbJour.set(v + " semaine")
        def jour(v):
            self.__sbNbJour.set(v + " jours")

        # Lecture
        self.getData().read(NOMFICHIER)
        self.getData().read("duree.def", add = True)

        ## Gestion de val en fct de semaine ou jour
        # Si on est au tout début pour escape l'erreur du calcul
        if self.__lastValSbNbJour is None:
            val = int(self.__sbNbJour.get())
        # Si on était une semaine
        elif self.__lastValSbNbJour %7 ==0:
            if self.__mode == "Ajouter":
                val = self.__lastValSbNbJour + 1
            elif self.__mode == "Retirer":
                val = self.__lastValSbNbJour - 1
        else:
            val = int(self.__sbNbJour.get())*1

        # On set le nouveau __lastValSbNbJour
        self.__lastValSbNbJour = val

        isValOk = False
        while not isValOk: # Je pense qu'on peut refactor ça # TODO
            for section in self.getData().sections():
                isValOk = False
                if self.getData()[section]["Duree en jour"] == str(val):
                    val = changeVal(val)
                    break # pour ne pas metre en True, il faut retester toutes les sections
                isValOk = True

        if val % 7 == 0:
            semaine(str(val//7), val/7)
        else:
            jour(str(val))

    def appliqueEffet(self, application):
        pass
