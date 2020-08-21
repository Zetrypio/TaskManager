# -*- coding:utf-8 -*-
from util.UndoRedo import *

class UndoRedoTaskDeleting(UndoRedo):
    def __init__(self, task):
        # Super Constructor and Action Info :
        super().__init__("Supprimer une tâche")

        # Data :
        self.data       = task.saveByDict()
        self.ID_task    = task.getUniqueID()
        self.ID_periode = task.getPeriode().getUniqueID()

        # Application & Other :
        self.app            = task.getApplication()
        self.periodeManager = self.app.getPeriodManager()

    def _undo(self):
        # Debug & Import :
        from ..Task import Task
        print("undo deleting task")

        # Get Period :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)

        # Operate :
        task = Task.load(self.data, periode)

        # Update :
        self.app.getTaskEditor().ajouter(task)

    def _redo(self):
        # Debug :
        print("undo creation task")

        # Get Period & Task :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)
        task    = periode.getByUniqueID(self.ID_task)
        
        # Operate :
        task.delete()

        # Update :
        self.app.getTaskEditor().redessiner()
        self.app.getDonneeCalendrier().updateAffichage(True)
