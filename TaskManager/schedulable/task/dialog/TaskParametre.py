# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

import datetime

from util.widgets.ColorButton import *
from util.widgets.ttkcalendar import *
from ...AbstractSchedulableParametre import *

from .datetimeDialog import *

class TaskParametre(AbstractSchedulableParametre):
    """
    Notebook qui contient tous les paramètres de la tache
    fournis dans le constructeur.
    Permet aussi de changer ses attributs (à la tache)
    """
    def __init__(self, master, task, **kw):
        """
        @param master : <tkinter.frame>
        @param task   : <Task> ceux qui sont à afficher
        """
        super().__init__(master, task, **kw)

        if task.getParent():
            # page du parent
            self.__frameSchedu = TaskParametre(self, task.getParent())
            super().add(self.__frameSchedu, text = "Parent")

        # Variable modifiable
        """ Géré par le parent
        self.varNom = StringVar()
        self.varPeriode = StringVar()
        #varCouleur = StringVar()
        # textDesc (je le met ici pour ne pas l'oublier)"""
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
        self.varDebut = self._getSchedulable().getDebut()
        self.varFin = self._getSchedulable().getFin()
        self.varDuree = self._getSchedulable().getDuree()
        self.varJour.set(self.varDuree.days)
        self.varHour.set(self.varDuree.seconds//3600)
        self.varMin.set(self.varDuree.seconds//60%60)
        self.varNbRep.set(8)
        self.varRepTimedelta = self._getSchedulable().getRep() if self._getSchedulable().getRep() is not None else datetime.timedelta()
        self.varRep = self.varRepTimedelta.seconds//3600 if self.varRepTimedelta.days == 0 else self.varRepTimedelta.days
        if self.varRep == 0: # ici les heures valent 0
            self.varUnitRep.set("jours")
        elif self.varRepTimedelta.days == 0 and self.varRep != 0:
            self.varUnitRep.set("heures")
        elif self.varRepTimedelta.days % 7 == 0:
            self.varUnitRep.set("semaines")
        else:
            self.varUnitRep.set("jours")
        self.varID.set(self._getSchedulable().getUniqueID())
        self.varDone.set(self._getSchedulable().isDone())


        ## Attributs généraux
        self.lbDebut = Label(           self._frameGeneral, text = "Début :")
        self.btnDebut = Button(         self._frameGeneral, text = self.varDebut, command = self.__askDebut)
        self.lbFin = Label(             self._frameGeneral, text = "Fin :")
        self.btnFin = Button(           self._frameGeneral, text = self.varFin, command = self.__askFin)
        self.lbDuree = Label(           self._frameGeneral, text = "Durée :")
        # Duree
        self.frameDuree = Frame(        self._frameGeneral)
        self.sbJour = Spinbox(          self.frameDuree, from_ = 0, to=31, increment = 1, width = 4, command = self.__autoSetFin, textvariable = self.varJour)
        self.lbJour = Label(            self.frameDuree, text = "jours")
        self.sbHour = Spinbox(          self.frameDuree, from_ = 0, to=23, increment = 1, width = 4, command = self.__autoSetFin, textvariable = self.varHour)
        self.lbHour = Label(            self.frameDuree, text = "heures")
        self.sbMin = Spinbox(           self.frameDuree, from_ = 0, to=59, increment = 1, width = 4, command = self.__autoSetFin, textvariable = self.varMin)
        self.lbMin= Label(              self.frameDuree, text = "minutes")
        # Répétition
        self.lbNbRep = Label(           self._frameGeneral, text = "Nombre de répétitions :")
        self.sbNbRep = Spinbox(         self._frameGeneral, from_ = -1, to = 100, increment = 1, width = 4, textvariable = self.varNbRep)
        self.lbRepet = Label(           self._frameGeneral, text = "Fréquence :")
        self.frameRepet = Frame(        self._frameGeneral)
        self.sbRep = Spinbox(           self.frameRepet, from_ = 1, to = 100, increment = 1, width = 4, textvariable = self.varRep)
        self.cbUnit = Combobox(         self.frameRepet, value = ["semaine", "jours", "heures"], textvariable = self.varUnitRep)

        ## Attributs avancés
        # (voir parent) self._frameAdvanced = LabelFrame(self._pageAvancee, text = "Options avancées")
        self.lbId = Label(           self._frameAdvanced, text = "ID :")
        self.entryId = Entry(        self._frameAdvanced, textvariable = self.varID, state = DISABLED)
        self.lbSubtask = Label(      self._frameAdvanced, text = "Sous-tâches :")
        self.lbListSub = Label(      self._frameAdvanced, text = self.__getListTask(self._getSchedulable().getSubTasks()) if self._getSchedulable().isContainer() else "Tache non conteneur", anchor = "nw")
        self.lbDepces = Label(       self._frameAdvanced, text = "Dépendances :")
        self.lbListDepces = Listbox( self._frameAdvanced, listvariable = self.__getListTask(self._getSchedulable().getDependances(), StringV = True), selectmode = "single", height = len(self._getSchedulable().getDependances()) if len(self._getSchedulable().getDependances()) > 0 else 1 )
        self.btnSupprDepces = Button(self._frameAdvanced, text = "Supprimer", command = lambda : self.__supprimeLien("depces"))
        self.lbDeptes = Label(       self._frameAdvanced, text = "Dépendantes :")
        self.lbListDeptes = Listbox( self._frameAdvanced, listvariable = self.__getListTask(self._getSchedulable().getDependantes(), StringV = True), selectmode = "single", height = len(self._getSchedulable().getDependantes()) if len(self._getSchedulable().getDependantes()) > 0 else 1 )
        self.btnSupprDeptes = Button(self._frameAdvanced, text = "Supprimer", command = lambda : self.__supprimeLien("deptes"))
        self.lbDone = Label(         self._frameAdvanced, text = "Fait :")
        self.cbDone = Checkbutton(   self._frameAdvanced, variable = self.varDone)
        self.lbParent = Label(       self._frameAdvanced, text = "Parent :")
        self.lbResultParent = Label( self._frameAdvanced, text = self._getSchedulable().getParent() if self._getSchedulable().getParent() else "")




        ## Affichage
        # Général
        # grid obligatoire
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
        # (voir parent) self._frameAdvanced.pack(side = TOP, fill = BOTH, expand = YES)
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
        self._frameAdvanced.columnconfigure(1, weight = 1)

        self.__autoSetDuree()

    def onClose(self):
        """
        On change tout ce qu'il faut
        """
        # Géré par le parent : nom, période, couleur, desc
        super().onClose()

        self._getSchedulable().setDebut(         self.varDebut, change = "duree")
        self._getSchedulable().setDuree(datetime.timedelta(days = self.varJour.get(), hours = self.varHour.get(), minutes = self.varMin.get()))
        #self._getSchedulable().setRep # TODO
        self._getSchedulable().setDone(          self.varDone.get())

        self._getSchedulable().getApplication().getTaskEditor().redessiner()
        self._getSchedulable().getApplication().getDonneeCalendrier().updateColor()
        return

    def __askDebut(self):
        """
        Permet de demander le début de la tâche à l'utilisateur via boîte de dialogue usuelle.
        """
        ## demande de la date
        date = askdatetime(False)
        if date is None:
            return
        self.varDebut = date
        self.btnDebut.config(text = self.varDebut if self.varDebut is not None else "")
        self.__autoSetDuree()

    def __askFin(self):
        """
        Permet de demander la fin de la tâche à l'utilisateur via boîte de dialogue usuelle.
        """
        # demande de la date
        date = askdatetime(False)
        if date is None:
            return
        self.varFin = date
        self.btnFin.config(text = self.varFin if self.varFin is not None else "")
        self.__autoSetDuree()

    def __autoSetDuree(self):
        """
        Permet de mettre à jour les widgets de durée de tâche.
        """
        try:
            ecart = self.varFin - self.varDebut
            self.varJour.set(ecart.days)
            self.varHour.set(ecart.seconds//3600)
            self.varMin.set(ecart.seconds//60%60)
        except:pass

    def __autoSetFin(self):
        """
        Fonction qui change automatiquement la fin si on change la durée
        """
        self.varFin = (self.varDebut + datetime.timedelta(days = self.varJour.get(), hours = self.varHour.get(), minutes = self.varMin.get()))
        self.btnFin.config(text = self.varFin)

    def __getListTask(self, list, StringV = False):
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

    def __supprimeLien(self, mode):
        """
        Fonction qui supprime un lien
        @param mode : <str> sert a savoir si c'est dépendances ou dépendantes
        """
        if mode == "depces":
            t = self.lbListDepces.get(ACTIVE)
            id = t.split("ID")[-1]
            id = id[id.rfind(" ")+1:]
            depces = self._getSchedulableWithID(id)
            deptes = self._getSchedulable()
        elif mode == "deptes":
            t = self.lbListDeptes.get(ACTIVE)
            id = t.split("ID")[-1]
            id = id[id.rfind(" ")+1:]
            deptes = self._getSchedulableWithID(id)
            depces = self._getSchedulable()
        else:
            return
        # On retire la dépendances
        deptes.removeDependance(depces)
        # On met à jour l'affichage
        if mode == "depces":
            self.lbListDepces.config(listvariable = self.__getListTask(self._getSchedulable().getDependances(), StringV = True))
        elif mode == "deptes":
            self.lbListDeptes.config(listvariable = self.__getListTask(self._getSchedulable().getDependantes(), StringV = True))
