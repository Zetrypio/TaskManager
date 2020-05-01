# -*- coding:utf-8 -*-
from .ToolBar import *

class PeriodToolBar(ToolBar):
    def __init__(self, master, periodeManager, **kwargs):
        self.periodeManager = periodeManager
        super().__init__(master, **kwargs)
    def _ajouterCategoriesEtBoutons(self):
        # CADRE Gestion des périodes
        self._creationCategorie("Gestion des périodes")
        # création des boutons
        self._creationBouton("Déplacer",                self.periodeManager.deplacerPeriode,   textVisible=True)
        self._creationBouton("Dupliquer",               self.periodeManager.dupliquerPeriode,  textVisible=True)
        self._creationBouton("Supprimer",               self.periodeManager.supprimerPeriode,  textVisible=True)
        # CADRE Division des périodes
        self._creationCategorie("Division des périodes")
        # création des boutons
        self._creationBouton("Scinder",                 self.periodeManager.scinderPeriode,    textVisible=True)
        self._creationBouton("Fusionner",               self.periodeManager.fusionnerPeriodes, textVisible=True)
        # CADRE Tâches indépendantes
        self._creationCategorie("Tâches indépendantes")
        # création des boutons
        self._creationBouton("Lier à une période",      self.periodeManager.lierTachePeriode,  textVisible=True)
        self._creationBouton("Voir dans une autre vue", self.master.voirTacheDansVue,          textVisible=True)
        self._creationBouton("Supprimer",               self.master.supprimerTache,            textVisible=True)
        

