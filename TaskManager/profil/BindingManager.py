# *-* conding:utf-8 *-*

NOMFICHIER = "binding"

class BindingManager:
    def __init__(self, app):
        """
        Classe qui s'occupe de gére les bindings
        """

        self.__app = app

    def bindingInsertToi(self, t):
        """
        Fonction qui permet pour chaque binding de d'inséré dans le treeview
        @param t : <treeveiw> sur lequel les binding doivent aller
        """
        pass

    def getData(self):
        return self.__app.getData()
