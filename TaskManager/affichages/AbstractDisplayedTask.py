# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

class AbstractDisplayedTask(Frame):
    def __init__(self, master, task, **kwargs):
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est une référence vers AffichageCalendrier ou AffichageGantt, héritant de AbstractDisplayedCalendar
        
        self.task = task

        self.texte = Text(self, wrap = "word", state = "normal", bg = "#0078FF" if self.task.isSelected() else self.task.getColor(), width=0, height=0)

        self.texte.insert(INSERT, task.getNom()) # On met le nom dedans
        self.texte.tag_add("titre", "0.0", "0.%s"%int(len(task.getNom())))
        self.texte.tag_config("titre", font="Arial 12 bold") 
        
        self.texte.insert(END, "\n"+task.getDescription())
        self.texte.tag_add("corps", "1.0", "1.%s"%int(len(task.getDescription())))
        self.texte.tag_config("corps", font="Arial 10") 
        
        self.texte.config(state = "disabled") # Pour ne pas changer le texte dedans
        self.texte.pack(fill=BOTH, expand=YES)# On l'affiche une fois qu'il est tout beau.
        self.pack_propagate(False)

        #La selection des taches
        self.texte.bind("<Button-1>", self._clique)
        self.texte.bind("<Control-Button-1>", self.multiSelection)

    def getCalendrier(self):
        return self.master

    def multiSelection(self, e):
        """Permet d'envoyer l'objet à la methode dans AbstractDisplayedCalendar"""
        self.getCalendrier().multiSelection(self.task)

    def _clique(self, e):
        self.getCalendrier().deselect()
        self.getCalendrier().select(self.task)

    def updateColor(self):
        # fonction pour mettre à jour la couleur
        try:
            self.texte.config(bg = "#0078FF" if self.task.isSelected() else self.task.getColor())
        except:
            self._report_exception()

    def getGroupes():
        """ Retourne une liste de groupe auxquelles appartient la tache et None s'il n'y a pas de groupe """
        return self.task.getGroupes()


