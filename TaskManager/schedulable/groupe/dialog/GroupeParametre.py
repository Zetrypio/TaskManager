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
        super().add(self.__frameSchedu, text = "Taches")

        # Initialisation des variables
        self.__listParamTask = [] # Liste des TaskParametres dont il faudra appeler onClose
        # Affectation des variables
        # Attributs généraux
        # Attributs avancées
        # Attributs taches
        self.__cbSchedu = Combobox(self.__frameSchedu, value = [s for s in self.getSchedulable().getListTasks()], state = "readonly")
        self.__cbSchedu.bind("<<ComboboxSelected>>", self.__updateTask)

        ## Affichage
        # Taches
        self.__cbSchedu.pack(side = TOP, fill = X, expand = NO)

    def __updateTask(self, e = None):
        """
        Méthode pour mettre à jour l'affichage de la tache
        en question dont on doit afficher les pramatres
        """
        t = [task for task in self.getSchedulable().getListTasks() if str(task) == self.__cbSchedu.get()][0]
        # Si la liste est vide on a juste à pack et enregistrer ce nouveau TaskParametre
        if self.__listParamTask == []:
            self.__listParamTask.append(TaskParametre(self.__frameSchedu,t))
            self.__listParamTask[-1].pack(fill = BOTH, expand = YES)
        # Sinon il faut packForget le dernier
        else :
            self.__listParamTask[-1].pack_forget()
            for paramTask in self.__listParamTask:
                if paramTask.getSchedulable() == t:
                    paramTask.pack(fill = BOTH, expand = YES)
                    # On le remet à la fin, prêt à être pack_forget()
                    self.__listParamTask.append(self.__listParamTask.pop(self.__listParamTask.index(paramTask)))
                    break
            else:
                self.__listParamTask.append(TaskParametre(self.__frameSchedu,t))
                self.__listParamTask[-1].pack(fill = BOTH, expand = YES)



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
