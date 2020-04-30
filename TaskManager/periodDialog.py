# -*- coding: utf-8 -*-
from dialog import *
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

def askPeriode(periodManager, taskEditor, from_ = None, duplicate = False):
    # JE SAIS PAS POURQUOI, MAIS ON EST OBLIGE DE NE PAS LE METTRE DANS LE GLOBAL,
    # CAR SINON "Periode" N'EXISTE PAS DANS LE FICHIER "periodAdder.py". JE NE TROUVE
    # PAS CELA LOGIQUE. LES IMPORTS EN PYTHON SONT VRAIMENT TRÈS MAL FAIT !!!!!!!!!!
    # CA N'A AUCUN SENS ET CA PEUT M'ENERVER. DONC LAISSEZ LE ICI TANT QUE CA MARCHE...
    from periodAdder import PeriodAdder
    
    per = from_

    def onClose(button):
        if button == "Ajouter" or button == "Modifier":
            p.valider()
    
    def supprimerPuisAjouter(*a):
        pass # TODO quand on aura de quoi faire.
#        taskEditor.remove(per)
#        taskEditor.ajouter(*a)

    def configurer():
        print("a")
        periodManager.supprimerPeriode()
        print("b")
        valider()
    
    fen = Dialog(command = onClose,
                 buttons = ("Ajouter" if duplicate else "Modifier", "Fermer" if duplicate else "Annuler"),
                 exitButton = ("Modifier", "Annuler", "Fermer", "WM_DELETE_WINDOW"))

    fen.redessiner = taskEditor.redessiner
    fen.ajouter = taskEditor.ajouter
    
    p = PeriodAdder(periodManager, fen)
    p.pack(expand = YES, fill = BOTH)
    p.boutonValider.grid_forget()
    
    if not duplicate:
        fen.ajouter = supprimerPuisAjouter
        valider = p.valider
        p.valider = configurer

    if per is not None:
        p.debut = per.getDebut()
        p.fin   = per.getFin()
        p.champNom        .insert(END, per.nom)
        p.champDebut      .config(text = p.debut)
        p.champFin        .config(text = p.fin)
        p.champDescription.insert(END, per.desc)
        p.boutonColor     .config(bg = per.color)
    
    fen.activateandwait()

if __name__ == '__main__':
    import  Application
    Application.main()