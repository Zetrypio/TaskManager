# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

from util.widgets.Dialog import *


def askModifierPeriode(periodManager, taskEditor, from_ = None):
    from ..PeriodAdder import PeriodAdder

    per = from_

    def onClose(button):
        if button == "Modifier":
            # La création d'une période permettra de récupérer ses attributs.
            # Cependant, cette période est temporaire au calcul et n'est pas
            # ajoutée au PeriodManager.
            periode = p.createPeriode()
            
            # Puis on remet les attributs :
            per.setNom(periode.getNom())
            per.setDebut(periode.getDebut())
            per.setFin(periode.getFin())
            per.setDescription(periode.getDescription())
            per.setColor(periode.getColor())
    
    fen = Dialog(command = onClose,
                 buttons = ("Modifier", "Annuler"),
                 exitButton = ("Modifier", "Annuler", "Fermer", "WM_DELETE_WINDOW"))

    # Pour faire croire au PeriodAdder que le Dialog est le TaskEditor.
    fen.redessiner     = taskEditor.redessiner
    fen.ajouter        = taskEditor.ajouter
    fen.getApplication = taskEditor.getApplication
    
    p = PeriodAdder(periodManager, fen)
    p.pack(expand = YES, fill = BOTH)
    p.boutonValider.grid_forget()
    
    # Ajouter les champs déjà rempli si on a une période :
    if per is not None:
        p.debut = per.getDebut()
        p.fin   = per.getFin()
        p.champNom        .insert(END, per.nom)
        p.champDebut      .config(text = p.debut)
        p.champFin        .config(text = p.fin)
        p.champDescription.insert(END, per.desc)
        p.boutonColor     .config(bg = per.color)
    
    fen.activateandwait()

    
