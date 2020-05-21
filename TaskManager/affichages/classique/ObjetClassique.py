# -*- coding:utf-8 -*-
from ..item.AbstractMultiFrameItem import *

class ObjetClassique(AbstractMultiFrameItem):
    """
    Classe représentant un contenu dans
    l'affichage calendrier classique.
    """
    def __init__(self, master, schedulable):
        """
        Constructeur d'un objet classique.
        """
        super().__init__(master, schedulable)

    def redraw(self, frame):
        # On se supprime :
        self.delete()
        
        # Et on se redessine :
        for part in self.getRepartition():
            # Si la partie est visible :
            if self.isPartVisible(part):
                # On crée le cadre
                f = Frame(frame, bg=self._schedulable.getColor())
                
                self._schedulable.createDisplayableInstance(frame, part)
                
                # On le place :
                temps1 = (part.getHeureDebut() - self.master.getHeureDebut())
                temps2 = (part.getHeureFin()   - self.master.getHeureDebut())

                ligne1 = temps1.hour * 60 + temps1.minute
                ligne2 = temps2.hour * 60 + temps2.minute

                lignespan = ligne2 - ligne1

                colonne = self.getPartPosition(part)
                colonnespan = self.getPartSpan(part)

                f.grid(row = ligne1, rowspan = lignespan, column = colonne, columnspan = colonnespan)

                # On le mémorise :
                self._listeCadre.append(f)
    
    def delete(self):
        for f in self._listeCadre:
            try:
                f.destroy()
            except:
                pass
        self._listeCadre = []