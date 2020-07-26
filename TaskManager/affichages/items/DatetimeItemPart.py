# -*- coding:utf-8 -*-
import datetime

class DatetimeItemPart:
    """
    Méthode représentant une portion de temps,
    en l'occurence une portion de tâche, groupe ou autres.
    Une datetimeItemPart ne peut être présent que sur un seul jour.
    """
    def __init__(self, jour, heureDebut, heureFin, schedulable):
        """
        Constructeur d'un DatetimeItemPart.
        @param jour: datetime.date() correspondant au seul et unique jour que cette part peut prendre.
        @param heureDebut: datetime.time() correspondant à l'heure du début de cette part.
        @param heureFin:   datetime.time() correspondant à l'heure de fin   de cette part.
        """
        assert isinstance(jour,       datetime.date)
        assert isinstance(heureDebut, datetime.time)
        assert isinstance(heureFin,   datetime.time)
        self.__heureDebut  = heureDebut
        self.__heureFin    = heureFin
        self.__jour        = jour
        self.__schedulable = schedulable

    def __eq__(self, other):
        """
        /!\ SURCHARGE DE L'OPÉRATEUR "==" /!\.
        Permet de faire le test d'égalité selon les états des DatetimeItemPart()s.
        TOUT LES ATTRIBUTS SONT TESTÉS.
        @param other: l'autre DatetimeItemPart() dont on teste l'égalité.
        @return True si les états de ces 2 objets sont égaux, False sinon
        @return NotImplemented si other n'est pas un DatetimeItemPart().
        """
        if isinstance(other, DatetimeItemPart):
            return (self.__heureDebut  == other.__heureDebut
                and self.__heureFin    == other.__heureFin
                and self.__jour        == other.__jour
                and self.__schedulable == other.__schedulable)
        return NotImplemented

    def __hash__(self):
        """
        Renvoie hash(self).
        Doit être redéfini car la méthode #__eq__() est redéfinie et qu'on va utiliser cet objet dans un set().
        Doit renvoyer un nombre le plus unique possible pour chaque instance en fonction de ses attributs.
        @return hash(self.__schedulable)
        """
        return hash(self.__schedulable)

    "" # Marque pour le repli de code
    #############
    # Getters : #
    #############
    ""
    def getDebut(self):
        """
        Getter pour le début de la part.
        @return datetime.datetime() qui combine le jour et l'heure de début de cette part.
        """
        return datetime.datetime.combine(self.__jour, self.__heureDebut)
    
    def getFin(self):
        """
        Getter pour la fin de la part.
        @return datetime.datetime() qui combine le jour et l'heure de fin de cette part.
        """
        return datetime.datetime.combine(self.__jour, self.__heureFin)
    
    def getHeureDebut(self):
        """
        Getter pour l'heure de début de la part.
        @return datetime.time() qui correspond à l'heure du début de cette part.
        """
        return self.__heureDebut
    
    def getHeureFin(self):
        """
        Getter pour l'heure de fin de la part.
        @return datetime.time() qui correspond à l'heure du fin de cette part.
        """
        return self.__heureFin

    def getJour(self):
        """
        Getter pour le jour qui est contenu dans cette part.
        @return datetime.date() qui correspond à une copie du jour contenu par cette part.
        """
        return self.__jour + datetime.timedelta()

    def getSchedulable(self):
        """
        Getter pour le AbstractSchedulableObject qui à instancié ce DatetimeItemPart.
        @return l'AbstractSchedulableObject qui à instancié cet part.
        """
        return self.__schedulable
    
    def intersectWith(self, other):
        """
        Permet de savoir si cette part se situe partiellement en même temps qu'un autre.
        @param other: l'autre part à tester avec celle-ci.
        @return True si les 2 parts sont partiellement en même temps,
        @return False sinon.
        """
        return self.getJour() == other.getJour() and\
            not (other.getHeureDebut() > self.getHeureFin()
              or other.getHeureFin()  <  self.getHeureDebut())
