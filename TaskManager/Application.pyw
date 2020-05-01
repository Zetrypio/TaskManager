# -*- coding:utf-8 -*-
# Installation auto au début:
from util.importPIL import *
# Imports :
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

from affichages.CalendarZone import *
from affichages.periode.Periode import *
from affichages.periode.PeriodManager import *
from task.TaskEditor import *

from MenuBar import *


# CECI est la CORRECTION d'un BUG :

style = Style()

def fixed_map(option):
    """
    Returns the style map for 'option' with any styles starting with
    ("!disabled", "!selected", ...) filtered out

    style.map() returns an empty list for missing options, so this should
    be future-safe
    """
    return [elm for elm in style.map("Treeview", query_opt=option)
            if elm[:2] != ("!disabled", "!selected")]

style.map("Treeview",
          foreground=fixed_map("foreground"),
          background=fixed_map("background"))



class Application(Frame):
    def __init__(self, master = None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.winfo_toplevel().title("Gestionnaire de calendrier")
        self.menu = MenuBar(self.winfo_toplevel(), self)
        self.periodManager = PeriodManager(self)
        self.taskEditor = TaskEditor(self, self.menu, self.periodManager)
        self.taskEditor.pack(side=LEFT, fill = BOTH, expand = NO)
        self.calendar = CalendarZone(self, self.periodManager)
        self.calendar.pack(side=LEFT, fill = BOTH, expand = YES)
    def nouveau(self):pass
    def setModeEditionPeriode(self, enEdition):
        self.calendar.setBarreOutilPeriode(enEdition)
        if enEdition:
            #self.taskEditor.filter(type = "Période")
            self.taskEditor.setEditionPeriode(True)
            pass
        else:
            #self.taskEditor.filter(type = "Tâche")
            self.taskEditor.setEditionPeriode(False)
            pass
    def getPeriodManager(self):
        return self.periodManager
    def getPanneauActif(self):
        return self.calendar.getPanneauActif()
    def getDonneeCalendrier(self):
        return self.calendar.getDonneeCalendrier()



def main():
    """Fonction main, principale du programme."""
    app = Application()
    app.pack(expand = YES, fill = BOTH)
    
    # Création de taches préaite
    app.taskEditor.ajouter(Task("A", datetime.datetime(2020, 4, 6, 8, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#F77CAA"))
    app.taskEditor.ajouter(Task("B", datetime.datetime(2020, 4, 8, 8, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#7CF0F7"))
    app.taskEditor.ajouter(Task("C", datetime.datetime(2020, 4, 8, 10, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#C2F77C"))
    app.taskEditor.ajouter(Task("D", datetime.datetime(2020, 4, 12, 8, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#B97CF7"))
    app.taskEditor.ajouter(Task("E", datetime.datetime(2020, 4, 12, 10, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#5D7CDC"))
    app.taskEditor.ajouter(Task("F", datetime.datetime(2020, 4, 8, 12, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#FA6FFF"))
    app.taskEditor.ajouter(Task("Joyeux anniversaire", datetime.datetime(2020, 4, 26, 12, 0, 0), datetime.timedelta(0,0,0, 0, 0, 5),-1,0,"Gateau au chocolat et ne pas oublier la crême anglaise","#85FAB7"))
    
    app.mainloop()
    try:
        app.destroy()
    except:
        pass