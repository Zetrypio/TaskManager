# -*- coding: utf-8 -*-

from .AbstractLink import *

class MultiFrameItemInnerLink(AbstractLink):
    """
    Cette classe permet de faire un lien entre 2 AbstractItemContent() d'un même
    AbstractMultiFrameItem(), ayant plusieurs DatetimeItemPart()s. Le lien ne peut
    pas être supprimé, d'où sa différence principale avec le lien de dépendance.
    Les couleurs sont changées, aussi ; elles sont plus grise foncés.
    """
    def __init__(self, affichageGantt, partA, partB):
        """
        Constructeur du MultiFrameItemInnerLink.
        Les 2 parts données doivent être du même objet. (une vérification est faite).

        @param affichageGantt: Référence vers l'affichageGantt pour avoir
        des informations sur le positionnement des parts.
        @param partA: DatetimeItemPart qui correspond au moment du début de la flèche.
        @param partB: DatetimeItemPart qui correspond au moment de la fin de la flèche.
        """
        # Constructeur parent :
        super().__init__(affichageGantt, partA, partB)

        if partA.getSchedulable() != partB.getSchedulable():
            raise RuntimeError("Le lien doit commencer et terminer sur le même lien.")

        # TODO : tester lien déjà existant ?

    def redraw(self, canvas):
        """
        Méthode pour dessiner la flèche.
        @param canvas: tkinter.Canvas() sur lequel dessiner la flèche du lien.
        """
        # TODO : Couleur lors Ajout et Suppression.
        self.setColor("grey")
        self.setStrokeWeight(2)
        super().redraw(canvas)