# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label, Button as TkButton
from tkinter.colorchooser import askcolor
import datetime
import time

from .dialog.datetimeDialog import *
from .Task import *

class TaskAdder(Frame):
    """Classe permettant d'ajouter des tâches (widget de gauche de l'Application)."""
    def __init__(self, master = None, menubar = None, **kwargs):
        """
        master : TaskEditor.
        menubar : MenuBar.
        **kwargs : options de configuration du Frame, voir Frame.config() et Frame.keys()
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

        # Widgets :
        # Nom :
        self.champNom           = Entry(self)
        # Debut :
        self.champDebut         = Button(self, command = self.askDateDebut)
        # Fin :
        self.champFin           = Button(self, command = self.askDateFin)
        # Duree
        self.champJour          = Spinbox(self, from_ = 0, to=31, increment = 1, width = 4)
        self.champHeure         = Spinbox(self, from_ = 0, to=23, increment = 1, width = 4)
        self.champMinute        = Spinbox(self, from_ = 0, to=59, increment = 1, width = 4)
        # Répétitions :
        self.champNbRepetition  = Spinbox(self, from_ = -1, to=100, increment = 1, width = 4) # Nombre de répétition
        self.champRepetition    = Spinbox(self, from_ = 1, to=100, increment = 1, width = 4) # quantit�e d'unitée de temps entre 2 rép.
        self.champUniteeRepet   = Combobox(self, values = ["minutes", "heures", "jours", "semaines", "mois", "ann�es"], state = "readonly", width = 4)
        # valeurs par défaut :
        self.champNbRepetition.set(0)
        self.champRepetition.set(1)
        self.champUniteeRepet.set(self.champUniteeRepet.cget("values")[2])
        # Autres :
        self.champDescription   = Text(self, height = 3, width = 10, wrap = "word")
        self.boutonColor        = TkButton(self, command = self.askcolor, width = 4, relief = GROOVE, bg = "white", activebackground = "white")
        # Valider
        self.boutonValider      =   Button(self, command = self.valider, text = "Ajouter")

        # Placement :
        # Ligne 0 :
        self.champNom         .grid(row = 0, column = 1, columnspan = 4, sticky ="ew")
        self.boutonColor      .grid(row = 0, column = 5, sticky="ew", padx = 2)
        self.boutonValider    .grid(row = 0, column = 6, columnspan = 2, sticky="ew")
        # Ligne 1 :
        self.champDebut       .grid(row = 1, column = 1, columnspan = 2)
        self.champJour        .grid(row = 1, column = 3)
        self.champHeure       .grid(row = 1, column = 4)
        self.champMinute      .grid(row = 1, column = 5)
        self.champFin         .grid(row = 1, column = 7) # Column 6 est pris par label "� :"
        # Ligne 2 :
        self.champNbRepetition.grid(row = 2, column = 2, sticky = "ew")
        self.champRepetition  .grid(row = 2, column = 5, sticky = "ew")
        self.champUniteeRepet .grid(row = 2, column = 6, sticky = "ew", columnspan = 2)
        # Ligne 3 :
        self.champDescription .grid(row = 3, column = 0, columnspan = 8, sticky ="ew")

    def askcolor(self):
        self.color = askcolor()[1]
        self.boutonColor.config(bg = self.color, activebackground = self.color)

    def askDateDebut(self):
        # Pour un obscure raison, il faut appeler cette méthode :
        self.master.redessiner()

        # demande de la date
        date = askdatetime(self.menu.variableHorlogeStyle.get())
        self.debut = date
        self.champDebut.config(text = date if date is not None else "")
        self.autoSetDuree()

    def askDateFin(self):
        # Pour un obscure raison, il faut appeler cette méthode :
        self.master.redessiner()

        # demande de la date
        date = askdatetime(self.menu.variableHorlogeStyle.get())
        if date is not None:
            self.fin = date
        self.champFin.config(text = date if date is not None else "")
        self.autoSetDuree()

    def getDuree(self):
        ecart = self.fin - (self.debut if self.debut is not None else self.fin)
        return ecart

    def autoSetDuree(self):
        ecart = self.getDuree()
        self.champJour.set(ecart.days)
        self.champHeure.set(ecart.seconds//3600)
        self.champMinute.set(ecart.seconds//60%60)

    def getRepetitionTime(self):
        unit = self.champUniteeRepet.get()
        val = int(self.champRepetition.get())
        return val, unit

    def valider(self):
        nom = self.champNom.get()
        if self.debut is not None:
            debut = self.debut+datetime.timedelta() # Faire une copie de la date
        else:
            debut = None
        duree = self.getDuree()
        rep   = self.getRepetitionTime()
        nbrep = int(self.champNbRepetition.get())
        desc  = self.champDescription.get("0.0", END)
        color = self.boutonColor.cget("bg")
        periode  = self.getApplication().getPeriodManager().getActivePeriode()
        self.master.ajouter(Task(nom, debut, duree, rep, nbrep, desc, color, periode))

    def getApplication(self):
        return self.master.getApplication()
