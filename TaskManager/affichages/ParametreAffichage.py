# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

class ParametreAffichage(Frame):
    def __init__(self, master = None, **kwargs):
        kwargs["bg"] = "yellow"
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est référence vers ZoneAffichage.
        self.boutonBienAvant = Button(self, text="<<", command=lambda:master.envoyerChangementJourDebut("d"))
        self.boutonBienAvant.pack(side=LEFT, fill=Y)
        self.boutonAvant = Button(self, text="<", command=lambda:master.envoyerChangementJourDebut(-1))
        self.boutonAvant.pack(side=LEFT, fill=Y)    
        
        self.boutonBienApres = Button(self, text=">>", command=lambda:master.envoyerChangementJourDebut("f"))
        self.boutonBienApres.pack(side=RIGHT, fill=Y)          
        self.boutonApres = Button(self, text=">", command=lambda:master.envoyerChangementJourDebut(1))
        self.boutonApres.pack(side=RIGHT, fill=Y)             
        
        self.listeMode = Combobox(self, values=['1 jour', '2 jours', '5 jours', '1 semaine', 'P�riode'], state= "readonly")
        self.listeMode.set(self.listeMode.cget("values")[-1])
        self.listeMode.bind("<<ComboboxSelected>>",master.envoyerChangementNbJour) #passer par le maître et pas de parenthèses car on n'appelle pas la fonction, on la passe en paramètre
        self.listeMode.pack(side=TOP, fill=Y)
    
    def setModeListe(self, mode = None):
        etatActuel = self.listeMode.cget("state")
        self.listeMode.config(state = NORMAL)
        try:
            if mode is None and self.listeMode.get() not in self.listeMode.cget("values"):
                self.listeMode.set(self.listeMode.cget("values")[-1])
            elif mode is not None:
                self.listeMode.set(mode)
        finally:
            self.listeMode.config(state = etatActuel)
    
    def setStateListe(self, state):
        if state == NORMAL:
            state = "readonly"
        self.listeMode.config(state = state)
        
    def getBoutonsChangementJours(self):
        return [self.boutonBienAvant, self.boutonAvant, self.boutonApres, self.boutonBienApres]

    
