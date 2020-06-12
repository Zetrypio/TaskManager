# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label, Button as TkButton
from tkinter.colorchooser import askcolor
import datetime
import time

from affichages.periode.Periode import *
from .dialog.datetimeDialog import *
from .Task import *

class TaskAdder(Frame):
    """
    Classe permettant d'ajouter des tâches (widget de gauche de l'Application).
    """
    def __init__(self, master = None, menubar = None, **kwargs):
        """
        Constructeur du TaskAdder.
        @param master : TaskEditor.
        @param menubar : MenuBar.
        @param **kwargs : options de configuration du Frame, voir Frame.config() et Frame.keys()
        """
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est une référence vers TaskEditor

        self.menu = menubar

        # Attributs normaux:
        date = time.localtime()
        self.debut = None # datetime.datetime(date.tm_year, date.tm_mon, date.tm_mday)
        self.fin = datetime.datetime(date.tm_year, date.tm_mon, date.tm_mday)
        del date

        # Widgets non référencés.
        Label(self, text="Nom :").grid(row = 0, column = 0, sticky="e")
        Label(self, text="De :").grid(row = 1, column = 0, sticky="e")
        Label(self, text="À :").grid(row = 1, column = 6, sticky="e")
        Label(self, text="Répétitions :").grid(row = 2, column = 0, columnspan = 2, sticky = "e")
        Label(self, text="répétitions tout les").grid(row = 2, column = 3, columnspan = 2)
        Label(self, text="Période :").grid(row = 3, column = 0, columnspan = 2, sticky = "e")

        # Widgets :
        # Nom :
        self.champNom           = Entry(self)
        # Début :
        self.champDebut         = Button(self, command = self.askDateDebut)
        # Fin :
        self.champFin           = Button(self, command = self.askDateFin)
        # Durée
        self.champJour          = Spinbox(self, from_ = 0, to=31, increment = 1, width = 4)
        self.champHeure         = Spinbox(self, from_ = 0, to=23, increment = 1, width = 4)
        self.champMinute        = Spinbox(self, from_ = 0, to=59, increment = 1, width = 4)
        # Répétitions :
        self.champNbRepetition  = Spinbox(self, from_ = -1, to=100, increment = 1, width = 4) # Nombre de répétition
        self.champRepetition    = Spinbox(self, from_ = 1, to=100, increment = 1, width = 4) # quantitée d'unitée de temps entre 2 répétition.
        self.champUniteeRepet   = Combobox(self, values = ["minutes", "heures", "jours", "semaines", "mois", "années"], state = "readonly", width = 4)
        # valeurs par défaut :
        self.champNbRepetition.set(0)
        self.champRepetition.set(1)
        self.champUniteeRepet.set(self.champUniteeRepet.cget("values")[2])
        # Période :
        self.champPeriode       = Combobox(self, state = "readonly")
        self.updatePossiblePeriods()
        # Autres :
        self.champDescription   = Text(self, height = 3, width = 10, wrap = "word")
        self.boutonColor        = TkButton(self, command = self.askcolor, width = 4, relief = GROOVE, bg = "white", activebackground = "white")
        # Valider
        self.boutonValider      =   Button(self, command = self.valider, text = "Ajouter")

        # Placements :
        # Ligne 0 :
        self.champNom         .grid(row = 0, column = 1, columnspan = 4, sticky ="ew")
        self.boutonColor      .grid(row = 0, column = 5, sticky="ew", padx = 2)
        self.boutonValider    .grid(row = 0, column = 6, columnspan = 2, sticky="ew")
        # Ligne 1 :
        self.champDebut       .grid(row = 1, column = 1, columnspan = 2)
        self.champJour        .grid(row = 1, column = 3)
        self.champHeure       .grid(row = 1, column = 4)
        self.champMinute      .grid(row = 1, column = 5)
        self.champFin         .grid(row = 1, column = 7) # Column 6 est pris par label "À :"
        # Ligne 2 :
        self.champNbRepetition.grid(row = 2, column = 2, sticky = "ew")
        self.champRepetition  .grid(row = 2, column = 5, sticky = "ew")
        self.champUniteeRepet .grid(row = 2, column = 6, sticky = "ew", columnspan = 2)
        # Ligne 3 :
        self.champPeriode     .grid(row = 3, column = 2, columnspan = 6, sticky = "ew")
        # Ligne 4 :
        self.champDescription .grid(row = 4, column = 0, columnspan = 8, sticky ="ew")

    def askcolor(self):
        """
        Permet de demander une couleur à l'utilisateur via boîte de dialogue usuelle.
        """
        self.color = askcolor()[1]
        self.boutonColor.config(bg = self.color, activebackground = self.color)

    def askDateDebut(self):
        """
        Permet de demander le début de la tâche à l'utilisateur via boîte de dialogue usuelle.
        """
        # Pour un obscure raison, il faut appeler cette méthode :
        self.master.redessiner()

        # demande de la date
        date = askdatetime(self.menu.variableHorlogeStyle.get())
        self.debut = date
        self.champDebut.config(text = date if date is not None else "")
        self.autoSetDuree()
        self.updatePossiblePeriods()

    def askDateFin(self):
        """
        Permet de demander la fin de la tâche à l'utilisateur via boîte de dialogue usuelle.
        """
        # Pour un obscure raison, il faut appeler cette méthode :
        self.master.redessiner()

        # demande de la date
        date = askdatetime(self.menu.variableHorlogeStyle.get())
        if date is not None:
            self.fin = date
        self.champFin.config(text = date if date is not None else "")
        self.autoSetDuree()
        self.updatePossiblePeriods()

    def getDebut(self):
        """
        Permet d'obtenir le début déjà choisi par l'utilisateur.
        @return le début de la tâche à créer.
        """
        return (self.debut + datetime.timedelta()) if self.debut is not None else None

    def getDuree(self):
        """
        Permet d'obtenir la durée calculée selon le début et la fin.
        @return la durée de la tâche à créer.
        """
        ecart = self.fin - (self.debut if self.debut is not None else self.fin)
        return ecart

    def getFin(self):
        """
        Permet d'obtenir la fin déjà choisie par l'utilisateur.
        @return la fin de la tâche à créer.
        """
        return (self.fin + datetime.timedelta()) if self.fin is not None else None

    def autoSetDuree(self):
        """
        Permet de mettre à jour les widgets de durée de tâche.
        """
        ecart = self.getDuree()
        self.champJour.set(ecart.days)
        self.champHeure.set(ecart.seconds//3600)
        self.champMinute.set(ecart.seconds//60%60)

    def getRepetitionTime(self):
        """
        Permet d'obtenir les informations de répétition.
        @return val, unit : val est tout les combien d'unit on répète.
        """
        unit = self.champUniteeRepet.get()
        val = int(self.champRepetition.get())
        return val, unit

    def updatePossiblePeriods(self):
        """
        Méthode à appeler dès que les périodes possibles changent.
        """
        periodes = self.getApplication().getPeriodManager().getPeriodes()
#        print(periodes)
        # Trouver les périodes présentes dans la plage sélectionnée :
        if self.debut is not None and self.fin is not None:
            pp = Periode(self.getApplication().getPeriodManager(), "", self.getDebut().date(), self.getFin().date(), "")
            periodes = [p.nom for p in periodes if p.intersectWith(pp)]
        else:
            periodes = []
        # Changer le combobox :
        self.champPeriode.config(values = ["(Aucune)"]+periodes)
        if self.getApplication().getPeriodManager().getActivePeriode() in periodes:
            self.champPeriode.set(self.getApplication().getPeriodManager().getActivePeriode().nom)
        elif periodes:
            self.champPeriode.set(self.champPeriode.cget("values")[1])
        else:
            self.champPeriode.set("(Aucune)")

    def valider(self):
        """
        Méthode quand on valide la création d'une tâche.
        @return la nouvelle tâche juste créée.
        """
        nom = self.champNom.get()
        debut = self.getDebut()
        duree = self.getDuree()
        rep   = self.getRepetitionTime()
        nbrep = int(self.champNbRepetition.get())
        desc  = self.champDescription.get("0.0", END)
        color = self.boutonColor.cget("bg")
        periode = None
        for p in self.getApplication().getPeriodManager().getPeriodes():
            if p.nom == self.champPeriode.get():
                periode = p
        self.master.ajouter(Task(nom, periode, desc, color, debut, duree, rep, nbrep))

    def getApplication(self):
        """
        Getter pour l'application.
        @return l'Application.
        """
        return self.master.getApplication()
