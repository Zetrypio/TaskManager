# -*- coding:utf-8 -*-

from util.UndoRedo import *

class UndoRedoLinkDeleting(UndoRedo):
    """
    Undo-Redo de suppression de lien.
    """
    def __init__(self, taskA, taskB):
        # Super Constructor and Action Info :
        super().__init__("Supprimer un lien")

        # Data :
        self.ID_taskA   = taskA.getUniqueID()
        self.ID_taskB   = taskB.getUniqueID()
        self.ID_periode = taskA.getPeriode().getUniqueID() # Ils ont forcément la même période

        # Application & Other :
        self.app            = taskA.getApplication()
        self.periodeManager = self.app.getPeriodManager()

    def _undo(self):
        # Get Period & Tasks :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)
        taskA   = periode.getByUniqueID(self.ID_taskA)
        taskB   = periode.getByUniqueID(self.ID_taskB)
        
        # Operate :
        taskA.addDependance(taskB)

        # Update :
        self.app.getTaskEditor().redessiner()
        self.app.getDonneeCalendrier().updateAffichage()

    def _redo(self):
        # Get Period & Tasks :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)
        taskA   = periode.getByUniqueID(self.ID_taskA)
        taskB   = periode.getByUniqueID(self.ID_taskB)

        # Operate :
        taskA.removeDependance(taskB)

        # Update :
        self.app.getTaskEditor().redessiner()
        self.app.getDonneeCalendrier().updateAffichage(True)
