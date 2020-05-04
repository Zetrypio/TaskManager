

class TaskEditorDisplayableObject:
    def __init__(self):
        if self.__class__ == TaskEditorDisplayableObject:
            raise RuntimeError("Impossible d'instancier TaskEditorDisplayableObject directement")
    def iterateContent(self):
        if False:yield