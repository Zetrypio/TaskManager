#*-* coding:UTF-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
from importPIL import *
from espacevisuel import *
from taskEditor import *

style = Style()


# CECI est la CORRECTION d'un BUG :
def fixed_map(option):
    # Returns the style map for 'option' with any styles starting with
    # ("!disabled", "!selected", ...) filtered out

    # style.map() returns an empty list for missing options, so this should
    # be future-safe
    return [elm for elm in style.map("Treeview", query_opt=option)
            if elm[:2] != ("!disabled", "!selected")]

style.map("Treeview",
          foreground=fixed_map("foreground"),
          background=fixed_map("background"))

class MenuBar(Menu):
    def __init__(self, root, master):
        Menu.__init__(self, master)
        root.configure(menu = self)
        # Menus Principaux :
        self.menuFichier = Menu(self, tearoff=0)
        self.menuEdition = Menu(self, tearoff=0)
        self.menuAffichage = Menu(self, tearoff=0)
        
        self.add_cascade(label = "Fichier", menu=self.menuFichier)
        self.add_cascade(label = "Edition", menu=self.menuEdition)
        self.add_cascade(label = "Affichage", menu=self.menuAffichage)

        # Menu Fichier :
        self.menuFichier.add_command(label = "Nouveau", accelerator="Ctrl-N", command = master.nouveau)
        self.menuFichier.add_command(label = "Ouvrir", accelerator="Ctrl-O", command = master.nouveau)
        self.menuFichier.add_separator()
        self.menuFichier.add_command(label = "Enregistrer", accelerator="Ctrl-S", command = master.nouveau)
        self.menuFichier.add_command(label = "Enregistrer sous", accelerator="Ctrl-Maj-S", command = master.nouveau)
        self.menuFichier.add_separator()
        self.menuFichier.add_command(label = "Quitter", accelerator="Ctrl-Q", command = master.nouveau)

        # Menu Affichage/Style Horloge :
        self.variableHorlogeStyle = StringVar(value="nombre")
        self.menuHorlogeStyle = Menu(self.menuAffichage, tearoff=0)
        self.menuHorlogeStyle.add_radiobutton(label = "Normal", command = master.nouveau, variable=self.variableHorlogeStyle, value = "normal")
        self.menuHorlogeStyle.add_radiobutton(label = "Nombre", command = master.nouveau, variable=self.variableHorlogeStyle, value = "nombre")

        # Menu Affichage :
        self.menuAffichage.add_cascade(label = "Style d'horloge", menu = self.menuHorlogeStyle)



class Application(Frame):
    def __init__(self, master = None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.winfo_toplevel().title("Gestionnaire de calendrier")
        self.menu = MenuBar(self.master, self)
        self.taskEditor = TaskEditor(self, self.menu)
        self.taskEditor.pack(side=LEFT, fill = BOTH, expand = NO)
        self.calendar = CalendarZone(self)
        self.calendar.pack(side=LEFT, fill = BOTH, expand = YES)
    def nouveau(self):pass
    def getPanneauActif(self):
        return self.calendar.getPanneauActif()
    def getDonneeCalendrier(self):
        return self.calendar.getDonneeCalendrier()



def main():
    """Fonction main, principale du programme."""
    app = Application()
    app.pack(expand = YES, fill = BOTH)
    
    # Création de taches préaite
    app.taskEditor.ajouter(Task("A", datetime.datetime(2020, 4, 6, 8, 0, 8), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#F77CAA"))
    app.taskEditor.ajouter(Task("B", datetime.datetime(2020, 4, 8, 8, 0, 8), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#7CF0F7"))
    app.taskEditor.ajouter(Task("C", datetime.datetime(2020, 4, 8, 10, 0, 8), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#C2F77C"))
    app.taskEditor.ajouter(Task("D", datetime.datetime(2020, 4, 12, 8, 0, 8), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#B97CF7"))
    app.taskEditor.ajouter(Task("E", datetime.datetime(2020, 4, 12, 10, 0, 8), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#5D7CDC"))
    app.taskEditor.ajouter(Task("F", datetime.datetime(2020, 4, 8, 12, 0, 8), datetime.timedelta(0,0,0, 0, 0, 1),-1,0,"","#FA6FFF"))
    app.taskEditor.ajouter(Task("Joyeux anniversaire", datetime.datetime(2020, 4, 26, 12, 0, 8), datetime.timedelta(0,0,0, 0, 0, 5),-1,0,"Gateau au chocolat et ne pas oublier la crême anglaise","#85FAB7"))
    
    app.mainloop()
    try:
        app.destroy()
    except:
        pass


if __name__=='__main__':
    main()
