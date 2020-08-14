# -*- coding: utf-8 -*-

from .AbstractLink import *

from util.widgets.infobulle import *

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

        #if partA.getSchedulable() != partB.getSchedulable():    # Pas dans le cas des groupes en fait...
            #raise RuntimeError("Le lien doit commencer et terminer sur le même objet planifiable.")

        # TODO : tester lien déjà existant ?

    "" # Marque pour le repli de code
    #############
    # Getters : #
    #############
    ""
    def isSelected(self):
        return self.getPartA().getSchedulable().isSelected()

    ""
    #############
    # Setters : #
    #############
    ""
    def __setColor(self):
        """
        Méthode qui permet de mettre la bonne couleur selon ce qu'il y a besoin.
        """
        # TODO : Couleur lors Ajout et Suppression.
        if self.isSelected():
            self.setColor(self.getPalette()["selected"]) # old : "#0078FF"
            self.setStrokeWeight(3)
        else:
            self.setColor(self.getPalette()["normalInnerLink"]) # old : "grey"
            self.setStrokeWeight(2)

    ""
    ##################################
    # Méthodes liées à l'affichage : #
    ##################################
    ""
    def redraw(self, canvas):
        """
        Méthode pour dessiner la flèche.
        @param canvas: tkinter.Canvas() sur lequel dessiner la flèche du lien.
        """
        self.__setColor()
        self.setStrokeWeight(2)
        super().redraw(canvas)

        # Ajouter infobulle :
        ajouterInfoBulleTagCanvas(canvas, self.getTag(), str(self.getPartA().getSchedulable()))

    def updateColor(self, canvas):
        self.__setColor()
        super().updateColor(canvas)

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def _onClic(self):
        self._getAffichageGantt().cancelEvent()
        self._getAffichageGantt().deselectEverything()
        self.getPartA().getSchedulable().setSelected(True)
        self._getAffichageGantt().getDonneeCalendrier().updateColor()

    def _onControlClic(self):
        self._getAffichageGantt().cancelEvent()
        self.getPartA().getSchedulable().inverseSelection()
        self._getAffichageGantt().getDonneeCalendrier().updateColor()
