# -*- coding:utf-8 -*-

from util.UndoRedo import *

class UndoRedoChangerPeriode(UndoRedo):
    def __init__(self, period1, period2, periodManager):
        # Super Constructor and Action Info :
        super().__init__("Changer de période")

        # Data :
        self.ID_periode1 = period1.getUniqueID() if period1 is not None else None
        self.ID_periode2 = period2.getUniqueID() if period2 is not None else None

        # Application & Other :
        self.periodeManager = periodManager

    def _undo(self):
        # Get Period :
        periode1 = self.periodeManager.getByUniqueID(self.ID_periode1)

        # Operate :
        self.periodeManager.setActivePeriode(periode1)

        # Update is Auto in PeriodManager.

    def _redo(self):
        # Get Period :
        periode2 = self.periodeManager.getByUniqueID(self.ID_periode2)

        # Operate :
        self.periodeManager.setActivePeriode(periode2)

        # Update is Auto in PeriodManager.
