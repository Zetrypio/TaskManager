# *-* coding:utf-8 *-*

class Data:
    def __init__(self):
        # Création des attributs
        self.__affichageNombreHorloge = True

    def getAffichageNombreHorloge(self):
        """ getter de l'affichage lié aux nombre sur les bords de l'horloge """
        return self.__affichageNombreHorloge

    def setAffichageNombreHorloge(self, value):
        """
        Setter de l'affichage lié aux nombre sur les bords de l'horloge
        @param valeur : <Bool> True = nombre, False = pas de nombre
        """
        if not isinstance(value, bool):
            raise TypeError("Exptected a boolean")
        self.__affichageNombreHorloge = value


