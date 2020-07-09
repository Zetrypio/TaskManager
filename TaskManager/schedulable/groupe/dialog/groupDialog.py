# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
from tkinter.messagebox import showerror
import datetime

from schedulable.groupe.Groupe import *

from util.widgets.Dialog import *
from util.widgets.ColorButton import *

def askGroup(periode):
    """
    Permet de demander à l'utilisateur les informations nécessaires pour créer un groupe.
    @param periode: La période dans laquelle sera le groupe.
    """
    # Variables :
    groupe = None
    nom = None
    desc = None
    color = None

    # Callback :
    def onClose(button):
        nonlocal groupe, nom, desc, color
        nom   = nomWidget.get()
        desc  = descWidget.get("0.0", END)
        color = colorWidget.get()
        if button == "Ok":
            if not nom:
                showerror("Nom incorrect", "Vous devez nommer le groupe.")
            else:
                groupe = Groupe(nom, periode, desc, color)
                fen.destroy()
    
    # Dialogue :
    fen = Dialog(title = "Ajouter un groupe",
                 buttons = ("Ok", "Annuler"),
                 exitButton = ("Annuler", "WM_DELETE_WINDOW"),
                 command = onClose)
    
    # Widgets :
    nomGroupe   = LabelFrame(fen, text = "Nom")
    descGroupe  = LabelFrame(fen, text = "Description")
    nomWidget   = Entry(nomGroupe)
    colorWidget = ColorButton(nomGroupe)
    descWidget  = Text(descGroupe, wrap="word")
    
    # Placements :
    descGroupe.pack(side = BOTTOM, expand = YES, fill = BOTH)
    nomGroupe.pack(side = TOP, expand = YES, fill = X)
    
    nomWidget.pack(side = LEFT, fill = X, expand = YES)
    colorWidget.pack(side = RIGHT)
    descWidget.pack(expand = YES, fill = BOTH)
    
    # Activation :
    fen.activateandwait()

    # Retour :
    return groupe
