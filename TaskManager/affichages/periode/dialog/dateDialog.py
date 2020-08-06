# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from util.widgets.Dialog import *
from util.widgets.ttkcalendar import *
from util.util import *

def askdate(data):
    """
    Permet d'ouvrir une boîte de dialogue usuelle pour demander
    la date (et pas l'heure) à l'utilisateur.
    @param data : <Data> pour la couleur du bandeau du calendrier
    @return datetime.date() choisie par l'utilisateur ou None
    """
    # Variable qui contient la valeur de retour :
    dateretour = None
    
    # Callback quand on ferme la fenêtre par l'un des boutons :
    def onClose(a):
        nonlocal dateretour

        # Si on annule :
        if a == 'Annuler' or a=='WM_DELETE_WINDOW':
            fen.destroy()
            return
        
        # Si on accepte :
        if cal.selection is not None:
            dateretour = cal.selection.date()
        # on ferme la fenêtre.
        fen.destroy()

    # Construction du dialogue :
    fen = Dialog(title = "Choix de la date", buttons = ("Ok", "Annuler"), command=onClose)
    # création des widgets :
    cal = Calendar(master = fen, data = data, firstweekday=calendar.MONDAY)
    # placement des widgets :
    cal.pack(expand=1, fill='both')

    # et on active le dialogue.
    fen.activateandwait()
    return dateretour
