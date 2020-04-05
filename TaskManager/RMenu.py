try:from Tkinter import Menu
except:from tkinter import Menu
class RMenu(Menu):
    def __init__(self, master = None, andInside = False, binder = None, **args):
        try:del args["tearoff"]
        except:pass
        if not binder:
            binder = master
        if not hasattr(master, "tk"):
            master = master.canvas
        self.binder = binder
        Menu.__init__(self, master, tearoff=0, **args)
        self.binder.bind("<Button-3>", self.right_menu_event)
        self.__bind_inside_of(binder)

    def __bind_inside_of(self, widget):
        widget.bind("<Button-3>", self.right_menu_event)
        try:
            subwidget = widget.slaves()
        except:
            return
        for w in subwidget:
            self.__bind_inside_of(w)

    def right_menu_event(self, event):
        self.event_generate("<<RMenu-Opened>>")
        self.tk_popup(event.x_root, event.y_root)

