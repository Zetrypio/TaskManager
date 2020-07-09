# -*- coding: utf-8 -*-
from util.widgets.Dialog import *
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

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
        if button == "Ok":
            if not nom:
                showerror("Nom incorrect", "Vous devez nommer le groupe.")
            elif not desc:
                desc = ""
            elif not color:
                color = "#EFEFEF"
            else:
                groupe = Groupe(nom, periode, desc, color)
                fen.destroy()
    
    # Dialogue :
    fen = Dialog(title = "Ajouter un groupe",
                 buttons = ("Ok", "Annuler"),
                 exitButton = ("Annuler",),
                 command = onClose)
    
    # Widgets :
    
    
    # Activation :
    fen.activateandwait()

    # Retour :
    return groupe
