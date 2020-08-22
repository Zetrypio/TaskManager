# -*- coding:utf-8 -*-
from util.UndoRedo import *
from ..Periode import *

class UndoRedoPeriodCreation(UndoRedo):
    def __init__(self, period):
        # Super Constructor and Action Info :
        super().__init__("Créer une période")

        # Data :
        self.data       = period.saveByDict()
        self.ID_periode = period.getUniqueID()

        # Application & Other :
        self.app            = period.getApplication()
        self.periodeManager = self.app.getPeriodManager()

    def _undo(self):
        # Get Period :
        periode = self.periodeManager.getByUniqueID(self.ID_periode)

        # Operate :
        self.periodeManager.supprimer(periode)

        # Update is Auto in PeriodManager.

    def _redo(self):
        # Nothing to Get.

        # Operate :
        periode = Periode.load(self.data, self.periodeManager)
        self.periodeManager.ajouter(periode)

        # Update is Auto in PeriodManager.