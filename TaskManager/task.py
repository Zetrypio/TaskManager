# -*- coding:utf-8 -*-
from taskDnD import TaskInDnd
from datedialog import *
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame, Button as TkButton
from tkinter.colorchooser import *
import datetime # pour date, datetime, time et timedelta, il y a aussi timezone je crois.

class Task:
    """Classe définissant une tâche."""
    def __init__(self, nom, debut, duree, rep=-1, nbrep = 0, desc="", color="white"):
        """
        @param nom : nom de la tâche.
        @param debut : datetime. du début.
        @param duree : datetime.
        @param rep : répétition.
        @param nbrep : nombre de répétitions.
        @param desc : description.
        @param color: couleur avec un nom compatible avec les noms de couleurs tkinter.
        """
        self.nom = nom
        self.debut = debut
        self.duree = duree
        self.rep = rep      # répétition
        self.nbrep = nbrep  # nombre de répétitions
        self.desc = desc    # descirption
        self.color = color
        self.dependances = []
        self.dependantes = []
        self.updateStatut()
        if self.isContainer():
            self.subtasks = []
    def isContainer(self):
        self.updateStatut()
        if self.statut == "Inconnu" and not hasattr(self, "subtasks"):
            self.subtasks = []
        return self.statut == "Inconnu"
    def addSubTask(self, task):
        """Il est impératif de gérer la suppresion de la tâche dans TaskEditor depuis l'extérieur."""
        if not self.isContainer():
            raise ValueError("Impossible de rajouter une tâche dans une tâche non conteneur.")
        if task.isContainer():
            raise ValueError("Impossible de rajouter une tâche conteneur dans une autre tâche conteneur")
        self.subtasks.append(task)
    def getSubTasks(self):
        if not self.isContainer():
            raise ValueError("Impossible d'obtenir les sous-tâches d'une tâche non conteneur.")
        return self.subtasks
    def addDependance(self, task):
        self.dependances.append(task)
        task.dependantes.append(self)
    def removeDependance(self, task):
        self.dependances.remove(task)
        task.dependantes.remove(self)
    def copy(self):
        t = Task(self.nom, self.getDebut(), self.getDuree(), self.rep, self.nbrep, self.desc, self.color)
        # Doit-on copier les dépendances et le statut ?
        t.dependances = self.dependances[:]
        t.statut = self.statut
        # On retourne la copie :
        return t
    def updateStatut(self):
        """Permet de mettre à jour le statut de la tâche."""
        self.statut = "Inconnu" if self.debut == None else "À faire" if self.nbrep == 0 else "Répétition"
    def getDebut(self):
        return self.debut + datetime.timedelta() if self.debut is not None else None # Faire une copie et vérifier les trucs
    def getDuree(self):
        return self.duree + datetime.timedelta() # Faire une copie
    def getFin(self):
        return (self.debut + self.duree) if self.debut is not None else None

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
        self.debut = None# datetime.datetime(date.tm_year, date.tm_mon, date.tm_mday)
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
        self.champRepetition    = Spinbox(self, from_ = 1, to=100, increment = 1, width = 4) # quantitée d'unitée de temps entre 2 rép.
        self.champUniteeRepet   = Combobox(self, values = ["minutes", "heures", "jours", "semaines", "mois", "années"], state = "readonly", width = 4)
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
        self.champFin         .grid(row = 1, column = 7) # Column 6 est pris par label "À :"
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
        date = askdate(self.menu.variableHorlogeStyle.get())
        self.debut = date
        self.champDebut.config(text = date if date is not None else "")
        self.autoSetDuree()

    def askDateFin(self):
        # Pour un obscure raison, il faut appeler cette méthode :
        self.master.redessiner()

        # demande de la date
        date = askdate(self.menu.variableHorlogeStyle.get())
        if date is not None:
            self.fin = date
        self.champFin.config(text = date if date is not None else "")
        self.autoSetDuree()

    def getDuree(self):
        print(self.debut, self.fin)
        ecart = self.fin - (self.debut if self.debut is not None else self.fin)
        print(ecart)
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
        self.master.ajouter(Task(nom, debut, duree, rep, nbrep, desc, color))



if __name__=='__main__':
    import Application
    Application.main()
