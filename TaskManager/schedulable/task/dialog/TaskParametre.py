# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

import datetime

from ...task.Task import *
from util.widgets.ColorButton import *
from util.widgets.Dialog import *
from util.widgets.ttkcalendar import *

from .datetimeDialog import *

class TaskParametre(Notebook):
    """
    Notebook qui contient tous les paramètres de la tache
    fournis dans le constructeur.
    Permet aussi de changer ses attributs (à la tache)
    class
    """
    def __init__(self, master, task, **kw):
        """
        @param master : <tkinter.frame>
        @param task   : <Task> ceux qui sont à afficher
        """
        super().__init__(master, **kw)
        self.task = task

        # Variable modifiable
        self.varNom = StringVar()
        self.varPeriode = StringVar()
        #varCouleur = StringVar()
        # textDesc (je le met ici pour ne pas l'oublier)
        self.varDebut = "" # Initialisation, affectation après
        self.varFin = ""
        self.varDuree = None
        self.varJour = IntVar()
        self.varHour = IntVar()
        self.varMin = IntVar()
        self.varNbRep = IntVar()
        self.varRepTimedelta = None
        self.varRep = IntVar()
        self.varUnitRep = StringVar()
        self.varID = StringVar()
        self.varDone = BooleanVar()


        # Affectation des variables
        self.varNom.set(self.task.getNom())
        self.varPeriode.set(self.task.getPeriode().getNom())
        #varCouleur.set(self.task.getColor())
        # textDesc (je le met ici pour ne pas l'oublier)
        self.varDebut = self.task.getDebut()
        self.varFin = self.task.getFin()
        self.varDuree = self.task.getDuree()
        self.varJour.set(self.varDuree.days)
        self.varHour.set(self.varDuree.seconds//3600)
        self.varMin.set(self.varDuree.seconds//60%60)
        self.varNbRep.set(8)
        self.varRepTimedelta = self.task.getRep() if self.task.getRep() is not None else datetime.timedelta()
        self.varRep = self.varRepTimedelta.seconds//3600 if self.varRepTimedelta.days == 0 else self.varRepTimedelta.days
        if self.varRep == 0: # ici les heures valent 0
            self.varUnitRep.set("jours")
        elif self.varRepTimedelta.days == 0 and self.varRep != 0:
            self.varUnitRep.set("heures")
        elif self.varRepTimedelta.days % 7 == 0:
            self.varUnitRep.set("semaines")
        else:
            self.varUnitRep.set("jours")
        self.varID.set(self.task.getUniqueID())
        self.varDone.set(self.task.isDone())

        self.pageGeneral = Frame(self)
        self.pageAvancee = Frame(self)
        self.add(self.pageGeneral, text = "Général")
        self.add(self.pageAvancee, text = "Avancée")

        ## Attributs généraux
        self.frameGeneral = LabelFrame(self.pageGeneral, text = "Attributs généraux")
        self.lbNom        = Label(      self.frameGeneral, text = "Nom :")
        self.entryNom     = Entry(      self.frameGeneral, textvariable = self.varNom)
        self.lbPeriode    = Label(      self.frameGeneral, text = "Période :")
        self.comboPeriode = Combobox(   self.frameGeneral, textvariable = self.varPeriode, value = [p.getNom() for p in self.task.getApplication().getPeriodManager().getPeriodes()], state = "readonly")
        self.lbColor      = Label(      self.frameGeneral, text = "Couleur :")
        #colbut       = ColorButton(frameGeneral, bg = varCouleur.get())
        self.colbut       = ColorButton(self.frameGeneral, bg = self.task.getColor())
        self.lbDesc       = Label(      self.frameGeneral, text = "Description :")
        self.textDesc     = Text(       self.frameGeneral, wrap = "word", height = 3, width = 30)
        self.textDesc.insert(END, self.task.getDescription()) # Car on peut pas mettre de variable
        self.sep = Separator(           self.frameGeneral, orient = HORIZONTAL)
        self.lbDebut = Label(           self.frameGeneral, text = "Début :")
        self.btnDebut = Button(         self.frameGeneral, text = self.varDebut, command = self.askDebut)
        self.lbFin = Label(             self.frameGeneral, text = "Fin :")
        self.btnFin = Button(           self.frameGeneral, text = self.varFin, command = self.askFin)
        self.lbDuree = Label(           self.frameGeneral, text = "Durée :")
        # Duree
        self.frameDuree = Frame(        self.frameGeneral)
        self.sbJour = Spinbox(          self.frameDuree, from_ = 0, to=31, increment = 1, width = 4, command = self.autoSetFin, textvariable = self.varJour)
        self.lbJour = Label(            self.frameDuree, text = "jours")
        self.sbHour = Spinbox(          self.frameDuree, from_ = 0, to=23, increment = 1, width = 4, command = self.autoSetFin, textvariable = self.varHour)
        self.lbHour = Label(            self.frameDuree, text = "heures")
        self.sbMin = Spinbox(           self.frameDuree, from_ = 0, to=59, increment = 1, width = 4, command = self.autoSetFin, textvariable = self.varMin)
        self.lbMin= Label(              self.frameDuree, text = "minutes")
        # Répétition
        self.lbNbRep = Label(           self.frameGeneral, text = "Nombre de répétitions :")
        self.sbNbRep = Spinbox(         self.frameGeneral, from_ = -1, to = 100, increment = 1, width = 4, textvariable = self.varNbRep)
        self.lbRepet = Label(           self.frameGeneral, text = "Fréquence :")
        self.frameRepet = Frame(        self.frameGeneral)
        self.sbRep = Spinbox(           self.frameRepet, from_ = 1, to = 100, increment = 1, width = 4, textvariable = self.varRep)
        self.cbUnit = Combobox(         self.frameRepet, value = ["semaine", "jours", "heures"], textvariable = self.varUnitRep)

        ## Attributs avancés
        self.frameAdvanced = LabelFrame(self.pageAvancee, text = "Options avancées")
        self.lbId = Label(           self.frameAdvanced, text = "ID :")
        self.entryId = Entry(        self.frameAdvanced, textvariable = self.varID, state = DISABLED)
        self.lbSubtask = Label(      self.frameAdvanced, text = "Sous-tâches :")
        self.lbListSub = Label(      self.frameAdvanced, text = self.getListTask(self.task.getSubTasks()) if self.task.isContainer() else "Tache non conteneur", anchor = "nw")
        self.lbDepces = Label(       self.frameAdvanced, text = "Dépendances :")
        self.lbListDepces = Listbox( self.frameAdvanced, listvariable = self.getListTask(self.task.getDependances(), StringV = True), selectmode = "single", height = len(self.getListTask(self.task.getDependances(), StringV = True).get().split("\\")))
        self.btnSupprDepces = Button(self.frameAdvanced, text = "Supprimer", command = lambda : self.supprimeLien("depces"))
        self.lbDeptes = Label(       self.frameAdvanced, text = "Dépendantes :")
        self.lbListDeptes = Listbox( self.frameAdvanced, listvariable = self.getListTask(self.task.getDependantes(), StringV = True), selectmode = "single", height = len(self.getListTask(self.task.getDependantes(), StringV = True).get().split("\\")))
        self.btnSupprDeptes = Button(self.frameAdvanced, text = "Supprimer", command = lambda : self.supprimeLien("deptes"))
        self.lbDone = Label(         self.frameAdvanced, text = "Fait :")
        self.cbDone = Checkbutton(   self.frameAdvanced, variable = self.varDone)
        self.lbParent = Label(       self.frameAdvanced, text = "Parent :")
        self.lbResultParent = Label( self.frameAdvanced, text = self.task.getParent() if self.task.getParent() else "")




        ## Affichage
        # Général
        self.frameGeneral.pack(side = TOP, fill = BOTH, expand = YES)
        self.lbNom.grid(       row = 0, column = 0, sticky = "e" )
        self.entryNom.grid(    row = 0, column = 1, sticky = "we")
        self.lbPeriode.grid(   row = 1, column = 0, sticky = "e" )
        self.comboPeriode.grid(row = 1, column = 1, sticky = "we")
        self.lbColor.grid(     row = 2, column = 0, sticky = "e" )
        self.colbut.grid(      row = 2, column = 1)
        self.lbDesc.grid(      row = 3, column = 0, sticky = "e" )
        self.textDesc.grid(    row = 4, column = 0, sticky = "we", columnspan = 2)
        self.sep.grid(         row = 5, column = 0, sticky = "we", columnspan = 2, pady = 2)
        self.lbDebut.grid(     row = 6, column = 0, sticky = "e" )
        self.btnDebut.grid(    row = 6, column = 1, sticky = "we")
        self.lbFin.grid(       row = 7, column = 0, sticky = "e" )
        self.btnFin.grid(      row = 7, column = 1, sticky = "we")
        # Duree
        self.lbDuree.grid(     row = 8, column = 0, sticky = "e" )
        self.frameDuree.grid(  row = 8, column = 1, sticky = "we")
        self.sbJour.grid(      row = 0, column = 0)
        self.lbJour.grid(      row = 0, column = 1)
        self.sbHour.grid(      row = 0, column = 2)
        self.lbHour.grid(      row = 0, column = 3)
        self.sbMin.grid(       row = 0, column = 4)
        self.lbMin.grid(       row = 0, column = 5)
        self.lbNbRep.grid(     row = 9, column = 0, sticky = "e" )
        self.frameRepet.grid(  row = 9, column = 1, sticky = "we")
        self.sbRep.pack( side = LEFT, fill = BOTH)
        self.cbUnit.pack(side = LEFT, fill = BOTH, expand = YES)
        # Avancée
        self.frameAdvanced.pack(side = TOP, fill = BOTH, expand = YES)
        self.lbId.grid(          row = 0, column = 0, sticky = "e" )
        self.entryId.grid(       row = 0, column = 1, sticky = "we")
        self.lbSubtask.grid(     row = 1, column = 0, sticky = "e" )
        self.lbListSub.grid(     row = 1, column = 1, sticky = "w" )
        self.lbDepces.grid(      row = 2, column = 0, sticky = "ne")
        self.lbListDepces.grid(  row = 2, column = 1, sticky = "nswe", rowspan = 2)
        self.btnSupprDepces.grid(row = 3, column = 0, sticky = "e" )
        self.lbDeptes.grid(      row = 4, column = 0, sticky = "ne")
        self.lbListDeptes.grid(  row = 4, column = 1, sticky = "nswe", rowspan = 2)
        self.btnSupprDeptes.grid(row = 5, column = 0, sticky = "e" )
        self.lbDone.grid(        row = 6, column = 0, sticky = "e" )
        self.cbDone.grid(        row = 6, column = 1, sticky = "we")
        self.lbParent.grid(      row = 7, column = 0, sticky = "e" )
        self.lbResultParent.grid(row = 7, column = 1, sticky = "w" )

        # Config grid
        self.frameAdvanced.columnconfigure(1, weight = 1)

        self.autoSetDuree()

    def onClose(self):
        """
        On change tout ce qu'il faut
        """
        self.task.setNom(            self.varNom.get())
        self.task.setPeriodeWithName(self.varPeriode.get())
        #self.task.setColor(varCouleur.get())
        self.task.setColor(         self.colbut.get())
        self.task.setDescription(   self.textDesc.get("0.0", END))
        self.task.setDebut(         self.varDebut, change = "duree")
        self.task.setDuree(datetime.timedelta(days = self.varJour.get(), hours = self.varHour.get(), minutes = self.varMin.get()))
        #self.task.setRep # TODO
        self.task.setDone(          self.varDone.get())

        self.task.getApplication().getTaskEditor().redessiner()
        self.task.getApplication().getDonneeCalendrier().updateColor()
        return

    def askDebut(self):
        """
        Permet de demander le début de la tâche à l'utilisateur via boîte de dialogue usuelle.
        """
        ## demande de la date
        date = askdatetime(False)
        if date is None:
            return
        self.varDebut = date
        self.btnDebut.config(text = self.varDebut if self.varDebut is not None else "")
        self.autoSetDuree()

    def askFin(self):
        """
        Permet de demander la fin de la tâche à l'utilisateur via boîte de dialogue usuelle.
        """
        # demande de la date
        date = askdatetime(False)
        if date is None:
            return
        self.varFin = date
        self.btnFin.config(text = self.varFin if self.varFin is not None else "")
        self.autoSetDuree()

    def autoSetDuree(self):
        """
        Permet de mettre à jour les widgets de durée de tâche.
        """
        ecart = self.varFin - self.varDebut
        self.varJour.set(ecart.days)
        self.varHour.set(ecart.seconds//3600)
        self.varMin.set(ecart.seconds//60%60)

    def autoSetFin(self):
        """
        Fonction qui change automatiquement la fin si on change la durée
        """
        self.varFin = (self.varDebut + datetime.timedelta(days = self.varJour.get(), hours = self.varHour.get(), minutes = self.varMin.get()))
        self.btnFin.config(text = self.varFin)

    def getListTask(self, list, StringV = False):
        """
        Fonction qui retourne un texte avec toutes les taches de la liste
        @format : Task -- uniqueId (+\n)
        @param list : <list> de task
        @param StringV : <bool> doit-on retourner un stringVar de listbox ?
        @return <str>
        """
        text = ""
        for task in list:
            text += str(task) + "\n\tID : " + task.getUniqueID() + "\n\\"
        if not StringV:
            return text.replace("\\", "")
        else:
            sv = StringVar()
            text = text.replace("\n", "")
            sv.set(text.replace("\t", "   ").split("\\")[:-1])
            return sv

    def supprimeLien(self, mode):
        """
        Fonction qui supprime un lien
        @param mode : <str> sert a savoir si c'est dépendances ou dépendantes
        """
        def chercheTask(id):
            """
            Fonction embarquée qui recherche la tache lié à l'id
            Pour l'instant seule les task ont un UUID
            @param id : <str> id de la tache qu'on cherche
            @param p  : <periode> celle qui contient la tache
            @return <task> recherché, None si non trouvé
            """
            for t in self.task.getPeriode().getPrimitivesSchedulables():
                if isinstance(t, Task):
                    if id == t.getUniqueID():
                        return t
                    elif t.isContainer():
                        for st in t.getSubTasks():
                            if st.getUniqueID() == id:
                                return st
        if mode == "depces":
            t = self.lbListDepces.get(ACTIVE)
            id = t.split("ID")[-1]
            id = id[id.rfind(" ")+1:]
            depces = chercheTask(id)
            deptes = self.task
        elif mode == "deptes":
            t = self.lbListDeptes.get(ACTIVE)
            id = t.split("ID")[-1]
            id = id[id.rfind(" ")+1:]
            deptes = chercheTask(id)
            depces = self.task
        else:
            return
        # On retire la dépendances
        deptes.removeDependance(depces)
        # On met à jour l'affichage
        if mode == "depces":
            self.lbListDepces.config(listvariable = self.getListTask(task.getDependances(), StringV = True))
        elif mode == "deptes":
            self.lbListDeptes.config(listvariable = self.getListTask(task.getDependantes(), StringV = True))
