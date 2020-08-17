# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from util.widgets.Dialog import *

from schedulable.group.dialog.GroupParametre import *

def askEditGroupe(groupe):
    """
    Dialogue qui édite le groupe sur ses paramètres
    @param groupe : <Groupe> le groupe à modifier
    """
    def onClose(button):
        if button == "Ok":
            print("ok.")
        fen.destroy()

    fen = Dialog(title = "Édition de \"%s\""%groupe.getNom(), buttons = ("Ok", "Annuler"), command = onClose) # Ajouter un supprimer
    paramGroupe = ParametreGroupe(groupe)
    paramGroupe.pack(fill = BOTH, expand = YES)
    fen.activateandwait()

