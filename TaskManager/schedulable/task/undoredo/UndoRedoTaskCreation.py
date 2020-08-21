# -*- coding:utf-8 -*-
from util.UndoRedo import *
from ..Task import *

class UndoRedoTaskCreation(UndoRedo):
    def __init__(self, taskEditor, task):
        super().__init__("Créer une tâche")
        self.taskEditor = taskEditor
        self.data = task.saveByDict()
        self.task = task
        self.idPeriode = task.getPeriode().getUniqueID()
        self.periodeManager = task.getPeriode().getPeriodeManager()

    def _undo(self):
        print("undo creation task")
        self.task.delete()
        self.taskEditor.redessiner()
        self.taskEditor.getApplication().getDonneeCalendrier().updateAffichage(True)
        self.task = None

    def _redo(self):
        print("redo creation task")
        self.task = Task.load(self.data, self.periodeManager.getByUniqueID(self.idPeriode))
        self.taskEditor.ajouter(self.task)
