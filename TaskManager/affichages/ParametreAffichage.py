# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

class ParametreAffichage(Frame):
    """
    Classe contenant les boutons permettant de savoir
    de quand à quand on affiche dans les calendriers.
    """
    def __init__(self, master = None, **kwargs):
        """
        Constructeur de ParametreAffichage.
        @param master: master du tkinter.Frame() que cet objet est.
        @param **kwargs: configurations d'affichage du tkinter.Frame() que cet objet est.
        """
        #kwargs["bg"] = "yellow" # on en a pas besoin en vrai
        super().__init__(master, **kwargs)
        # Note : self.master est référence vers ZoneAffichage.

        # Boutons avant :
        self.boutonBienAvant = Button(self, text="<<", command=lambda:master.envoyerChangementJourDebut("d"))
        self.boutonBienAvant.pack(side=LEFT, fill=Y)
        self.boutonAvant = Button(self, text="<", command=lambda:master.envoyerChangementJourDebut(-1))
        self.boutonAvant.pack(side=LEFT, fill=Y)    

        # Boutons après :
        self.boutonBienApres = Button(self, text=">>", command=lambda:master.envoyerChangementJourDebut("f"))
        self.boutonBienApres.pack(side=RIGHT, fill=Y)          
        self.boutonApres = Button(self, text=">", command=lambda:master.envoyerChangementJourDebut(1))
        self.boutonApres.pack(side=RIGHT, fill=Y)             

        ## Frame du milieu
        self.midFrame = Frame(self)
        # Label : de la période
        self.lbPeriode = Label(self.midFrame, text = "Periode :")
        # Combobox de quelle période :
        self.listePeriode = Combobox(self.midFrame, values=['Periode'], state= "readonly")
        self.listePeriode.set(self.listePeriode.cget("values")[-1])
        #self.listePeriode.bind("<<ComboboxSelected>>",lambda e = None : self.setPeriodeActiveForApp()) # TODO
        # Label : du combien de jour
        self.lbCbJour = Label(self.midFrame, text = "Montrer :")
        # Combobox de combien de jours :
        self.listeMode = Combobox(self.midFrame, values=['Periode'], state= "readonly")
        self.listeMode.set(self.listeMode.cget("values")[-1])
        self.listeMode.bind("<<ComboboxSelected>>",master.envoyerChangementNbJour) #passer par le maître et pas de parenthèses car on n'appelle pas la fonction, on la passe en paramètre
        # Affichage
        self.midFrame.pack(side=TOP, fill=Y)
        self.lbPeriode.pack(side = LEFT)
        self.listePeriode.pack(side=LEFT)
        self.lbCbJour.pack(side = LEFT)
        self.listeMode.pack(side=LEFT)

    "" # Marque pour que le repli de code fasse ce que je veux
    #############
    # Getters : #
    #############
    ""
    def getApplication(self):
        """
        Permet d'obtenir l'Application.
        @return Application.
        """
        return self.getZoneAffichage().getApplication()

    def getBoutonsChangementJours(self):
        """
        Retourne une liste des boutons de changement de jours, dans l'ordre
        <<, <, >, >>.
        @return les boutons de changements de jours dans l'ordre indiqué ci-dessus.
        """
        return [self.boutonBienAvant, self.boutonAvant, self.boutonApres, self.boutonBienApres]

    def getData(self):
        """
        Permet d'obtenir Data
        @return Data
        """
        return self.getApplication().getData()

    def getPeriodeActive(self):
        """
        Permet d'obtenir la période active
        @return <Période> période active
        """
        return self.getPeriodManager().getActivePeriode()

    def getPeriodManager(self):
        """
        Permet d'obtenir le PeriodManager
        @return PeriodManager
        """
        return self.getApplication().getPeriodManager()

    def getZoneAffichage(self):
        """
        Permet d'obtenir la ZoneAffichage.
        @return ZoneAffichage.
        """
        return self.master

    ""
    #############
    # Setters : #
    #############
    ""
    def configPossibiliteListe(self):
        """
        Permet de mettre des choix en fonction du nombre de jour dans le combobox
        """
        def dureeEnJour(nom): # Fonction qui retourne le nombre de jour
            if nom == "Période":
                return 42
            else:
                return int(self.getData()[nom.upper()]["Duree en jour"])

        periode = self.getPeriodeActive()
        nbJour = periode.getDuree().days

        listeValue = [] # liste des strings
        # On va chercher dans data les valeurs
        self.getData().readFile("duree")
        for duree in self.getData().sections():
            # Mais on ne rajoute pas la période tout de suite ("and")
            if nbJour >= int(self.getData()[duree]["Duree en jour"]):
                listeValue.append(self.getData()[duree]["nom"])

        # Et on setup la liste
        self.listeMode.config(value = listeValue)

    def configPossibiliteListePeriode(self):
        """
        Permet de mettre des choix en fonction des périodes
        """
        listeValue = [] # liste des strings
        for p in self.getPeriodManager().getPeriodes():
            listeValue.append(p.getNom())

        self.listePeriode.config(value = listeValue)

    def setModeListe(self, mode = None):
        """
        Permet de changer la valeur du combobox, sans altérer son état de lecture.
        @param mode = None: None si on met sur le dernier élément de la liste, ou un autre
        texte si on veut quelque chose en particulier.
        """
        etatActuel = self.listeMode.cget("state")
        self.listeMode.config(state = NORMAL)
        try:
            if mode is None and self.listeMode.get() not in self.listeMode.cget("values"):
                self.listeMode.set(self.listeMode.cget("values")[-1])
            elif mode is not None:
                self.listeMode.set(mode)
        finally:
            self.listeMode.config(state = etatActuel)

    def setPeriodeActiveForApp(self):
        """
        Méthode pour changer la période actuelle en passant par le combobox
        """
        self.getPeriodManager().setActivePeriodeWithName(self.listePeriode.get())

    def setPeriodeActiveInCombo(self):
        """
        Met la période active dans le combobox des périodes
        """
        self.listePeriode.set(self.getPeriodeActive().getNom())

    def setStateListe(self, state):
        """
        Permet de changer l'état du combobox, en étant certain que le mode ne
        soit pas un mode qui permette à l'utilisateur de le changer.
        """
        if state == NORMAL:
            state = "readonly"
        self.listeMode.config(state = state)

    def updateComboboxNbJour(self):
        """
        Fonction qui met à jour les possibilités du combobox et
        en plus remet l'affichage période s'il y était avant.
        """
        self.configPossibiliteListe()
        self.listeMode.event_generate("<<ComboboxSelected>>")

    def updateComboboxPeriode(self):
        """
        Fonction qui met à jour les possibilités du combobox et
        en plus remet l'affichage période s'il y était avant.
        """
        self.configPossibiliteListePeriode()
