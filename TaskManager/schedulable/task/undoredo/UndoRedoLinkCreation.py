# -*- coding:utf-8 -*-

from util.UndoRedo import *

class UndoRedoLinkCreation(UndoRedo):
    """
    Undo-Redo de création de lien.
    """
    def __init__(self, taskA, taskB):
        # Super Constructor and Action Info :
        super().__init__("Créer un lien")

        # Data :
        self.ID_taskA   = taskA.getUniqueID()
        self.ID_taskA_P = taskA.getParent().getUniqueID() if taskA.getParent() else None
        self.ID_taskB   = taskB.getUniqueID()
        self.ID_taskB_P = taskB.getParent().getUniqueID() if taskB.getParent() else None
        self.ID_periode = taskA.getPeriode().getUniqueID() # Ils ont forcément la même période

        # Application & Other :
        self.app            = taskA.getApplication()
        self.periodeManager = self.app.getPeriodManager()

    def _undo(self):
        # Get Period & Tasks :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)
        taskA   = periode.getByUniqueID(self.ID_taskA)
        if taskA is None:
            taskA_P = periode.getByUniqueID(self.ID_taskA_P)
            for task in taskA_P.getSubTasks():
                if task.getUniqueID() == self.ID_taskA:
                    taskA = task
                    break
        taskB   = periode.getByUniqueID(self.ID_taskB)
        if taskB is None:
            taskB_P = periode.getByUniqueID(self.ID_taskB_P)
            for task in taskB_P.getSubTasks():
                if task.getUniqueID() == self.ID_taskB:
                    taskB = task
                    break
        
        # Operate :
        taskA.removeDependance(taskB)

        # Update :
        self.app.getTaskEditor().redessiner()
        self.app.getDonneeCalendrier().updateAffichage(True)

    def _redo(self):
        # Get Period & Tasks :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)
        taskA   = periode.getByUniqueID(self.ID_taskA)
        taskB   = periode.getByUniqueID(self.ID_taskB)
        if taskA is None:
            taskA_P = periode.getByUniqueID(self.ID_taskA_P)
            for task in taskA_P.getSubTasks():
                if task.getUniqueID() == self.ID_taskA:
                    taskA = task
                    break
        taskB   = periode.getByUniqueID(self.ID_taskB)
        if taskB is None:
            taskB_P = periode.getByUniqueID(self.ID_taskB_P)
            for task in taskB_P.getSubTasks():
                if task.getUniqueID() == self.ID_taskB:
                    taskB = task
                    break

        # Operate :
        taskA.addDependance(taskB)

        # Update :
        self.app.getTaskEditor().redessiner()
        self.app.getDonneeCalendrier().updateAffichage()
