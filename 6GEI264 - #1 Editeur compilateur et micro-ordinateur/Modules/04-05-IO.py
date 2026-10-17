#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projet          : Editeur, Compilateur et Micro-Ordinateur pour
                      un langage assembleur.
    Nom du fichier  : 04-05-IO.py

    Identification  : 04-05-IO
    Titre           : I/O
    Auteurs         : Marc-André Jean
    Date            : 15-04-2017
    Description     : Composant entrée/sortie du Micro-Ordinateur.


    Le module ``I/O``
    ================================

    Ce module présente la classe IO qui est la représentation des entrées et
    sorties du micro-ordinateur. C'est elle qui lit ou écrit en mémoire les IO
    selon l'adresse indiqué dans le bus. Si c'est une lecture, la mémoire
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

from threading import Lock


class IO:
    """
        class IO
        ========================

        Cette classe représente les entrées/sorties du micro-ordinateur.
        À chaque coup d'horloge (clock/event), la classe vérifie si elle doit
        effectuer une lecture ou écriture en mémoire.

        :example:
        >>> test = IO(modBus.Bus())

    """

    # Constructeur.
    def __init__(self, bus):
        """
            Constructeur de la classe IO.

            Le constructeur s'occupe d'initialiser la mémoire IO et lie
            ce composant avec le bus.

            :example:
            >>> test = IO(modBus.Bus())

            :param bus: Composant Bus du Micro-Ordinateur.
            :type bus: Bus

        """
        self.lockIO = Lock()
        # Bus.
        self.bus = bus
        self.bus.register(self)

        # Tableau de int pour représenter la mémoire IO.
        self.data = [0] * (0x3F03 + 1)
        return

    def event(self):
        """
            Récepteur pour le signal event.

            Cette fonction est appelé lorsqu'un event est émit
            sur le bus. Elle gère l'écriture et la lecture en mémoire.

            :example:
            >>> bus = modBus.Bus()
            >>> test = IO(bus)
            >>> test.event()
            >>> bus.event()

        """
        # Si ce n'est pas de I/O, on quitte.
        if self.bus.address < 0x40FC or self.bus.address > 0x7FFF:
            return
        # Si en mode LECTURE:
        if self.bus.mode == MODE.READ:
            # On mets la valeur de la case mémoire à l'adresse bus.address
            # dans le bus.data.
            self.lockIO.acquire()
            self.bus.data = self.data[self.bus.address - 0x40FC]
            self.lockIO.release()
        # Si en mode ÉCRITURE:
        elif self.bus.mode == MODE.WRITE:
            # On mets la valeur de bus.data dans la case mémoire
            # à l'adresse bus.address.
            self.lockIO.acquire()
            self.data[self.bus.address - 0x40FC] = self.bus.data
            self.lockIO.release()
        return

    def clock(self):
        """
            Récepteur pour le signal clock.

            Cette fonction est appelé lorsqu'un coup d'horloge est émit
            sur le bus. Elle gère la réinitialisation de la mémoire si
            le bus est en mode RESET.

            :example:
            >>> bus = modBus.Bus()
            >>> test = IO(bus)
            >>> test.clock()
            >>> bus.clock()

        """
        # On réinitialise la mémoire si le bus est en mode reset.
        if self.bus.mode == MODE.RESET:
            self.lockIO.acquire()
            for i in range(0, 0x3F03 + 1):
                self.data[i] = 0x0000
            self.lockIO.release()
        # Fin de la fonction.
        return


# Activation des doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod()
