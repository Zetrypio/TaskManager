# -*- coding:utf-8 -*-
from util.UndoRedo import *

class UndoRedoIntervertirJours(UndoRedo):
    def __init__(self, setDay1, setDay2, timedelta, periode):
        """
        @param setDay1: ensemble des objets du premier jour.
        @param setDay2: ensemble des objets du second jour.
        @param timedelta: écart de temps entre les 2 jours.
        """
        # Super Constructor and Action Info :
        super().__init__("Intervertir jours")

        # Data :
        self.setIDTaskDay1 = {obj.getUniqueID() for obj in setDay1 - setDay2} # pour être sûr
        self.setIDTaskDay2 = {obj.getUniqueID() for obj in setDay2 - setDay1} # aussi
        self.timedelta = timedelta
        self.ID_periode = periode.getUniqueID()

        # Application & Other :
        self.app            = periode.getApplication()
        self.periodeManager = self.app.getPeriodManager()

    def _undo(self):
        # Get Period :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)

        # Do for each Tasks of day 1:
        for ID_task in self.setIDTaskDay1:
            # Get the task :
            task = periode.getByUniqueID(ID_task)

            # Change the task :
            task.setDebut(task.getDebut() - self.timedelta)

        # Do for each Tasks of day 2:
        for ID_task in self.setIDTaskDay2:
            # Get the task :
            task = periode.getByUniqueID(ID_task)

            # Change the task :
            task.setDebut(task.getDebut() + self.timedelta)
        
        # Update affichage :
        self.app.getDonneeCalendrier().updateAffichage(True)
        self.app.getTaskEditor().redessiner()

        # Fire event :
        for p in self.app.getDonneeCalendrier().getToutLesPanneaux():
            p.onIntervertir()

    def _redo(self):
        # Get Period :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)

        # Do for each Tasks of day 2:
        for ID_task in self.setIDTaskDay2:
            # Get the task :
            task = periode.getByUniqueID(ID_task)

            # Change the task :
            task.setDebut(task.getDebut() - self.timedelta)

        # Do for each Tasks of day 1:
        for ID_task in self.setIDTaskDay1:
            # Get the task :
            task = periode.getByUniqueID(ID_task)

            # Change the task :
            task.setDebut(task.getDebut() + self.timedelta)
        
        # Update affichage :
        self.app.getDonneeCalendrier().updateAffichage(True)
        self.app.getTaskEditor().redessiner()

        # Fire event :
        for p in self.app.getDonneeCalendrier().getToutLesPanneaux():
            p.onIntervertir()
