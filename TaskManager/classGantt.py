# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime
from superclassCalendrier import *

class AffichageGantt(SuperCalendrier):
    def __init__(self, master = None, **kwargs):
        SuperCalendrier.__init__(self, master, **kwargs)
        # Note : self.master est référence vers Notebook.
        self.updateAffichage()
        
    
    def updateAffichage(self):
        self.__afficherLesJours()
    

    def __afficherLesJours(self):
        for indice, jour in enumerate(self.listeLabelJour): # on efface ceux déjà présent
            jour.destroy()
            self.columnconfigure(indice*2,weight=0)
            
        for indice, separator in enumerate(self.listeSeparateurJour): # on efface aussi les separator
            separator.destroy()
            self.columnconfigure(indice*2+1,weight=0)
        
        self.listeLabelJour = []
        self.listeSeparateurJour = []
        
        for jour in range(self.getJourDebut(), self.getJourDebut()+self.getNbJour()):
            self.listeLabelJour.append(Label(self, text=JOUR[jour%7]))
            self.listeLabelJour[-1].grid(row=0, column=(jour-self.getJourDebut())*2, sticky="NSWE")
            if jour != self.getJourDebut()+self.getNbJour()-1:
                self.listeSeparateurJour.append(Separator(self, orient=VERTICAL))
                self.listeSeparateurJour[-1].grid(row=0, column=1+2*(jour-self.getJourDebut()), rowspan = 2, sticky="NS") # le rowspan devra dépendre du nombre de tache a afficher
            
        self.__adapteGrid()

    def __adapteGrid(self):
        # à mettre À LA FIN ! ! ! (pour les expands)
        for column in range(self.nbJour*2):
            if column%2 ==0:
                self.columnconfigure(column,weight=1)
            else:
                self.columnconfigure(column, weight=0)
        self.rowconfigure(ALL,weight=1)
        self.rowconfigure(0, weight=0)

if __name__=='__main__':
    import Application
    Application.main()
