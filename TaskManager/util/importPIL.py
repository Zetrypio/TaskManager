# -*- coding:utf-8 -*-
import sys, os
try:
    from PIL import Image, ImageTk
except:
    ## faudra faire des essais avec ça : (ca marche pas en l'etat)
    ##if len(sys.argv) < 2:
    ##   sys.argv.append("install")
    #sys.argv[1:1] = "install"
    #from setuptools import setup
    #setup(install_requires=['Pillow'])
    if sys.platform.startswith("win"):
        pip = "py -3.8 -m pip"
#        pip = sorted(i for i in sys.path if i) # trier et enlever le ''
#        if any(p[0].islower() for p in pip):   # dans la console et dans le shell, il y a des différences entre 'c:\\python27...' et 'C:\\python27...'
#            pip = [p for p in pip if p[0].islower()]
#        pip = pip[0]
#        pip = pip+"\\Scripts\\pip"
#        #print pip #debug
#        pip = '"'+pip+'"'
    else:
        pip = "python3 -m pip"
    print(pip + " install --user Pillow --upgrade")
    os.system(pip + " install --user Pillow --upgrade")
    try:
        from PIL import Image, ImageTk
    except:
        ext = '"'+ '" "'.join(sys.argv[1:]) + '"' if len(sys.argv[1:]) else ""
        input("**Appuyez sur entrer pour continuer**")
        print("start py -3.8 Application.pyw " + ext)
        os.system("py -3.8 Application.pyw " + ext)
        exit()

IMAGES = {} # dictionnaire des images charg�es (mieux vaut utiliser la fonction getImage())
def getImage(imageName):
    """
    Manière sécurisé d'obtenir les images sans problèmes
    (on ne doit pas charger 2 fois la même image).
    """
    if not imageName in IMAGES:
        IMAGES[imageName] = ImageTk.PhotoImage(Image.open(imageName))
    return IMAGES[imageName]

__all__ = ("getImage",)
