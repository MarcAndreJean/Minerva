#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projet          : Editeur, Compilateur et Micro-Ordinateur pour
                      un langage assembleur.
    Nom du fichier  : 01-05-TextCin.py

    Identification  : 01-05-TextCin
    Titre           : Widget : Texte pour console input
    Auteurs         : Marc-André Jean
    Date            : 16-04-2017
    Description     : Un widget Tk qui représente une entrée console (keyboard).


    Le module ``TextCin``
    ================================

    Ce module contient une classe nommée « TextCin » qui est un widget similaire
    à Text mais modifié pour permettre le contrôle des entrées du clavier. Il
    s'agit d'un Widget qui n'existe pas dans la bibliothèque de Tkinter
    (Python).


"""

__author__ = "Marc-Andre Jean"
__version__ = "1.0"
__status__ = "Production"

# Importation des modules nécessaires.
try:
    modEnum = __import__("05-Enum")
except ImportError:
    import importlib
    modEnum = importlib.import_module("Modules.05-Enum")
# Redéfinition.
intTOascii = modEnum.intTOascii

# Importation de Tkinter selon la version de Python.
# Python 2 seulement:
try:
    from Tkinter import *
    import ttk as ttk
# Python 2 et 3 (Python 2 après ''pip install future''):
except ImportError:
    from tkinter import *
    import tkinter.ttk as ttk


class TextCin(Text):
    """
        TextCin est tout simplement un Widget Text auquel nous contrôlons et
        gèrons les entrées clavier avec une whitelist.

        :example:
        >>> test = TextCin()

    """

    def __init__(self, *args, **kwargs):
        """
            Constructeur de TextCin.

            Le constructeurs prend en argument *args et **kwargs pour
            une construction plus complexe du Text si désiré.

            :example:
            >>> test = TextCin()

        """
        self.haveToUpdate = False
        self.lastkey = ''
        self.lastText = '.' * 255
        # Initialisation de Text avec les arguments.
        Text.__init__(self, *args, **kwargs)
        self.insert(END, self.lastText)

        # Création de l'évènement <<change>> lorsqu'il y des mofications dans
        # le widget texte. Le code en commentaire n'est pas du code Python mais
        # du code Tcl (Tck/Tk).
        self.tk.eval('''
            proc widget_proxy {widget widget_command args} {

                # On fait un appel avec le vrai tk Widget avec ces args.
                set result [uplevel [linsert $args 0 $widget_command]]

                # On génère les évènements pour les différents types
                # de commandes.
                if {([lindex $args 0] in {insert replace delete}) ||
                    ([lrange $args 0 2] == {mark set insert}) } {

                    event generate  $widget <<Change>> -when tail
                }

                # On retourne le résultat.
                return $result
            }
            ''')
        self.tk.eval('''
            rename {widget} _{widget}
            interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
        '''.format(widget=str(self)))

        # Bind.
        self.bind('<<Change>>', self.afterRefresh)
        # Fin.
        return

    def afterRefresh(self, event):
        """
            Fonction qui est appelée par l'event <<Change>>.

            Cette fonction est appelée par l'event <<Change>>. Elle s'occupe
            de mettre à jour le texte du widget après un appel de refresh.

            :example:
            >>> test = TextCin()
            >>> test.afterRefresh(None)

            :param event: Object event qui détient les informations.
            :type event: Event.

        """
        # Si refresh a été appelée.
        if self.haveToUpdate:
            # On mets à jour le texte.
            self.delete(1.0, END)
            self.insert(END, self.lastText)
            # Nous fermons l'update.
            self.haveToUpdate = False
        # Fin.
        return

    def reset(self):
        """
            Réinitialise le texte.

            Cette fonction réinitialise le texte.

            :example:
            >>> test = TextCin()
            >>> test.reset()

        """
        # Réinitialise le texte.
        self.delete(1.0, END)
        self.lastText = "." * 255
        self.insert(END, self.lastText)
        # Fin.
        return

    def setCharacter(self, pos, char):
        """
            Change un caractère dans le widget Text.

            Cette fonction change la valeur du caractère « char » à la position
            « pos ».

            :example:
            >>> test = TextCin()
            >>> test.setCharacter(0, 'A')

            :param pos: Position à remplacer.
            :type pos: int
            :param char: Remplacer par ce caractère.
            :type char: str

        """
        # Effectue le changement.
        self.lastText = self.lastText[:pos] + char + self.lastText[pos + 1:]
        # Réinitialise le texte.
        self.delete(1.0, END)
        self.insert(END, self.lastText)
        # Fin.
        return

    def refresh(self, newkey):
        """
            Prépare la mise à jour et traite l'entrée clavier.

            Cette fonction prépare la mise à jour (car elle est appelée avant
            l'event <<Change>>) et traite l'entrée clavier puis la place dans
            le tampon mémoire du clavier.

            :example:
            >>> egal = 'L' + ('.' * 254)
            >>> test = TextCin()
            >>> test.refresh('L') == egal
            True

            :param newkey: Nouvelle entrée clavier (touche).
            :type newkey: char
            :return: Mémoire tampon des entrées clavier.
            :rtype: str

        """
        # On vérifie si la touche est dans la whitelist.
        newkey = intTOascii(newkey)
        # Sinon, on ajoute la dernière touche.
        self.lastText = newkey + self.lastText
        # On coupe si on dépasse le domaine du tampon mémoire.
        self.lastText = self.lastText[:255]
        # On avertit a «afterRefresh» que nous avons une mise à jour.
        self.haveToUpdate = True
        # Fin.
        return self.lastText


# Activation des doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod()
