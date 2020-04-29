# -*- coding: utf-8 -*-
from tkinter.messagebox import *
from ttkcalendar import *
from dialog import *
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

MOIS = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

def rangeMois(debut, fin):
    while debut != fin:
        yield debut.month
        debut += datetime.timedelta(days = tailleMois(debut.month, debut.year))
    yield fin.month

def tailleMois(mois, annee):
        return (datetime.datetime(annee + (mois)//12, (mois)%12+1, 1) - datetime.timedelta(days = 1)).day

def askScinderPeriode(periodManager, taskEditor, periode = None):
    # Vérifications :
    if periode.getDebut() == periode.getFin():
        showerror("Longueur de période invalide", "Il est impossible de scinder une période qui dure un seul jour.")
        raise ValueError("Impossiblr de scinder une période qui dure un seul jour")

    # Variables à retourner :
    dateScindage = None

    # Fonction quand on appuie sur un bouton :
    def onClose(button):
        nonlocal dateScindage
        if button == "Aujourd'hui":
            date = datetime.datetime.now().date()
            jour.set(date.day)
            if mois is not None:
                mois.set(MOIS[date.month - 1])
            if annee is not None:
                annee.set(date.year)
            return
        if button == "Ok":
            dateScindage = datetime.date(getAnnee(), getMois(), getJour())
        fen.destroy()

    def setJourCalendrier(event):
        if event.widget.master == cal:
            date = cal.selection.date()
            if date is not None:
                if date < periode.getDebut() or date > periode.getFin():
                    showerror("Date invalide", "La date choisie est en dehors des limites de la période à scinder.")
                    return
                jour.set(date.day)
                if mois is not None:
                    mois.set(MOIS[date.month - 1])
                if annee is not None:
                    annee.set(date.year)
    
    def adapteJours():
        min = 1
        max = tailleMois(getMois(), getAnnee())
        
        if getMois() == periode.getDebut().month and getAnnee() == periode.getDebut().year:
            min = periode.getDebut().day
        if getMois() == periode.getFin().month and getAnnee() == periode.getFin().year:
            max = periode.getFin().day
        
        jour.config(from_ = min, to = max)
        if getJour() < min:
            jour.set(min)
        if getJour() > max:
            jour.set(max)
    
    def adapteMois():
        if mois is not None:
            lesMois = {}
            for m in rangeMois(periode.getDebut(), periode.getFin()):
                lesMois.add(m)
            lesVraisMois = []
            for indice, m in enumerate(MOIS):
                if indice+1 in lesMois:
                    lesVraisMois.append(m)
            mois.config(values = lesVraisMois)
            if mois.get() not in lesVraisMois:
                mois.set(lesVraisMois[0])
    
    def adapte():
        adapteMois()
        adapteJours()
    
    def getJour():
        return int(jour.get())
    def getMois():
        if mois is None:
            return datetime.datetime.now().month
        return MOIS.index(mois.get()) + 1
    def getAnnee():
        if annee is None:
            return datetime.datetime.now().year
        return int(annee.get())

    # Dialogue :
    fen = Dialog(title = "Scinder une période", buttons = ("Ok", "Annuler", "Aujourd'hui"), command=onClose)
    
    # Widgets :
    cal = Calendar(fen)
    cal.pack(expand = YES, fill = BOTH, side = TOP)
    cal.bind_all("<Button-1>", setJourCalendrier)

    jour = Spinbox(fen, from_ = 1, to = 31)
    jour.pack(side = LEFT, fill = X)
    
    if periode.getDebut().year != periode.getFin().year or periode.getDebut().month != periode.getFin().month:
        mois = Combobox(fen,
                        values = MOIS,
                        state = "readonly")
        mois.pack(side = LEFT, fill = X)
    else:
        mois = None
    
    if periode.getDebut().year != periode.getFin().year:
        annee = Spinbox(fen, from_ = periode.getDebut().year, to = periode.getFin().year)
        annee.pack(side = LEFT, fill = X)
    else:
        annee = None

    # Activation du dialogue :
    fen.activateandwait()
    
    # revoie des valeures
    return dateScindage

if __name__ == '__main__':
    import Application
    Application.main()