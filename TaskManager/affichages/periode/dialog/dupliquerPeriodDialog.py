# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

from util.widgets.Dialog import *


def askDupliquerPeriode(periodManager, taskEditor, from_ = None):
    from affichages.periode.Periode import Periode
    from ..PeriodAdder import PeriodAdder

    per = from_

    def onClose(button):
        if button == "Ajouter":
            periode = p.createPeriode()
            
            ## Ajout des schedulables et autres :
            # Il faut en faire une copie,
            # Mais pour éviter tout les soucis de non copies en profondeur
            # (je pense notamment aux dépendances qui pourrait alors se trouver dans une autre période...)
            # on va faire une "sauvegarde-lecture" dans la RAM.
            data = per.saveByDict()
            newPeriode = Periode.load(data, periodManager)
            # Puis on remet les attributs :
            newPeriode.setNom(periode.getNom())
            newPeriode.setDebut(periode.getDebut())
            newPeriode.setFin(periode.getFin())
            newPeriode.setDescription(periode.getDescription())
            newPeriode.setColor(periode.getColor())
            periodManager.ajouter(newPeriode)
            

    fen = Dialog(command = onClose,
                 buttons = ("Ajouter", "Fermer"),
                 exitButton = ("Fermer", "WM_DELETE_WINDOW"))

    fen.redessiner = taskEditor.redessiner
    fen.ajouter = taskEditor.ajouter

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
        p.boutonColor     .set(per.color)
    
    fen.activateandwait()
