# *-* coding:utf-8 *-*
from util.UndoRedo import *

class UndoRedoTaskEditing(UndoRedo):
    def __init__(self, taskUndo, task):
        # Super Constructor and Action Info :
        super().__init__("Éditer une tâche.")

        # Data :
        self.undoData   = taskUndo
        self.redoData   = task.saveByDict()
        self.ID_task    = task.getUniqueID()
        self.ID_periode = task.getPeriode().getUniqueID()

        # Application & Other :
        self.app            = task.getApplication()
        self.periodeManager = self.app.getPeriodManager()

    def _undo(self):
        from ...Task import Task
        # Get Period & Task :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)
        task    = periode.getByUniqueID(self.ID_task)
        
        # Operate :
        newTask = Task.load(self.undoData, periode)

        periode.addCopiedTask(newTask, task)

        # Update :
        task.delete()
        self.app.getDonneeCalendrier().updateAffichage(True)

    def _redo(self):
        from ...Task import Task
        # Get Period & Task :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)
        task    = periode.getByUniqueID(self.ID_task)

        # Operate :
        newTask = Task.load(self.redoData, periode)

        periode.addCopiedTask(newTask, task)

        # Update :
        task.delete()
        #self.app.getTaskEditor().ajouter(newTask)
        self.app.getDonneeCalendrier().updateAffichage(True)
