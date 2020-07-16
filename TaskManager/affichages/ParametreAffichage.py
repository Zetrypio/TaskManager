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

        # Combobox de combien de jours :
        self.listeMode = Combobox(self, values=['Periode'], state= "readonly")
        self.listeMode.set(self.listeMode.cget("values")[-1])
        self.listeMode.bind("<<ComboboxSelected>>",master.envoyerChangementNbJour) #passer par le maître et pas de parenthèses car on n'appelle pas la fonction, on la passe en paramètre
        self.listeMode.pack(side=TOP, fill=Y)
    
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
    
    def configPossibiliteListe(self):
        """
        Permet de mettre des choix en fonction du nombre de jour dans le combobox
        """
        periode = self.getZoneAffichage().getDonneeCalendrier().getPeriodeActive()
        nbJour = periode.getDuree().days
        listeValue = []
        print("DATA :", self.getApplication().getData().sections())
        if nbJour >= 1:
            listeValue.append('1 jour')
        if nbJour >= 2:
            listeValue.append('2 jours')
        if nbJour >= 5:
            listeValue.append('5 jours')
        if nbJour >= 7:
            listeValue.append('1 semaine')

        listeValue.append("Période")

        self.listeMode.config(value= listeValue)

    def updateCombobox(self):
        """
        Fonction qui met à jour les possibilités du combobox et
        en plus remet l'affichage période s'il y était avant.
        """
        self.configPossibiliteListe()
        self.listeMode.event_generate("<<ComboboxSelected>>")

    def setStateListe(self, state):
        """
        Permet de changer l'état du combobox, en étant certain que le mode ne
        soit pas un mode qui permette à l'utilisateur de le changer.
        """
        if state == NORMAL:
            state = "readonly"
        self.listeMode.config(state = state)
        
    def getBoutonsChangementJours(self):
        """
        Retourne une liste des boutons de changement de jours, dans l'ordre
        <<, <, >, >>.
        @return les boutons de changements de jours dans l'ordre indiqué ci-dessus.
        """
        return [self.boutonBienAvant, self.boutonAvant, self.boutonApres, self.boutonBienApres]

    def getZoneAffichage(self):
        """
        Permet d'obtenir la ZoneAffichage.
        @return ZoneAffichage.
        """
        return self.master

    def getApplication(self):
        """
        Permet d'obtenir l'Application.
        @return Application.
        """
        return self.getZoneAffichage().getApplication()

    
