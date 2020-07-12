# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label
from tkinter.messagebox import showerror
import datetime

from .AbstractPage import *

NOMFICHIER = os.sep + "duree"

class PageCalendrier(AbstractPage):
    def __init__(self, master, **kwargs):
        super().__init__(master, nom = "Calendrier", **kwargs)
        # Note : self.master renvoie a ParametrageZone
        # Note : Si on rajoute une option ne pas oublier d'ajouter la variable de controle à self._listData.append([variable, "texte explicatif", variableParDefaut])


        def changeMode(v): # Fonction d'assignement qu'un certain lambda sait pas faire
            self.__mode = v

        self.__lastValSbNbJour = None # Dernière valeur du spinbox pour savoir si on ajoute ou retire dans formatSpinBox()
        self.__mode = None
        ## Widget
        self.__varBtnAncienneConfig = BooleanVar()
        self._listData.append([self.__varBtnAncienneConfig, "recharger duree precedente", False])
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

        ## Frame style affichage jour
        self.__frameStyle = LabelFrame(self._mFrame, text = "Style d'affichage des jours")

        self.__varComboStyleFinal = StringVar()
        #self._listData.append([self.__varComboStyleFinal, "", "JSE NN MM"]) # TODO
        self.__comboStyleFinal = Combobox(self.__frameStyle, state = "readonly", textvariable = self.__varComboStyleFinal)
        self.__varLienStyle = StringVar()
        self._listData.append([self.__varLienStyle, "Lien", " "])
        self.__oldLien = self._listData[-1][-1] # pour le retrouver lorsqu'on change le lien et refaire l'affichage du combobox
        self.__comboLienStyle = Combobox(self.__frameStyle, state = "readonly", textvariable = self.__varLienStyle, value = [" ", "/", "-", "."])
        self.__comboLienStyle.bind("<<ComboboxSelected>>", lambda e=None : self.__chargerStyle())
        # Affichage numéro de la semaine
        self.__varNumDeLaSemaine = BooleanVar()
        self._listData.append([self.__varNumDeLaSemaine, "Numéro de la semaine", False])
        self.__numDeLaSemaine = Checkbutton(self.__frameStyle, text = "Numéro de la semaine", variable = self.__varNumDeLaSemaine, command = self.__activeSemaineWidget) # Widget
        self.__varCbStyleNumDeLaSemaine = StringVar()
        self._listData.append([self.__varCbStyleNumDeLaSemaine, "Style-numéro de la semaine", "Semaine"])
        self.__cbStyleNumDeLaSemaine = Combobox(self.__frameStyle, value = ["S", "Semaine"], textvariable = self.__varCbStyleNumDeLaSemaine, width = 10) # Widget
        self.__lbStyleNumDeLaSemaine = Label(self.__frameStyle, text = "Style :")
        # Décompte des semaines
        self.__varCompteurStyleJourDeLaSemaine = StringVar()
        self._listData.append([self.__varCompteurStyleJourDeLaSemaine, "Style-décompte numéro de la semaine", "Début de la période"])
        self.__cbCompteurNumDeLaSemaine = Combobox(self.__frameStyle, value = ["Début de la période", "Début de l'année", "Fin de la période"], textvariable = self.__varCompteurStyleJourDeLaSemaine) # Widget
        self.__lbCompteurNumDeLaSemaine = Label(self.__frameStyle, text = "depuis")


        # Affichage
        self.__btnAncienneConfig.pack(side=TOP, fill=X)

        self.__frameLbCombo.pack(side = TOP, fill = X, pady = 2)
        self.__lbNbJour.grid(column = 0, row = 0, sticky = "w")
        self.__sbNbJour.grid(column = 1, row = 0, sticky = "we")
        self.__btnAjouter.grid(column = 2, row = 0, sticky = "e", padx = 2)
        self.__listebDureeCree.grid(column = 0, row = 2, sticky = "we", columns=2, pady = 0, padx = 2)
        self.__btnSupprimer.grid(column = 2, row = 2, sticky = "n", pady = 2)

        self.__frameStyle.pack(side = TOP, fill = X)
        self.__comboStyleFinal.grid(         column = 0, row = 0, sticky = "we") # Combo des jours
        self.__comboLienStyle.grid(          column = 1, row = 0               ) # combo du lien
        self.__numDeLaSemaine.grid(          column = 0, row = 1, sticky = "w" ) # Checkbutton de l'affichage des semaines
        self.__lbStyleNumDeLaSemaine.grid(   column = 0, row = 2               ) # Label "style" de l'affichage semaine
        self.__cbStyleNumDeLaSemaine.grid(   column = 1, row = 2, sticky = "we") # Combobox du style
        self.__lbCompteurNumDeLaSemaine.grid(column = 2, row = 2               )
        self.__cbCompteurNumDeLaSemaine.grid(column = 3, row = 2, sticky = "we") # Combobox du comptage des semaines

        # Fonctions
        self._loadDataFile() # Pour les prefs standards
        self.__chargerListBox() # Pour les prefs durees
        self.__chargerStyle()
        self.__activeSemaineWidget() # gérer l'état des widgets de la semaine

    def __convSbStrToInt(self, value):
        """
        Fonction qui convertie le texte du spinbox et de getData()[section][nom] en nombre de jour
        @param value : <str> a convertir
        @return : <int> du nombre de jour
        """
        morceau = value.split(" ")
        # si c'est la période, à la fin
        if len(morceau) == 1:
            return 42
        elif len(morceau) == 2 and morceau[1].startswith("jour"):
            return int(morceau[0])
        elif len(morceau) == 2 and morceau[1].startswith("semaine"):
            return int(morceau[0])*7
        else:
            raise AttributeError()

    def __ajouter(self):
        """
        Enregistre la nouvelle durée crée
        """
        self.readFile(NOMFICHIER, lireDef=False)
        nom = self.__sbNbJour.get()
        duree = self.__convSbStrToInt(self.__sbNbJour.get()) # On prend que le nombre
        self.getData()[nom.upper()] = {"Nom":nom, "Duree en jour" : duree}

        self.getData().sauv(self.getProfilFolder() + NOMFICHIER + ".cfg")
        self.__chargerListBox()

    def __supprimer(self):
        """
        Supprime la durée sélectionné du combobox
        """
        self.readFile(NOMFICHIER, lireDef=False)

        section = self.__listebDureeCree.get(self.__listebDureeCree.curselection()).upper()
        if section in self.getData().sections():
            self.getData().remove_section(section)
        else:
            showerror("Action incorrect", "Vous ne pouvez pas retirer ce choix.")


        self.getData().sauv(self.getProfilFolder() + NOMFICHIER + ".cfg")
        self.__chargerListBox()

    def __chargerListBox(self):
        """
        Permet de mettre toutes les durée dans le listBox
        """
        self.readFile(NOMFICHIER)


        # On supprime toutes options
        self.__listebDureeCree.delete(0,END)

        listName = [] # Pour mettre toutes les options possible
        for section in self.getData().sections():
            listName.append(self.getData().get(section, "Nom"))

        # Trie de la liste
        listName.sort(key = lambda nom : self.__convSbStrToInt(nom))


        for duree in listName:
            self.__listebDureeCree.insert(END, duree)

    def __chargerStyle(self):
        """
        Permet de mettre toutes les possibilités de configuration d'affichage des jours dans self.__comboStyleFinal.
        """
        # Constantes
        jour        = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        mois        = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Décembre"]
        lien        = self.__varLienStyle.get()
        toudai      = datetime.datetime.today() # Pour la blague je le laisse, permet d'avoir un affichage joli

        numJour     = str(toudai.day)
        numMois     = str(toudai.month)
        numAnnee    = str(toudai.year)
        jourSemaine = str(jour[toudai.weekday()])
        mois        = str(mois[toudai.month])

        listAffichage = [] # liste des affichages disponible
        listAffichage.append(jourSemaine + lien + numJour + lien + mois)                          # Lundi 1 Janvier
        listAffichage.append(jourSemaine + lien + numJour + lien + mois + lien + numAnnee)        # Lundi 1 Janvier 2020
        listAffichage.append(jourSemaine + lien + numJour + lien + mois[:3])                      # Lundi 1 Jan
        listAffichage.append(jourSemaine + lien + numJour + lien + mois[:3] + lien + numAnnee)    # Lundi 1 Jan 2020

        listAffichage.append(jourSemaine[0] + lien + numJour + lien + mois)                       # L 1 Janvier
        listAffichage.append(jourSemaine[0] + lien + numJour + lien + mois + lien + numAnnee)     # L 1 Janvier 2020
        listAffichage.append(jourSemaine[0] + lien + numJour + lien + mois[:3])                   # L 1 Jan
        listAffichage.append(jourSemaine[0] + lien + numJour + lien + mois[:3] + lien + numAnnee) # L 1 Jan 2020

        listAffichage.append(numJour + lien + mois)                                               # 1 Janvier
        listAffichage.append(numJour + lien + mois + lien + numAnnee)                             # 1 Janvier 2020
        listAffichage.append(numJour + lien + mois[:3])                                           # 1 Jan
        listAffichage.append(numJour + lien + mois[:3] + lien + numAnnee)                         # 1 Jan 2020

        listAffichage.append(numJour + lien + numMois)                                            # 1 1
        listAffichage.append(numJour + lien + numMois + lien + numAnnee)                          # 1 1 2020


        self.__comboStyleFinal.config(value = listAffichage)
        ## Réafectation de la valeur d'avant (si on change le lien/première affectation)
        # Première affectation
        if self.__varComboStyleFinal.get() == "":
            self.__varComboStyleFinal.set(listAffichage[0]) # Lundi 1 Janvier
        # Changement du combo en cours
        else:
            self.__varComboStyleFinal.set(self.__varComboStyleFinal.get().replace(self.__oldLien, lien))
            self.__oldLien = lien


    def __activeSemaineWidget(self):
        """
        Fonction qui gère l'état des combobox des semaines en fct de l'état du checkbutton
        """
        if self.__varNumDeLaSemaine.get():
            self.__cbStyleNumDeLaSemaine.config(state = "readonly")
            self.__cbCompteurNumDeLaSemaine.config(state = "readonly")
        else :
            self.__cbStyleNumDeLaSemaine.config(state = "disabled")
            self.__cbCompteurNumDeLaSemaine.config(state = "disabled")

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
        self.readFile(NOMFICHIER)

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

        # Vérifie si c'est déjà existant en nombre de jours
        isValOk = False
        while not isValOk: # Je pense qu'on peut refactor ça # TODO
            for section in self.getData().sections():
                print(self.getData()[section], self.getData()[section]["Duree en jour"], val)
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
        self._makeDictAndSave()
