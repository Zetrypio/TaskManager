# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

from util.widgets.Dialog import *


def askPeriode(periodManager, taskEditor, from_ = None):
    from ..PeriodAdder import PeriodAdder

    per = from_

    def onClose(button):
        if button == "Ajouter" or button == "Modifier":
            p.valider()
    
    def supprimerPuisAjouter(*a):
        pass # TODO quand on aura de quoi faire.
#        taskEditor.remove(per)
#        taskEditor.ajouter(*a)

    def configurer():
        periodManager.supprimerPeriodes()
        valider()
    
    fen = Dialog(command = onClose,
                 buttons = ("Modifier", "Annuler"),
                 exitButton = ("Modifier", "Annuler", "Fermer", "WM_DELETE_WINDOW"))

    fen.redessiner = taskEditor.redessiner
    fen.ajouter = taskEditor.ajouter
    
    p = PeriodAdder(periodManager, fen)
    p.pack(expand = YES, fill = BOTH)
    p.boutonValider.grid_forget()
    
    fen.ajouter = supprimerPuisAjouter
    valider = p.valider
    p.valider = configurer

    # Sauvegarder les tâches : TODO
    if per:
        listSchedulables =      per.listSchedulables
        listAllThingsInPeriod = per.listAllThingsInPeriod

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

    
