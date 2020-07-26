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
        self.champNom           = Entry(self)
        # Début :
        self.champDebut         = Button(self, command = self.askDateDebut)
        # Fin :
        self.champFin           = Button(self, command = self.askDateFin)
        # Durée
        self.champJour          = Spinbox(self, from_ = 0, to=9999, increment = 1, width = 4)
        
        # Autres :
        self.champDescription   = Text(self, height = 3, width = 10, wrap = "word")
        self.boutonColor        = ColorButton(self)
        # Valider
        self.boutonValider      =   Button(self, command = self.valider, text = "Ajouter")

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
        if date is not None:
            self.debut = date
        self.champDebut.config(text = date)
        self.autoSetDuree()

    def askDateFin(self):
        """
        Permet de demander à l'utilisateur une date de fin pour la période, par l'intermédaire d'une boîte de dialogue usuelle.
        """
        # Pour un obscure raison, il faut appeler cette méthode :
        self.master.redessiner()

        # demande de la date
        date = askdate()
        if date is not None:
            self.fin = date
        self.champFin.config(text = date)
        self.autoSetDuree()

    def getDuree(self):
        """
        Permet d'obtenir la durée de la nouvelle période à créer.
        """
        return self.fin - self.debut

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

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def valider(self):
        """
        Méthode exécutée quand on appuie sur le bouton validé, pour créer la nouvelle période et l'ajouter au PeriodManager.
        """
        # Si il manque un champ, on ne valide pas
        if (not self.champNom.get().strip()
            or self.debut is None
            or self.fin is None):
            showerror("Erreur", "L'un des champs n'est pas rempli comme il faut ou est vide.")
            return
        nom   = self.champNom.get().strip()
        debut = self.debut + datetime.timedelta() # Faire une copie de la date
        fin   = self.fin  +  datetime.timedelta() # Ici aussi
        desc  = self.champDescription.get("0.0", END) # Du début jusqu'à la fin !
        color = self.boutonColor.get()
        
        # Création de la période :
        periode = Periode(self.periodManager, nom, debut, fin, desc, color)
        self.periodManager.ajouter(periode)
        #self.master.ajouter(periode) # TODO
