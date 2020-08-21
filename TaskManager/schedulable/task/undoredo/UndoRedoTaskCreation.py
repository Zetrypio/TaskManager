# -*- coding:utf-8 -*-
from util.UndoRedo import *

class UndoRedoTaskCreation(UndoRedo):
    def __init__(self, taskEditor, task):
        super().__init__("Créer une tâche")
        self.taskEditor = taskEditor
        self.data = task.saveByDict()
        self.task = task

    def _undo(self):
        print("undo creation task")
        self.task.delete()
        self.taskEditor.redessiner()
        self.taskEditor.getApplication().getDonneeCalendrier().updateAffichage(True)
        self.task = None

    def _redo(self):
        print("redo creation task")
        pass