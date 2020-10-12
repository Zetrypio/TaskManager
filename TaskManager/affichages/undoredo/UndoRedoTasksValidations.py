# -*- coding:utf-8 -*-
from util.UndoRedo import *

class UndoRedoTasksValidations(UndoRedo):
    def __init__(self, tasks, mode = "Manuelle"):
        # Super Constructor and Action Info :
        nom = "Valider une tâche"
        if mode == "Manuelle":
            if len(tasks) > 1:
                nom = "Valider plusieurs tâches"
        elif mode == "Normal":
            nom = "Valider les tâches jusqu'à maintenant"
        elif mode == "Jour Fini":
            nom = "Valider les tâches d'aujourd'hui"
        super().__init__(nom)

        # Data :
        self.ID_tasks   = [task.getUniqueID() for task in tasks]
        self.ID_periode = tasks[0].getPeriode().getUniqueID() # Toutes les tâches sont forcément de la même période.

        # Application & Other :
        self.app            = tasks[0].getApplication()
        self.periodeManager = self.app.getPeriodManager()

    def _undo(self):
        # Get Period & Tasks :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)

        for task_ID in self.ID_tasks:
            task = periode.getByUniqueID(task_ID)

            # Operate :
            task.setDone(False)

        # Update :
        self.app.getTaskEditor().redessiner()

    def _redo(self):
        # Get Period & Tasks :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)

        for task_ID in self.ID_tasks:
            task = periode.getByUniqueID(task_ID)

            # Operate :
            task.setDone(True)

        # Update :
        self.app.getTaskEditor().redessiner()