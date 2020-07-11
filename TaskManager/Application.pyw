# -*- coding:utf-8 -*-
# Installation auto au début:
from util.importPIL import *
# Imports :
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import os

from affichages.CalendarZone import *
from affichages.periode.Periode import *
from affichages.periode.PeriodManager import *
from schedulable.groupe.Groupe import *
from schedulable.groupe.GroupeManager import *
from schedulable.task.TaskEditor import *

from MenuBar import *
from preferences.fenetre import *
from dataManager.data import *
from dataManager.ProfilManager import *
from dataManager.BindingManager import *


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
    """
    Application Globale.
    """
    def __init__(self, master = None, **kwargs):
        """
        Constructeur de l'application.
        @param master: master du tkinter.Frame() que cet objet est.
        @param **kwargs: paramètre de configurations du tkinter.Frame() que cet objet est.
        """
        super().__init__(master, **kwargs)
        os.makedirs(os.path.expanduser("~/.taskManager/"), exist_ok = True)

        self.__data = Data()

        self.winfo_toplevel().title("Gestionnaire de calendrier")
        self.menu = MenuBar(self.winfo_toplevel(), self)
        self.periodManager = PeriodManager(self)
        self.taskEditor = TaskEditor(self, self.menu, self.periodManager)
        self.taskEditor.pack(side=LEFT, fill = BOTH, expand = NO)
        self.calendar = CalendarZone(self, self.periodManager)
        self.calendar.pack(side=LEFT, fill = BOTH, expand = YES)

        self.__profilManager  = ProfilManager(self)
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
        """
        Permet de switcher entre le mode période et le mode normal.
        @param enEdition: True pour période, False sinon.
        """
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
        print(" non lancé")
        self.prefFen.activateandwait()
        print("lancé")

    def getPeriodManager(self):
        """
        Permet d'obtenir le PeriodManager.
        @return le periodeManager.
        """
        return self.periodManager

    def getPanneauActif(self):
        """
        Permet d'obtenir le panneau actif dans les affichages de calendrier.
        @return le panneau actif dans les affichages de calendrier.
        """
        return self.calendar.getPanneauActif()

    def getDonneeCalendrier(self):
        """
        Permet d'obtenir le DonneeCalendrier.
        @return le DonneeCalendrier.
        """
        return self.calendar.getDonneeCalendrier()

    def getTaskEditor(self):
        """
        Permet d'obtenir le TaskEditor.
        @return le TaskEditor.
        """
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
    w = app.winfo_toplevel().winfo_screenwidth()
    h = app.winfo_toplevel().winfo_screenheight()
    app.winfo_toplevel().geometry("%sx%s+%s+%s"%(int(0.9*w), int(0.8*h), int(0.05*w), int(0.05*h)))
    app.update()
    try:
        app.winfo_toplevel().state("zoomed")
    except:
        pass
    app.pack(expand = YES, fill = BOTH)
    

    # Création d'une période préfaite
    periodeSemaine = Periode(app.getPeriodManager(),
                             "semaine",
                             datetime.date(2020, 7, 4),
                             datetime.date(2020, 7, 27),
                             "semaine pour faciliter les calculs",
                             color = "#7FFF7F")
    app.getPeriodManager().ajouter(periodeSemaine)

    # Création de tâches préfaites (c'est du lore)
    tacheA1 = Task("A1", periodeSemaine, "", "#F77CAA", datetime.datetime(2020, 7,  6,  8, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1))
    tacheA2 = Task("A2", periodeSemaine, "", "#42A69A", datetime.datetime(2020, 7,  6, 10, 0, 0), datetime.timedelta(0,0,0, 0, 0, 2))
    app.getTaskEditor().ajouter(Task("B",  periodeSemaine, "", "#7CF0F7", datetime.datetime(2020, 7,  8,  8, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1)))
    app.getTaskEditor().ajouter(Task("C",  periodeSemaine, "", "#C2F77C", datetime.datetime(2020, 7,  8, 10, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1)))
    app.getTaskEditor().ajouter(Task("D",  periodeSemaine, "", "#B97CF7", datetime.datetime(2020, 7, 12,  8, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1)))
    app.getTaskEditor().ajouter(Task("E",  periodeSemaine, "", "#5D7CDC", datetime.datetime(2020, 7, 12, 10, 0, 0), datetime.timedelta(3,0,0, 0, 0, 1)))
    app.getTaskEditor().ajouter(Task("F",  periodeSemaine, "", "#FA6FFF", datetime.datetime(2020, 7,  8, 12, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1)))
    app.getTaskEditor().ajouter(Task("Joyeux anniversaire", periodeSemaine,
                                "Gâteau au chocolat et ne pas oublier la crême anglaise", "#85FAB7",
                                datetime.datetime(2020, 7, 26, 12, 0, 0), datetime.timedelta(0,0,0, 0, 0, 5)))

    # Création d'un groupe préfait
    # Les 2 première tâches sont dans le groupe.
    group = Groupe("Mon Groupe", periodeSemaine, "description", "#FF88FF")
    group.addTask(tacheA1)
    group.addTask(tacheA2)
    periodeSemaine.getGroupeManager().ajouter(group)
    
    
    app.mainloop()
    try:
        app.destroy()
    except:
        pass
