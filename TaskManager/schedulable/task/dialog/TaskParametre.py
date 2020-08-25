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
        if not self._getSchedulable().isContainer():
            self.__varDebut    = "" # Initialisation, affectation après
            self.__varFin      = ""
            self.__varDuree    = None
            self.__varJour     = IntVar()
            self.__varHour     = IntVar()
            self.__varMin      = IntVar()
        self.__varNbRep        = IntVar()
        self.__varRepTimedelta = None
        self.__varRep          = IntVar()
        self.__varUnitRep      = StringVar()
        self.__varDone         = BooleanVar()
        self.__varGroupe       = StringVar()


        # Affectation des variables
        if not self._getSchedulable().isContainer():
            self.__varDebut    = self._getSchedulable().getDebut()
            self.__varFin      = self._getSchedulable().getFin()
            self.__varDuree    = self._getSchedulable().getDuree()
            self.__varJour.set(  self.__varDuree.days)
            self.__varHour.set(  self.__varDuree.seconds//3600)
            self.__varMin.set(   self.__varDuree.seconds//60%60)
        self.__varNbRep.set(     self._getSchedulable().getNbRep())
        self.__varRepTimedelta = self._getSchedulable().getRep() if self._getSchedulable().getRep() is not None else datetime.timedelta()
        self.__varRep          = self.varRepTimedelta.seconds//3600 if self.__varRepTimedelta.days == 0 else self.__varRepTimedelta.days
        self.__varDone.set(      self._getSchedulable().isDone())
        if self.__varRep == 0: # ici les heures valent 0
            self.__varUnitRep.set("jours")
        elif self.__varRepTimedelta.days == 0 and self.__varRep != 0:
            self.__varUnitRep.set("heures")
        elif self.__varRepTimedelta.days % 7 == 0:
            self.__varUnitRep.set("semaines")
        else:
            self.__varUnitRep.set("jours")
        self.__varGroupe.set(    str(self._getSchedulable().getGroupe()) + "   ID : " +self._getSchedulable().getGroupe().getUniqueID()) if self._getSchedulable().hasGroupe() else self.__varGroupe.set("N'est pas dans un groupe")


        ## Attributs généraux
        if not self._getSchedulable().isContainer():
            self.__lbDebut =    Label( self._frameGeneral, text = "Début :")
            self.__btnDebut =   Button(self._frameGeneral, text = self.__varDebut, command = self.__askDebut)
            self.__lbFin =      Label( self._frameGeneral, text = "Fin :"  )
            self.__btnFin =     Button(self._frameGeneral, text = self.__varFin,   command = self.__askFin)
            self.__lbDuree =    Label( self._frameGeneral, text = "Durée :")
            # Duree
            self.__frameDuree = Frame(    self._frameGeneral)
            self.__sbJour =     Spinbox(  self.__frameDuree, from_ = 0, to=31, increment = 1, width = 4, command = self.__autoSetFin, textvariable = self.__varJour)
            self.__lbJour =     Label(    self.__frameDuree, text = "jours")
            self.__sbHour =     Spinbox(  self.__frameDuree, from_ = 0, to=23, increment = 1, width = 4, command = self.__autoSetFin, textvariable = self.__varHour)
            self.__lbHour =     Label(    self.__frameDuree, text = "heures")
            self.__sbMin =      Spinbox(  self.__frameDuree, from_ = 0, to=59, increment = 1, width = 4, command = self.__autoSetFin, textvariable = self.__varMin)
            self.__lbMin =      Label(    self.__frameDuree, text = "minutes")
        # Répétition
        self.__lbNbRep =    Label(   self._frameGeneral, text = "Nombre de répétitions :")
        self.__sbNbRep =    Spinbox( self._frameGeneral, from_ = -1, to = 100, increment = 1, width = 4, textvariable = self.__varNbRep)
        self.__lbRepet =    Label(   self._frameGeneral, text = "tout les :")
        self.__frameRepet = Frame(   self._frameGeneral)
        self.__sbRep =      Spinbox( self.__frameRepet, from_ = 1, to = 100, increment = 1, width = 4, textvariable = self.__varRep)
        self.__cbUnit =     Combobox(self.__frameRepet, value = ["semaine", "jours", "heures"], textvariable = self.__varUnitRep)

        ## Attributs avancés
        # (voir parent) self._frameAdvanced = LabelFrame(self._pageAvancee, text = "Options avancées")
        self.__lbSubtask =      Label(      self._frameAdvanced, text = "Sous-tâches :")
        self.__lbListSub =      Label(      self._frameAdvanced, text = self.__getListTask(self._getSchedulable().getSubTasks()) if self._getSchedulable().isContainer() else "Tache non conteneur", anchor = "nw")
        self.__lbDepces =       Label(      self._frameAdvanced, text = "Dépendances :")
        self.__lbListDepces =   Listbox(    self._frameAdvanced, listvariable = self.__getListTask(self._getSchedulable().getDependances(), StringV = True), selectmode = "single", height = len(self._getSchedulable().getDependances()) if len(self._getSchedulable().getDependances()) > 0 else 1 )
        self.__btnSupprDepces = Button(     self._frameAdvanced, text = "Supprimer", command = lambda : self.__supprimeLien("depces"))
        self.__lbDeptes =       Label(      self._frameAdvanced, text = "Dépendantes :")
        self.__lbListDeptes =   Listbox(    self._frameAdvanced, listvariable = self.__getListTask(self._getSchedulable().getDependantes(), StringV = True), selectmode = "single", height = len(self._getSchedulable().getDependantes()) if len(self._getSchedulable().getDependantes()) > 0 else 1 )
        self.__btnSupprDeptes = Button(     self._frameAdvanced, text = "Supprimer", command = lambda : self.__supprimeLien("deptes"))
        self.__lbDone =         Label(      self._frameAdvanced, text = "Fait :")
        self.__cbDone =         Checkbutton(self._frameAdvanced, variable = self.__varDone)
        self.__lbParent =       Label(      self._frameAdvanced, text = "Parent :")
        self.__lbResultParent = Label(      self._frameAdvanced, text = self._getSchedulable().getParent() if self._getSchedulable().getParent() else "")
        self.__lbGroupe =       Label(      self._frameAdvanced, text = "Groupe :")
        self.__lbResultGroupe = Label(      self._frameAdvanced, text = self.__varGroupe.get())




        ## Affichage
        # Général
        # grid obligatoire
        if not self._getSchedulable().isContainer():
            self.__lbDebut.grid(   row = 6,  column = 0, sticky = "e" )
            self.__btnDebut.grid(  row = 6,  column = 1, sticky = "we")
            self.__lbFin.grid(     row = 7,  column = 0, sticky = "e" )
            self.__btnFin.grid(    row = 7,  column = 1, sticky = "we")
            # Duree
            self.__lbDuree.grid(   row = 8,  column = 0, sticky = "e" )
            self.__frameDuree.grid(row = 8,  column = 1, sticky = "we")
            self.__sbJour.grid(    row = 0,  column = 0)
            self.__lbJour.grid(    row = 0,  column = 1)
            self.__sbHour.grid(    row = 0,  column = 2)
            self.__lbHour.grid(    row = 0,  column = 3)
            self.__sbMin.grid(     row = 0,  column = 4)
            self.__lbMin.grid(     row = 0,  column = 5)
        self.__lbNbRep.grid(       row = 9,  column = 0, sticky = "e" )
        self.__sbNbRep.grid(       row = 9,  column = 1, sticky = "w")
        self.__lbRepet.grid(       row = 10, column = 0, sticky = "e")
        self.__frameRepet.grid(    row = 10, column = 1, sticky = "we")
        self.__sbRep.pack( side = LEFT, fill = BOTH)
        self.__cbUnit.pack(side = LEFT, fill = BOTH, expand = YES)
        # Avancée
        # (voir parent) self._frameAdvanced.pack(side = TOP, fill = BOTH, expand = YES)
        self.__lbSubtask.grid(     row = 1, column = 0, sticky = "e" )
        self.__lbListSub.grid(     row = 1, column = 1, sticky = "w" )
        self.__lbDepces.grid(      row = 2, column = 0, sticky = "ne")
        self.__lbListDepces.grid(  row = 2, column = 1, sticky = "nswe", rowspan = 2)
        self.__btnSupprDepces.grid(row = 3, column = 0, sticky = "e" )
        self.__lbDeptes.grid(      row = 4, column = 0, sticky = "ne")
        self.__lbListDeptes.grid(  row = 4, column = 1, sticky = "nswe", rowspan = 2)
        self.__btnSupprDeptes.grid(row = 5, column = 0, sticky = "e" )
        self.__lbDone.grid(        row = 6, column = 0, sticky = "e" )
        self.__cbDone.grid(        row = 6, column = 1, sticky = "we")
        self.__lbParent.grid(      row = 7, column = 0, sticky = "e" )
        self.__lbResultParent.grid(row = 7, column = 1, sticky = "w" )
        self.__lbGroupe.grid(      row = 8, column = 0, sticky = "e" )
        self.__lbResultGroupe.grid(row = 8, column = 1, sticky = "w" )

        # Config grid
        self._frameAdvanced.columnconfigure(1, weight = 1)

        self.__autoSetDuree()

    def onClose(self):
        """
        On change tout ce qu'il faut
        """
        # Géré par le parent : nom, période, couleur, desc
        super().onClose()
        if not self._getSchedulable().isContainer():
            self._getSchedulable().setDebut(self.__varDebut, change = "duree")
            self._getSchedulable().setDuree(datetime.timedelta(days = self.__varJour.get(), hours = self.__varHour.get(), minutes = self.__varMin.get()))
        if self.__varRep is not None and self.__varUnitRep is not None:
            if self.__varUnitRep == "semaine":
                self._getSchedulable().setRep(datetime.timedelta(days = self.__varRep * 7))
            elif self.__varUnitRep == "jours":
                self._getSchedulable().setRep(datetime.timedelta(days = self.__varRep))
            elif self.__varUnitRep == "heures":
                self._getSchedulable().setRep(datetime.timedelta(hours = self.__varRep))

        self._getSchedulable().setNbRep(self.__varNbRep.get())
        self._getSchedulable().setDone(self.__varDone.get())

        self._getSchedulable().getApplication().getTaskEditor().redessiner()
        self._getSchedulable().getApplication().getDonneeCalendrier().updateAffichage(True) # Le True pour les liens de l'issue 92
        return

    def __askDebut(self):
        """
        Permet de demander le début de la tâche à l'utilisateur via boîte de dialogue usuelle.
        """
        ## demande de la date
        date = askdatetime(False)
        if date is None:
            return
        self.__varDebut = date
        self.__btnDebut.config(text = self.__varDebut if self.__varDebut is not None else "")
        self.__autoSetDuree()

    def __askFin(self):
        """
        Permet de demander la fin de la tâche à l'utilisateur via boîte de dialogue usuelle.
        """
        # demande de la date
        date = askdatetime(False)
        if date is None:
            return
        self.__varFin = date
        self.__btnFin.config(text = self.__varFin if self.__varFin is not None else "")
        self.__autoSetDuree()

    def __autoSetDuree(self):
        """
        Permet de mettre à jour les widgets de durée de tâche.
        """
        try:
            ecart = self.__varFin - self.__varDebut
            if ecart < datetime.timedelta(0) : # Si durée négative, on remet la fin en vue de la durée
                self.__autoSetFin()
                return
            else:
                self.__varJour.set(ecart.days)
                self.__varHour.set(ecart.seconds//3600)
                self.__varMin.set(ecart.seconds//60%60)
        except:pass

    def __autoSetFin(self):
        """
        Fonction qui change automatiquement la fin si on change la durée
        """
        self.__varFin = (self.__varDebut + datetime.timedelta(days = self.__varJour.get(), hours = self.__varHour.get(), minutes = self.__varMin.get()))
        self.__btnFin.config(text = self.__varFin)

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
            t = self.__lbListDepces.get(ACTIVE)
            id = t.split("ID")[-1]
            id = id[id.rfind(" ")+1:]
            depces = self._getSchedulableWithID(id)
            deptes = self._getSchedulable()
        elif mode == "deptes":
            t = self.__lbListDeptes.get(ACTIVE)
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
