# -*- coding:utf-8 -*-
# Installation auto au début:
from util.importPIL import *
# Imports :
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import os

from affichages.CalendarZone import *
from affichages.groupe.Groupe import *
from affichages.groupe.GroupeManager import *
from affichages.periode.Periode import *
from affichages.periode.PeriodManager import *
from task.TaskEditor import *

from MenuBar import *
from preferences.fenetre import *
from profil.data import *
from profil.ProfilManager import *
from profil.BindingManager import *


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

        os.makedirs(os.path.expanduser("~/.taskManager/"), exist_ok = True)

        self.__data = Data()

        self.winfo_toplevel().title("Gestionnaire de calendrier")
        self.menu = MenuBar(self.winfo_toplevel(), self)
        self.periodManager = PeriodManager(self)
        self.taskEditor = TaskEditor(self, self.menu, self.periodManager)
        self.taskEditor.pack(side=LEFT, fill = BOTH, expand = NO)
        self.calendar = CalendarZone(self, self.periodManager)
        self.calendar.pack(side=LEFT, fill = BOTH, expand = YES)

        print("Avant profil Manager")
        self.__profilManager  = ProfilManager(self)
        print("Apres profil Manager")
        self.__BindingManager = BindingManager(self)
        self.prefFen = FenetrePreferences(self)

        self.bind_all("<Control-,>", lambda e=None:self.preferences())

    def destroy(self):
        """
        Redéfinition de la méthode pour supprimer aussi la fenetre parente
        """
        super().destroy()
        try:
            self.winfo_toplevel().destroy() # Pour détruire aussi la fenêtre parente
        except:pass

    def nouveau(self):pass
    def setModeEditionPeriode(self, enEdition):
        self.calendar.setBarreOutilPeriode(enEdition)
        if enEdition:
            self.taskEditor.filter(type = ("Période", "Tâche indépendante"))
            self.taskEditor.setEditionPeriode(True)
            pass
        else:
            self.taskEditor.filter(type = ("Tâche", "Tâche indépendante"))
            self.taskEditor.setEditionPeriode(False)
            pass

    def preferences(self):
        self.prefFen.activateandwait()

    def getPeriodManager(self):
        return self.periodManager
    def getPanneauActif(self):
        return self.calendar.getPanneauActif()
    def getDonneeCalendrier(self):
        return self.calendar.getDonneeCalendrier()
    def getTaskEditor(self):
        return self.taskEditor

    def getData(self):
        """ Retourne le Gestionnaire des données """
        return self.__data

    def getProfilManager(self):
        """ Retourne le Profil Manager """
        return self.__profilManager
    def getBindingManager(self):
        """ Retourne le Profil Manager """
        return self.__BindingManager



def main():
    """Fonction main, principale du programme."""
    app = Application()
    app.pack(expand = YES, fill = BOTH)
    

    # Création de periode préfaite

    periodeSemaine = app.getPeriodManager().ajouter( Periode(app.getPeriodManager(),"semaine", datetime.date(2020, 5, 4), datetime.date(2020, 5, 27), "semaine pour faciliter les calculs",color = "#7FFF7F"))
    periodeSemaine = app.getPeriodManager().getPeriodes()[-1]

    # Création de taches  préfaite
    app.taskEditor.ajouter(Task("A", datetime.datetime(2020, 5, 6, 8, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#F77CAA", periode = periodeSemaine))
    app.taskEditor.ajouter(Task("B", datetime.datetime(2020, 5, 8, 8, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#7CF0F7", periode = periodeSemaine))
    app.taskEditor.ajouter(Task("C", datetime.datetime(2020, 5, 8, 10, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#C2F77C", periode = periodeSemaine))
    app.taskEditor.ajouter(Task("D", datetime.datetime(2020, 5, 12, 8, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#B97CF7", periode = periodeSemaine))
    app.taskEditor.ajouter(Task("E", datetime.datetime(2020, 5, 12, 10, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#5D7CDC", periode = periodeSemaine))
    app.taskEditor.ajouter(Task("F", datetime.datetime(2020, 5, 8, 12, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#FA6FFF", periode = periodeSemaine))
    app.taskEditor.ajouter(Task("Joyeux anniversaire", datetime.datetime(2020, 5, 26, 12, 0, 0), datetime.timedelta(0,0,0, 0, 0, 5),-1,0,"Gateau au chocolat et ne pas oublier la crême anglaise","#85FAB7", periode = periodeSemaine))

    # Création d'un groupe préfait
    periodeSemaine.getGroupeManager().ajouter(Groupe("Mon Groupe", [app.taskEditor.taches[1]], "#FF88FF", periodeSemaine, periodeSemaine.getGroupeManager()))
    
    app.mainloop()
    try:
        app.destroy()
    except:
        pass
