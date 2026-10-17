#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projet          : Editeur, Compilateur et Micro-Ordinateur pour
                      un langage assembleur.
    Nom du fichier  : 04-06-RAM.py

    Identification  : 04-06-RAM
    Titre           : RAM
    Auteurs         : Marc-André Jean
    Date            : 15-04-2017
    Description     : Mémoire RAM du Micro-Ordinateur.


    Le module ``RAM``
    ================================

    Ce module présente la classe RAM qui est la représentation de la
    mémoire RAM du micro-ordinateur. C'est elle qui lit ou écrit en mémoire
    RAM selon l'adresse indiqué dans le bus. Si c'est une lecture, la mémoire
    renvoit la valeur sur la ligne Data du bus.


"""

__author__ = "Marc-Andre Jean"
__version__ = "1.0"
__status__ = "Production"


# Importation des modules nécessaires.
try:
    modEnum = __import__("05-Enum")
    modBus = __import__("04-01-Bus")
except ImportError:
    import importlib
    modEnum = importlib.import_module("Modules.05-Enum")
    modBus = importlib.import_module("Modules.04-01-Bus")
# Redéfinition.
MODE = modEnum.MODE


class RAM:
    """
        class RAM
        ========================

        Cette classe représente la mémoire RAM du micro-ordinateur. À chaque
        coup d'horloge (clock/event), la classe vérifie si elle doit effectuer
        une lecture ou écriture en mémoire.

        :example:
        >>> test = RAM(modBus.Bus())


    """

    # Constructeur.
    def __init__(self, bus):
        """
            Constructeur de la classe RAM.

            Le constructeur s'occupe d'initialiser la mémoire et lie
            ce composant avec le bus.

            :example:
            >>> test = RAM(modBus.Bus())

            :param bus: Composant Bus du Micro-Ordinateur.
            :type bus: Bus

        """
        # Bus.
        self.bus = bus
        self.bus.register(self)

        # Tableau de int pour représenter la mémoire.
        self._data = [0] * (0x7FFF + 1)
        return

    def event(self):
        """
            Récepteur pour le signal event.

            Cette fonction est appelé lorsqu'un event est émit
            sur le bus. Elle gère l'écriture et la lecture en mémoire.

            :example:
            >>> bus = modBus.Bus()
            >>> test = RAM(bus)
            >>> test.event()
            >>> bus.event()

        """
        # Si ce n'est pas de la mémoire RAM, on quitte.
        if self.bus.address < 0x8000:
            return
        # Si en mode LECTURE:
        if self.bus.mode == MODE.READ:
            # On mets la valeur de la case mémoire à l'adresse bus.address
            # dans le bus.data.
            self.bus.data = self._data[self.bus.address - 0x8000]
        # Si en mode ÉCRITURE:
        elif self.bus.mode == MODE.WRITE:
            # On mets la valeur de bus.data dans la case mémoire
            # à l'adresse bus.address.
            self._data[self.bus.address - 0x8000] = self.bus.data
        return

    def clock(self):
        """
            Récepteur pour le signal clock.

            Cette fonction est appelé lorsqu'un coup d'horloge est émit
            sur le bus. Elle gère la réinitialisation de la mémoire si
            le bus est en mode RESET.

            :example:
            >>> bus = modBus.Bus()
            >>> test = RAM(bus)
            >>> test.clock()
            >>> bus.clock()

        """
        # On réinitialise la mémoire si le bus est en mode reset.
        if self.bus.mode == MODE.RESET:
            for i in range(0, 0x7FFF + 1):
                self._data[i] = 0x0000
        # Fin de la fonction.
        return


# Activation des doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod()
