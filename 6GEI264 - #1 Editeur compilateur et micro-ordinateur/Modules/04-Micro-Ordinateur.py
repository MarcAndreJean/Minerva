#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projet          : Editeur, Compilateur et Micro-Ordinateur pour
                      un langage assembleur.
    Nom du fichier  : 04-Micro-Ordinateur.py

    Identification  : 04-Micro-Ordinateur
    Titre           : Micro-Ordinateur
    Auteurs         : Marc-André Jean
    Date            : 15-04-2017
    Description     : Micro-Ordinateur. Rassemble les composantes et
                      initialise l'émulation.


    Le module ``Micro-Ordinateur``
    ================================

    Ce module contient une classe nommée « Micro-Ordinateur » qui gère les
    composantes (Bus, CPU, Clock et Mémoire). C'est le chef-d'orchestre
    pour l'émulation et c'est lui qui est responsable du bon fonctionnement
    du micro-ordinateur. La Clock est compris dans le micro-ordinateur comme
    dans l'horloge à l'intérieur de la carte-mère d'un ordinateur.


"""

__author__ = "Marc-Andre Jean"
__version__ = "1.0"
__status__ = "production"

# Importation des modules nécessaires.
try:
    modEnum = __import__("05-Enum")
    modBus = __import__("04-01-Bus")
    modCPU = __import__("04-02-CPU")
    modROM = __import__("04-04-ROM")
    modIO = __import__("04-05-IO")
    modRAM = __import__("04-06-RAM")
except ImportError:
    import importlib
    modEnum = importlib.import_module("Modules.05-Enum")
    modBus = importlib.import_module("Modules.04-01-Bus")
    modCPU = importlib.import_module("Modules.04-02-CPU")
    modROM = importlib.import_module("Modules.04-04-ROM")
    modIO = importlib.import_module("Modules.04-05-IO")
    modRAM = importlib.import_module("Modules.04-06-RAM")
# Redéfinition.
MODE = modEnum.MODE

from threading import Thread
from threading import Lock


class MicroOrdinateur():
    """
        class MicroOrdinateur
        ========================

        Cette classe s'occupe de l'émulation du MicroOrdinateur.

        :example:
        >>> test = MicroOrdinateur()

        ..note: L'horloge est intégré au micro-ordinateur. La fonction
                tick() et toggleClock() fait appel à fonction
                _runningClock() dans un Thread pour permettre une
                utilisation asynchrone du micro-ordinateur et de la GUI.

    """

    def __init__(self, extracomponents=[]):
        """
            Contrusteur de la classe Micro-Ordinateur.

            Cette fonction crée les composantes de bases du
            micro-ordinateur. Elle attache des composantes
            supplémentaires (pour permettre une compatibilité pour
            une réutilisation ou utilisation externe de cette classe).

            :example:
            >>> test = MicroOrdinateur()

            :param extracomponents: Liste de composants supplémentaires.
            :type extracomponents: List

            ..note: Les composants devraient être une classe ayant une
                    méthode nommée event() et une méthode nommée clock().

        """
        global clockActive
        global bus
        clockActive = False
        self.clock = False
        # État de la Clock.
        self.lock = Lock()
        self.clockThread = None
        # Création du bus.
        self.bus = modBus.Bus()
        bus = self.bus
        # Création des composants de base du Micro-Ordinateur.
        self.cpu = modCPU.CPU(self.bus)
        self.rom = modROM.ROM(self.bus)
        self.io = modIO.IO(self.bus)
        self.ram = modRAM.RAM(self.bus)
        # Attachement des composants supplémentaires (s'il y a lieu).
        self.xtracomp = extracomponents
        if self.xtracomp is not None:
            if not isinstance(self.xtracomp, list):
                self.xtracomp = [self.xtracomp]
            if len(self.xtracomp) > 0:
                for xcomp in self.xtracomp:
                    # On attache le bus.
                    if xcomp.attachBus:
                        xcomp.attachBus(self.bus)
                    # On attache le CPU.
                    if xcomp.attachCPU:
                        xcomp.attachCPU(self.cpu)
                    # On attache le module IO.
                    if xcomp.attachIO:
                        xcomp.attachIO(self.io)
        # Fin de __init__.
        return

    def load(self, bytecode):
        """
            Fonction pour charger bytecode dans la ROM un programme.

            Cette fonction charge un programme (celui dans bytecode) dans
            la mémoire ROM du micro-ordinateur.

            :example:
            >>> test = MicroOrdinateur()
            >>> test.load([0xFAFA, 0xAFAF, 0x0000, 0xFFFF])

            :param bytecode: Tableau de int (16 bits) d'un programme
                             exécutable.
            :type bytecode: int[]

        """
        # On réinitialise le micro-ordinateur.
        self.reset()
        self.rom.uploadProgram(bytecode)
        return

    def reset(self):
        """
            Fonction pour réinitialiser le micro-ordinateur.

            Cette fonction réinitialise la mémoire (sauf la ROM), les
            états et informations du CPU, et les informations sur le
            bus.

            :example:
            >>> test = MicroOrdinateur()
            >>> test.reset()

        """
        # On reset le bus et les éléments.
        self.bus.mode = MODE.RESET
        self.tick()  # Thread safe.
        # Retour à la normale.
        self.bus.mode = MODE.END
        return

    def tick(self):
        """
            Fonction pour produire un coup d'horloge.

            Cette fonction produit un coup d'horloge dans le bus
            duquel il propagera ce coup aux travers des autres
            composantes.

            :example:
            >>> test = MicroOrdinateur()
            >>> test.tick()

        """
        # On essaie d'acquérir le lock.
        if self.lock.acquire(False):
            # On donne un coup d'horloge.
            self.bus.clock()
            # Fin de l'utilisation du lock.
            self.lock.release()
        # Fin.
        return

    def toggleClock(self):
        """
            Fonction pour changer l'état de l'horloge.

            Cette fonction active/désactiver l'horloge dépendant
            de son état actuel.

            :example:
            >>> test = MicroOrdinateur()
            >>> test.toggleClock()
            >>> test.toggleClock()

        """
        global clockActive
        # Nous changons la valeur d'état du clock.
        clockActive = not clockActive
        # Si l'état est maintenant actif pour la clock, nous recréons
        # thread pour celui-ci.
        if clockActive:
            # On obtient le lock peu importe le temps.
            self.lock.acquire()
            # Si le thread n'a pas terminé on attends au moins
            # sa terminaison.
            # On crée le thread.
            self.clockThread = RunningClock()
            self.clockThread.start()
        else:
            # On attends que le Thread se termine.
            self.clockThread.join()
            # Fin de l'utilisation du lock.
            self.lock.release()
        # Fin.
        return

    def execute(self, bytecode):
        """
            Fonction qui exécute une simple ligne de commande.

            Cette fonction exécute une simple ligne de commande. Elle
            utilise le bytecode donné en argument.

            :example:
            >>> test = MicroOrdinateur()
            >>> test.execute([0x0000, 0x0000])

            :param bytecode: Code à exécuter.
            :type bytecode: int[] (16 bits)

        """
        # On upload le code.
        if len(bytecode) > 0:
            self.bus.mode = MODE.WRITE
            self.bus.address = 0x0000
            self.bus.data = bytecode[0]
            self.bus.event()
            if len(bytecode) > 1:
                self.bus.mode = MODE.WRITE
                self.bus.address = 0x0001
                self.bus.data = bytecode[1]
                self.bus.event()

        # On réinitialise le bus et le program counter.
        self.cpu.regP = 0x0000
        self.bus.mode = MODE.END
        # On exécute.
        self.tick()  # Thread safe.
        # Retour à la normale.
        return


class RunningClock(Thread):
    """
        class RunningClock
        ========================

        Cette classe s'occupe de l'horloge du MicroOrdinateur.

        :example:
        >>> var = MicroOrdinateur()
        >>> test = RunningClock()
        >>> test.start()
        >>> var.bus.mode = MODE.HALT

        ..note: L'horloge est intégré au micro-ordinateur. La fonction
                tick() et toggleClock() fait appel à fonction
                _runningClock() dans un Thread pour permettre une
                utilisation asynchrone du micro-ordinateur et de la GUI.

    """

    def run(self):
        """
            Fonction thread pour le clock.

            Fonction thread pour le clock. Si un OPCODE a terminé ces
            «computations» et que le bus est maintenant en arrêt (en
            attente d'un nouveau coup d'horloge), et bien nous lui donnons
            un nouveau coup d'horloge.

           ..note: La fonction ne donne aucun coup d'horloge si clockActive
                   est devenu inactif.

        """
        global clockActive
        global bus
        # On donne des coups d'horloge tant que l'horloge est active.
        while clockActive and bus.mode != MODE.HALT:
            # On donne un coup d'horloge si l'horloge est active.
            bus.clock()
        # Fin.
        return


# Activation des doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod()
