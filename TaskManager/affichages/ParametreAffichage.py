# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

MOIS = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

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
        self.boutonBienAvant = Button(self, text="<<", command=lambda:master.envoyerChangementDebut("d"))
        self.boutonBienAvant.pack(side=LEFT, fill=Y)
        self.boutonAvant = Button(self, text="<", command=lambda:master.envoyerChangementDebut(-1))
        self.boutonAvant.pack(side=LEFT, fill=Y)    

        # Boutons après :
        self.boutonBienApres = Button(self, text=">>", command=lambda:master.envoyerChangementDebut("f"))
        self.boutonBienApres.pack(side=RIGHT, fill=Y)          
        self.boutonApres = Button(self, text=">", command=lambda:master.envoyerChangementDebut(1))
        self.boutonApres.pack(side=RIGHT, fill=Y)             

        ### Frame du milieu
        ## Config calendrier classique
        self.midFrame = Frame(self)
        # Label : de la période
        self.lbPeriode = Label(self.midFrame, text = "Periode :")
        # Combobox de quelle période :
        self.listePeriode = Combobox(self.midFrame, values=['Periode'], state= "readonly")
        self.listePeriode.set(self.listePeriode.cget("values")[-1])
        self.listePeriode.bind("<<ComboboxSelected>>",lambda e = None : self.setPeriodeActiveForApp())
        # Label : du combien de jour
        self.lbCbJour = Label(self.midFrame, text = "Montrer :")
        # Combobox de combien de jours :
        self.comboDuree = Combobox(self.midFrame, values=['Periode'], state= "readonly")
        self.comboDuree.set(self.comboDuree.cget("values")[-1])
        self.comboDuree.bind("<<ComboboxSelected>>",master.envoyerChangementNbJour) #passer par le maître et pas de parenthèses car on n'appelle pas la fonction, on la passe en paramètre
        # Affichage
        self.lbPeriode.pack(side = LEFT)
        self.listePeriode.pack(side=LEFT)
        self.lbCbJour.pack(side = LEFT)
        self.comboDuree.pack(side=LEFT)
        ## Config Calendrier des périodes
        self.midFramePeriode = Frame(self)
        self.comboMoisPeriode = Combobox(self.midFramePeriode, value = MOIS, state = "readonly")
        self.comboMoisPeriode.bind("<<ComboboxSelected>>",lambda e, MOIS=MOIS : master.envoyerChangementMois(MOIS.index(e.widget.get())))
        self.varAnnee = StringVar()
        self.lbAnnee = Label(self.midFramePeriode, textvariable = self.varAnnee)
        # Affichage
        self.comboMoisPeriode.pack(side=LEFT)
        self.lbAnnee.pack(side = LEFT)


        # Affichage
        self.midFrame.pack(side=TOP, fill=Y)

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
        nbJour = self.getZoneAffichage().getDonneeCalendrier().getLongueurPeriode().days

        listeValue = [] # liste des strings
        # On va chercher dans data les valeurs
        self.getData().readFile("duree")
        for duree in self.getData().sections():
            # Mais on ne rajoute pas la période tout de suite ("and")
            if nbJour >= int(self.getData()[duree]["Duree en jour"]):
                listeValue.append(self.getData()[duree]["nom"])

        # On trie la liste
        listeValue.sort(key = lambda v : dureeEnJour(v))
        # Et on setup la liste
        self.comboDuree.config(value = listeValue)

    def configPossibiliteListePeriode(self):
        """
        Permet de mettre des choix en fonction des périodes
        """
        listeValue = [] # liste des strings
        for p in self.getPeriodManager().getPeriodes():
            listeValue.append(p.getNom())

        self.listePeriode.config(value = listeValue)

    def setLabelAnnee(self, annee):
        """
        Permet de mettre a jour l'année a afficher
        """
        self.varAnnee.set(annee)

    def setModeListe(self, mode = None):
        """
        Permet de changer la valeur du combobox, sans altérer son état de lecture.
        @param mode = None: None si on met sur le dernier élément de la liste, ou un autre
        texte si on veut quelque chose en particulier.
        """
        etatActuel = self.comboDuree.cget("state")
        self.comboDuree.config(state = NORMAL)
        try:
            if mode is None and self.comboDuree.get() not in self.comboDuree.cget("values"):
                self.comboDuree.set(self.comboDuree.cget("values")[-1])
            elif mode is not None:
                self.comboDuree.set(mode)
        finally:
            self.comboDuree.config(state = etatActuel)

    def setPeriodeActiveForApp(self):
        """
        Méthode pour changer la période actuelle en passant par le combobox
        """
        self.getPeriodManager().setActivePeriodeWithName(self.listePeriode.get())

    def setStateListe(self, state):
        """
        Permet de changer l'état du combobox, en étant certain que le mode ne
        soit pas un mode qui permette à l'utilisateur de le changer.
        """
        if state == NORMAL:
            state = "readonly"
        self.comboDuree.config(state = state)

    def updateComboboxNbJour(self):
        """
        Fonction qui met à jour les possibilités du combobox et
        en plus remet l'affichage période s'il y était avant.
        """
        self.configPossibiliteListe()
        self.comboDuree.event_generate("<<ComboboxSelected>>")

    def updateComboboxPeriode(self):
        """
        Fonction qui met à jour les possibilités du combobox et
        en plus remet l'affichage période s'il y était avant.
        """
        self.configPossibiliteListePeriode()

    ""
    #################################
    # Méthodes liées aux périodes : #
    #################################
    ""
    def changeMoisCombobox(self, val):
        """
        Permet de mettre a jour le combobox en fonction du mois (quand on passe par les boutons
        @param val : <int> au format datetime, c'est à dire index de MOIS +1
        """
        self.comboMoisPeriode.set(MOIS[val-1])

    def setPeriodeMode(self, calendrierPeriode = False, month = None, year = None):
        """
        Méthode qui change les combobox en cours
        @param calendrierPeriode : <Bool> True -> on pack le frame avec combo des mois de l'année
                                          False -> on pack le frame avec le combo de la période actuelle + durée d'affichage
        @param month             : <int> indice du mois actuel, celui de base a afficher
        @param year              : <int> annee en cours d'affichage
        """
        if calendrierPeriode:
            self.midFrame.pack_forget()
            self.midFramePeriode.pack(side=TOP, fill=Y)
            self.comboMoisPeriode.set(MOIS[month-1])
            self.varAnnee.set(year)
        else:
            self.midFramePeriode.pack_forget()
            self.midFrame.pack(side=TOP, fill=Y)

        self.getZoneAffichage().getDonneeCalendrier().updateAffichage()

    def switchPeriode(self):
        """
        Méthode a appeler quand on doit charger une période
        """
        # On met à jour la liste des durée possible
        self.configPossibiliteListe()
        # On set le combo des périodes avec le nom de la période
        self.listePeriode.set(self.getPeriodeActive().getNom())

        # On affiche la période entière
        self.comboDuree.set("Période")
        self.comboDuree.event_generate("<<ComboboxSelected>>")

