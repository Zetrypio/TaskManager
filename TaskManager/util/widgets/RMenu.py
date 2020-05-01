from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

class RMenu(Menu):
    def __init__(self, master = None, andInside = False, binder = None, bindWithId = None, **args):
        try:del args["tearoff"]
        except:pass
        if not binder:
            binder = master
        if not hasattr(master, "tk"):
            master = master.canvas
        self.binder = binder
        Menu.__init__(self, master, tearoff=0, **args)
        self.__bindWithId = bindWithId
        if bindWithId is None:
            self.__binding = self.binder.bind("<Button-3>", self.right_menu_event)
            self.__bind_inside_of(binder)
        else:
            self.__binding = self.binder.tag_bind(bindWithId, "<Button-3>", self.right_menu_event)

    def __bind_inside_of(self, widget):
        widget.bind("<Button-3>", self.right_menu_event)
        try:
            subwidget = widget.slaves()
        except:
            return
        for w in subwidget:
            self.__bind_inside_of(w)

    def right_menu_event(self, event):
        self.event_generate("<<RMenu-Opened>>", x = event.x, y = event.y, rootx = event.x_root, rooty = event.y_root)
        self.tk_popup(event.x_root, event.y_root)
    
    def destroy(self):
        try:
            self.binder.unbind(self.__binding)
        except:
            pass
        Menu.destroy(self)
