# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from util.widgets.Dialog import *

from schedulable.task.dialog.TaskParametre import *


def askEditTask(task):
    """
    Dialogue qui édite la tache sur ses paramètres
    @param task : <Task> la tache à modifier
    """
    def onClose(button):
        if button == "Ok":
            parametrage.onClose()
            return
        fen.destroy()


    fen = Dialog(title = "Édition de \"%s\""%task.getNom(), buttons = ("Ok", "Annuler"), command = onClose) # Ajouter un supprimer
    parametrage = TaskParametre(fen, task)
    parametrage.pack(fill = BOTH, expand = YES)
    fen.activateandwait()
