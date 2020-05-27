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
        @return True si les 2 parts sont partiellements en même temps,
        @return False sinon.
        """
        return self.getJour() == other.getJour() and\
            not (other.getHeureDebut() > self.getHeureFin()
              or other.getHeureFin()  <  self.getHeureDebut())
