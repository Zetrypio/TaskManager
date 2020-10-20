# -*- coding:utf-8 -*-
from .Periode import *
from .dialog.dateDialog import *
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame, Button as TkButton
from tkinter.messagebox import showerror
from tkinter.colorchooser import askcolor
import datetime

from util.widgets.ColorButton import *
from util.util import adaptDate

class PeriodAdder(Frame):
    """
    Classe permettant d'ajouter des périodes
    (widget de gauche de l'Application pour
    quand on est en mode édition de périodes).
    """
    def __init__(self, periodManager, master = None, **kwargs):
        """
        @param master : TaskEditor. (est en réalité aussi un éditeur de périodes =).
        @param **kwargs : options de configuration du Frame, voir Frame.config() et Frame.keys()
        """
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est une référence vers TaskEditor
        
        # Attributs normaux:
        self.periodManager = periodManager
        self.debut = datetime.date.today()
        self.fin   = datetime.date.today()

        # Widgets non référencés.
        Label(self, text="Nom :").grid(row = 0, column = 0, sticky="e")
        Label(self, text="De :").grid(row = 1, column = 0, sticky="e")
        Label(self, text="Durée :").grid(row = 1, column = 3, sticky="e")
        Label(self, text="À :").grid(row = 1, column = 5, sticky="e")
        
        # Widgets :
        # Nom :
        self.champNom         = Entry(self)
        # Début :
        self.champDebut       = Button(self, text = "Aujourd'hui", command = self.askDateDebut)
        # Fin :
        self.champFin         = Button(self, text = "Aujourd'hui", command = self.askDateFin)
        # Durée
        self.champJour        = Spinbox(self, from_ = 0, to=9999, increment = 1, width = 4, command = self.setAutoFin)
        
        # Autres :
        self.champDescription = Text(self, height = 3, width = 10, wrap = "word")
        self.boutonColor      = ColorButton(self)
        # Valider
        self.boutonValider    = Button(self, command = self.valider, text = "Ajouter")

        # Placement :
        # Ligne 0 :
        self.champNom         .grid(row = 0, column = 1, columnspan = 4, sticky ="ew")
        self.boutonColor      .grid(row = 0, column = 5, sticky="ew", padx = 2)
        self.boutonValider    .grid(row = 0, column = 6, columnspan = 2, sticky="ew")
        # Ligne 1 :
        self.champDebut       .grid(row = 1, column = 1, columnspan = 2)
        self.champJour        .grid(row = 1, column = 4)                 # Column 3 est pris par label "Durée :"
        self.champFin         .grid(row = 1, column = 6, columnspan = 2) # Column 5 est pris par label "À :"
        
        # Ligne 2 :
        self.champDescription .grid(row = 2, column = 0, columnspan = 8, sticky ="ew")

    "" # Marque pour le repli de code
    #############
    # Getters : #
    #############
    ""
    def askDateDebut(self):
        """
        Permet de demander à l'utilisateur une date de début pour la période, par l'intermédaire d'une boîte de dialogue usuelle.
        """
        # Pour un obscure raison, il faut appeler cette méthode :
        self.master.redessiner()

        # demande de la date
        date = askdate()
        self.setDebut(date)

    def askDateFin(self):
        """
        Permet de demander à l'utilisateur une date de fin pour la période, par l'intermédaire d'une boîte de dialogue usuelle.
        """
        # Pour un obscure raison, il faut appeler cette méthode :
        self.master.redessiner()

        # demande de la date
        date = askdate()
        self.setFin(date)

    def getApplication(self):
        """
        Getter pour l'application
        @return l'Application
        """
        return self.getTaskEditor().getApplication()

    def getData(self):
        """
        Getter pour le data
        @return <data>
        """
        return self.getApplication().getData()

    def getDuree(self):
        """
        Permet d'obtenir la durée de la nouvelle période à créer.
        """
        return self.fin - self.debut

    def getTaskEditor(self):
        """
        Getter pour le taskEditor
        @return <Taskeditor>
        """
        return self.master
    ""
    #############
    # Setters : #
    #############
    ""
    def autoSetDuree(self):
        """
        Permet de mettre automatiquement le widget de durée de la période vers
        la nouvelle valeur selon le début et la fin auparavant sélectionné.
        """
        ecart = self.getDuree()
        self.champJour.set(ecart.days)
        self.verifyDuree()

    def setDebut(self, value):
        """
        Méthode qui permet de mettre un début
        + config un joli texte (en accord avec les préférences) sur le bouton
        + verifyDuree
        @param value : <datetime.date> date a mettre en place
        """
        if value is not None:
            self.debut = value
        self.champDebut.config(text = adaptDate(self.getData(), value) if value is not None else "")
        self.autoSetDuree()

    def setFin(self, value):
        """
        Méthode qui permet de mettre une fin
        + config un joli texte (en accord avec les préférences) sur le bouton
        + verifyDuree
        @param value : <datetime.date> date a mettre en place
        """
        if value is not None:
            self.fin = value
        self.champFin.config(text = adaptDate(self.getData(), value) if value is not None else "")
        self.autoSetDuree()

    def setAutoFin(self):
        """
        Méthode qui permet de fixer la fin en éditant la durée
        """
        self.setFin(self.debut + datetime.timedelta(days = int(self.champJour.get())))

    def verifyDuree(self):
        """
        Méthode qui vérifie si la durée est correct
        """
        self.champJour.config(foreground = "#FF0000") if self.getDuree() < datetime.timedelta(0) else self.champJour.config(foreground = self.getApplication().getData().getPalette()["foreground"])

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def createPeriode(self):
        """
        Méthode pour créer la période qui correspond au champs qui ont été saisis par l'utilisateur.
        Ne rajoute pas la période dans le periodManager.
        Il est important de faire une méthode séparée, car elle est utilisée également sans la validation
        dans les cas des dialogues de modification/duplications de période.
        @return la période créée.
        """
        # Si il manque un champ, on ne valide pas
        if (not self.champNom.get().strip()
            or self.debut is None
            or self.fin is None):
            showerror("Erreur", "L'un des champs n'est pas rempli comme il faut ou est vide.")
            return

        # Récupération des champs :
        nom   = self.champNom.get().strip()
        debut = self.debut + datetime.timedelta()       # Faire une copie de la date
        fin   = self.fin  +  datetime.timedelta()       # Ici aussi
        if debut > fin:
            showerror("Durée incorrect", "Vous ne pouvez pas faire une période avec une durée négative")
            return
        desc  = self.champDescription.get("0.0", END)   # Du début jusqu'à la fin !
        color = self.boutonColor.get()

        # Création de la période :
        return Periode(self.periodManager, nom, debut, fin, desc, color)

    def valider(self):
        """
        Méthode exécutée quand on appuie sur le bouton validé, pour créer la nouvelle période et l'ajouter au PeriodManager.
        """
        periode = self.createPeriode()
        self.periodManager.ajouter(periode) if periode is not None else None


