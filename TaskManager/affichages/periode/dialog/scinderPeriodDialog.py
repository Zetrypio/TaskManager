# -*- coding: utf-8 -*-
from tkinter.messagebox import showerror
from util.widgets.ttkcalendar import *
from util.widgets.Dialog import *
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

MOIS = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

def rangeMois(debut, fin):
    compteur = 0
    while debut < fin and compteur < 14:
        yield debut.month
        debut += datetime.timedelta(days = tailleMois(debut.month, debut.year))
        compteur += 1
    yield fin.month

def tailleMois(mois, annee):
    return (datetime.datetime(annee + mois//12, (mois)%12+1, 1) - datetime.timedelta(days = 1)).day

def askScinderPeriode(periodManager, taskEditor, periode = None):
    # Vérifications :
    if periode.getDebut() == periode.getFin():
        showerror("Longueur de période invalide", "Il est impossible de scinder une période qui dure un seul jour.")
        raise ValueError("Impossible de scinder une période qui dure un seul jour")
    
    def getDebut():
        return periode.getDebut() + datetime.timedelta(days = 1)

    # Une période de 2 jours ne peut être coupé qu'entre les 2 jours,
    # donc le début de la 2ème période dure à partir du 2ème jour,
    # soit la fin de cette période. (on notera que la fonction permet justement d'ignorer le début,
    # étant donné qu'il est impossible de scinder le même jour que ça commence).
    if getDebut() == periode.getFin():
        return periode.getFin()

    # Variables à retourner :
    dateScindage = None
    
    # Fonction quand on appuie sur un bouton :
    def onClose(button):
        """
        Fonction quand on appuie sur un bouton.
        @param button: le texte du bouton appuyé.
        """
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

    def setJourCalendrier():
        date = cal.selection
        if date is not None:
            date = date.date()
            if date < getDebut() or date > periode.getFin():
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
        
        if getMois() == getDebut().month and getAnnee() == getDebut().year:
            min = getDebut().day
        if getMois() == periode.getFin().month and getAnnee() == periode.getFin().year:
            max = periode.getFin().day
        
        jour.config(from_ = min, to = max)
        if getJour() < min:
            jour.set(min)
        if getJour() > max:
            jour.set(max)
    
    def adapteMois():
        if mois is not None:
            lesMois = set()
            for m in rangeMois(getDebut(), periode.getFin()):
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
        if not jour.get():
            jour.set(1)
        return int(jour.get())
    def getMois():
        if mois is None:
            return datetime.datetime.now().month
        return MOIS.index(mois.get()) + 1
    def getAnnee():
        if annee is None:
            return datetime.datetime.now().year
        if not annee.get():
            jour.set(getDebut().year)
        return int(annee.get())

    # Dialogue :
    hasAujourdhui = datetime.datetime.now().date() >= getDebut() and datetime.datetime.now().date() < periode.getFin()
    fen = Dialog(title = "Scinder une période", buttons = ("Ok", "Annuler", "Aujourd'hui") if hasAujourdhui else ("Ok", "Annuler"), command=onClose)
    
    # Widgets :
    cal = Calendar(fen)
    cal.pack(expand = YES, fill = BOTH, side = TOP)
    cal._calendar.bind("<Button-1>", lambda e: setJourCalendrier(), add = True)

    Label(fen, text = "Le :").pack(side = LEFT, fill = X)
    jour = Spinbox(fen, from_ = 1, to = 31, command = adapte, width = 4)
    jour.pack(side = LEFT, fill = X)
    
    if getDebut().year != periode.getFin().year or getDebut().month != periode.getFin().month:
        mois = Combobox(fen, values = MOIS, state = "readonly", width = 11)
        mois.bind("<<ComboboxSelected>>", lambda e: adapte())
        mois.pack(side = LEFT, fill = X)
    else:   
        mois = None
        Label(fen, text = MOIS[getMois()-1]).pack(side = LEFT, fill = X)
    
    if getDebut().year != periode.getFin().year:
        annee = Spinbox(fen, from_ = getDebut().year, to = periode.getFin().year, command = adapte, width = 6)
        annee.pack(side = LEFT, fill = X)
    else:
        annee = None
        Label(fen, text = getAnnee()).pack(side = LEFT, fill = X)
    
    adapte()

    # Activation du dialogue :
    fen.activateandwait()
    
    # renvoie des valeurs
    return dateScindage

