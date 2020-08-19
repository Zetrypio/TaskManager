# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from util.widgets.ColorButton import *
from ...AbstractSchedulableParametre import *

from ...task.dialog.TaskParametre import *

class GroupeParametre(AbstractSchedulableParametre):
    """
    Notebook qui contient tous les paramètres du groupe
    fournis dans le constructeur.
    Permet aussi de changer ses attributs (au groupe)
    """
    def __init__(self, master, groupe, **kw):
        """
        @param master : <tkinter.frame>
        @param groupe   : <Groupe> ceux qui sont à afficher
        """
        super().__init__(master, groupe, **kw)

        # page des schedulables in
        self.__frameSchedu = Frame(self)
        super().add(self.__frameSchedu, text = "Tâches")

        # Initialisation des variables
        self.__listParamTask = [] # Liste des TaskParametres dont il faudra appeler onClose
        self.__varNbTask = IntVar()
        self.__varListTasks = StringVar()
        self.__varComboLT = StringVar()

        # Affectation des variables
        self.__varNbTask.set(len(self._getSchedulable().getListTasks()))
        self.__varListTasks.set([(str(s) + "   ID : " + s.getUniqueID()) for s in self._getSchedulable().getListTasks()])


        # Attributs généraux
        self.__lbTaskNb = Label(self._frameGeneral, text = "Nombre de taches :")
        self.__lbResultTaskNb = Label(self._frameGeneral, textvariable = self.__varNbTask)
        self.__lbTask = Label(self._frameGeneral, text = "Taches :")
        self.__lbListTask = Listbox(self._frameGeneral, listvariable = self.__varListTasks, height = len(self._getSchedulable().getListTasks()), selectmode = "extended")
        self.__btnRetireGen = Button(self._frameGeneral, text = "Retirer", command = lambda : self.__removeTask(strTask = self.__lbListTask.get(ACTIVE)))

        # Attributs avancées

        # Attributs taches
        self.__cbSchedu = Combobox(self.__frameSchedu, value = [(str(s) + "   ID : " + s.getUniqueID()) for s in self._getSchedulable().getListTasks()], state = "readonly", textvariable = self.__varComboLT)
        self.__cbSchedu.bind("<<ComboboxSelected>>", self.__updateTask)
        self.__btnRetireTask = Button(self.__frameSchedu, text = "Retirer", command = lambda : self.__removeTask(strTask = self.__varComboLT.get()))

        ## Affichage
        # Générale (grid Obligé)
        self.__lbTaskNb.grid(      row = 6, column = 0, sticky = "e")
        self.__lbResultTaskNb.grid(row = 6, column = 1)
        self.__lbTask.grid(        row = 7, column = 0, sticky = "e")
        self.__lbListTask.grid(    row = 7, column = 1, sticky = NSEW, rowspan = 2)
        self.__btnRetireGen.grid(  row = 8, column = 0, sticky = "e")
        # Taches (libre)
        self.__cbSchedu.grid(row = 0, column = 0, sticky = "we")
        self.__btnRetireTask.grid(row = 0, column = 1)

        # Final
        self._frameGeneral.columnconfigure(1, weight = 1)
        self.__frameSchedu.columnconfigure(0, weight = 1)
        self.__frameSchedu.rowconfigure(1, weight = 1)

    ""
    ############
    # Méthodes #
    ############
    ""
    def __removeTask(self, strTask = None):
        """
        Méthode qui retire la task du groupe
        @param task     : <str> de la tache AVEC son UID
        """
        # S'il n'y a rien
        if strTask is None:
            return
        # On cherche l'ID
        id = strTask.split("ID")[-1]
        id = id[id.rfind(" ")+1:]
        # On retire le schedulable
        print(id, [s.getUniqueID() for s in self._getSchedulable().getListTasks()])
        task = [s for s in self._getSchedulable().getListTasks() if s.getUniqueID() == id][0]
        self._getSchedulable().removeTask(task, testDelete = True)
        #self._getSchedulable().getPeriode().addPrimitiveSchedulable(task)
        #task.instantiate()
        # On remet à jour tout le monde
        self.__cbSchedu.config(value = [(str(s) + "   ID : " + s.getUniqueID()) for s in self._getSchedulable().getListTasks()])
        self.__varComboLT.set("")
        self.__updateTask()
        self.__varNbTask.set(len(self._getSchedulable().getListTasks()))
        self.__varListTasks.set([(str(s) + "   ID : " + s.getUniqueID()) for s in self._getSchedulable().getListTasks()])


    def __updateTask(self, e = None):
        """
        Méthode pour mettre à jour l'affichage de la tache
        en question dont on doit afficher les pramatres
        """
        t = [task for task in self._getSchedulable().getListTasks() if (str(task) + "   ID : " + task.getUniqueID()) == self.__cbSchedu.get()]
        # Si rien de correspond on grid_forget et on annule tout (c'est si on retire la tache en question)
        if t == []: # ne pas mettre if self.__listParamTask != []
            self.__listParamTask[-1].grid_forget() if self.__listParamTask != [] else None
            self.__listParamTask.pop(-1) if  self.__listParamTask != [] else None
            return
        else :
            t = t[0]
        # Si la liste est vide on a juste à grid et enregistrer ce nouveau TaskParametre
        if self.__listParamTask == []:
            self.__listParamTask.append(TaskParametre(self.__frameSchedu, t))
            self.__listParamTask[-1].grid(row = 1, column = 0, columnspan = 2, sticky = NSEW)
        # Sinon il faut gridForget le dernier
        else :
            self.__listParamTask[-1].grid_forget()
            for paramTask in self.__listParamTask:
                if paramTask._getSchedulable() == t:
                    paramTask.grid(row = 1, column = 0, columnspan = 2, sticky = NSEW)
                    # On le remet à la fin, prêt à être grid_forget()
                    self.__listParamTask.append(self.__listParamTask.pop(self.__listParamTask.index(paramTask)))
                    break
            else:
                self.__listParamTask.append(TaskParametre(self.__frameSchedu,t))
                self.__listParamTask[-1].grid(row = 1, column = 0, columnspan = 2, sticky = NSEW)

    "" # Pour le repli de code
    ###########
    # onClose #
    ###########
    ""
    def onClose(self):
        """
        On change les attributs
        """
        super().onClose()
        for p in self.__listParamTask:
            p.onClose()
