# -*- coding:utf-8 -*-
from util.UndoRedo import *
from ..Task import *

class UndoRedoTransformTaskToDnD(UndoRedo):
    def __init__(self, task):
        # Super Constructor and Action Info :
        super().__init__("Transformer une tâche en tâche déplaçable")

        # Data :
#        self.data       = task.saveByDict()
        self.ID_task    = task.getUniqueID()
        self.ID_parent  = task.getParent().getUniqueID()
        self.ID_periode = task.getPeriode().getUniqueID()

        # Application & Other :
        self.app            = task.getApplication()
        self.taskEditor     = self.app.getTaskEditor()
        self.periodeManager = self.app.getPeriodManager()

    def _undo(self):
        # Get Period & Task :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)
        parent  = periode.getByUniqueID(self.ID_parent)
        task    = next(t for t in parent.getSubTasks() if t.getUniqueID() == self.ID_task)

        # Operate :
        periode.removePrimitiveSchedulable(parent) # Attention ne pas utiliser delete sur la tâche, car ça supprimer les sous-tâches.
        task._Task__parent = None # TODO Corriger : TRÈS MOCHE d'accéder à un attribut privé...
        periode.addPrimitiveSchedulable(task)

        # Update :
        self.app.getTaskEditor().redessiner()

    def _redo(self):
        # Get Period & task:
        periode = self.periodeManager.getByUniqueID(self.ID_periode)
        task = periode.getByUniqueID(self.ID_task)

        # Operate :
        task.transformToDnd(self.taskEditor) # TODO : obtenir le taskEditor

        # Update :
        self.ID_parent  = task.getParent().getUniqueID()
