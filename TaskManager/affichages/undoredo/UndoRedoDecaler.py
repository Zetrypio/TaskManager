# -*- coding:utf-8 -*-
from util.UndoRedo import *

class UndoRedoDecaler(UndoRedo):
    def __init__(self, periode, mapIDBeginTaskBefore, mapIDBeginTaskAfter):
        """
        @param mapIDSavedTaskBefore: un dictionnaire qui map l'UniqueID d'une
        tâche déplacé avec sa date d'avant le déplacement.
        @param mapIDSavedTaskAfter:  un dictionnaire qui map l'UniqueID d'une
        tâche déplacé avec sa date d'après le déplacement.
        """
        # Super Constructor and Action Info :
        super().__init__("Décaler")

        # Data :
        self.mapIDBeginTaskBefore = mapIDBeginTaskBefore
        self.mapIDBeginTaskAfter  = mapIDBeginTaskAfter
        self.ID_periode = periode.getUniqueID()

        # Application & Other :
        self.app            = periode.getApplication()
        self.periodeManager = self.app.getPeriodManager()

    def _undo(self): # TODO: groups ?
        # Get Period :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)

        # Do for each Tasks :
        for ID_task in self.mapIDBeginTaskAfter:
            task = periode.getByUniqueID(ID_task)

            # Change to Before :
            task.setDebut(self.mapIDBeginTaskBefore[ID_task])
        
        # Update affichage :
        self.app.getDonneeCalendrier().updateAffichage(True)
        self.app.getTaskEditor().redessiner()

    def _redo(self): # TODO: groups ?
        # Get Period :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)

        # Do for each Tasks :
        for ID_task in self.mapIDBeginTaskBefore:
            task = periode.getByUniqueID(ID_task)

            # Change to Before :
            task.setDebut(self.mapIDBeginTaskAfter[ID_task])
        
        # Update affichage :
        self.app.getDonneeCalendrier().updateAffichage(True)
        self.app.getTaskEditor().redessiner()
