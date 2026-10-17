#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projet          : Editeur, Compilateur et Micro-Ordinateur pour
                      un langage assembleur.
    Nom du fichier  : 04-02-CPU.py

    Identification  : 04-02-CPU
    Titre           : CPU
    Auteurs         : Marc-André Jean
    Date            : 16-04-2017
    Description     : CPU du Micro-Ordinateur.


    Le module ``CPU``
    ================================

    Ce module contient la classe CPU qui est la représentation du CPU du
    micro-ordinateur. C'est cette classe qui gère les calculs, le transfert
    de la mémoire et l'exécution des instructions d'un programme.


"""

__author__ = "Marc-Andre Jean"
__version__ = "1.0"
__status__ = "Production"

# Importation des modules nécessaires.
try:
    modEnum = __import__("05-Enum")
    modBus = __import__("04-01-Bus")
    modALU = __import__("04-03-ALU")
except ImportError:
    import importlib
    modEnum = importlib.import_module("Modules.05-Enum")
    modBus = importlib.import_module("Modules.04-01-Bus")
    modALU = importlib.import_module("Modules.04-03-ALU")
# Redéfinition.
OPCODE = modEnum.OPCODE
MODE = modEnum.MODE
REGISTRE = modEnum.REGISTRE
ADRESSAGE = modEnum.ADRESSAGE

# À partir du bit le moins significatif :
#  - Parity
#  - Sign
#  - Carry (overflow)
#  - Zero
#  - CND
# Enumération pour le registre STATUS.
STATUS = modEnum.enum(PARITY=0x0001,  # 0b 0000 0000 0000 0001
                      SIGN=0x0002,   # 0b 0000 0000 0000 0010
                      CARRY=0x0004,  # 0b 0000 0000 0000 0100
                      ZERO=0x0008,   # 0b 0000 0000 0000 1000
                      CND=0x0010)    # 0b 0000 0000 0001 0000


class CPU:
    """
        class CPU
        ========================

        Cette classe contient la classe cpu. Elle représente le CPU
        telle que présentée dans le document de
        spécification.

        :example:
        >>> test = CPU(modBus.Bus())


    """

    def __init__(self, bus):
        """
            Constructeur de la classe CPU.

            Le constructeur initialise les composants du CPU dont l'ALU.
            Elle s'occupe aussi de lier le CPU avec le bus en entrée.

            :example:
            >>> test = CPU(modBus.Bus())

            :param bus: Le bus du MicroOrdinateur.
            :type bus: Bus

        """
        self.event = False
        # Connexion avec le bus.
        self.bus = bus
        self.bus.register(self)
        # Création de l'ALU.
        self.alu = modALU.ALU()
        # Création des registres.
        self.regP = 0x0000  # Program counter.
        self.regI = 0x0000  # Instruction register.
        self.regS = 0x0000  # Status Register.
        # Registres A, B, C, D
        self.regA = 0x0000
        self.regB = 0x0000
        self.regC = 0x0000
        self.regD = 0x0000

        # Fin.
        return

    def _getReg(self, registre):
        """
            Lit le registre en argument avec la valeur.

            Cette fonction lit et retourne la valeur du registre en argument.

            :param registre: Registre à lire.
            :type registre: int (16 bits)
            :rtype: Valeur dudit registre.
            :rtype: int (16 bits)


        """
        if registre == REGISTRE.A:
            return self.regA
        elif registre == REGISTRE.B:
            return self.regB
        elif registre == REGISTRE.C:
            return self.regC
        elif registre == REGISTRE.D:
            return self.regD
        else:
            raise Exception()
        # Fin impossible.
        return

    def _setReg(self, registre, valeur):
        """
            Modifie le registre en argument avec la valeur.

            Cette fonction modifie la valeur du registre en argument avec
            la valeur en argument.

            :param registre: Registre à modifier.
            :type registre: int (16 bits)
            :param valeur: Valeur à assigner.
            :type valeur: int (16 bits)

        """
        if registre == REGISTRE.A:
            self.regA = valeur
        elif registre == REGISTRE.B:
            self.regB = valeur
        elif registre == REGISTRE.C:
            self.regC = valeur
        elif registre == REGISTRE.D:
            self.regD = valeur
        else:
            return None
        return

    def clock(self):
        """
            Récepteur pour le signal clock.

            Cette fonction est appelé lorsqu'un coup d'horloge est émit
            sur le bus. Elle gère la réinitialisation du CPU si le bus est
            en mode RESET. Sinon le CPU fetch la prochaine instruction.

            :example:
            >>> bus = modBus.Bus()
            >>> test = CPU(bus)
            >>> test.clock()
            >>> bus.clock()
            >>> bus.event()

        """
        # On réinitialise le CPU si le bus est en mode reset.
        if self.bus.mode == MODE.RESET:
            # Registres program.
            self.regP = 0x0000  # Program counter.
            self.regI = 0x0000  # Instruction register.
            self.regS = 0x0000  # Status Register.
            # Registres A, B, C, D
            self.regA = 0x0000
            self.regB = 0x0000
            self.regC = 0x0000
            self.regD = 0x0000
        # On fetch la prochaine instruction si le bus est en mode INERTE.
        elif self.bus.mode == MODE.INERTE:
            self._fetch()
            self._decode()
            self._execute()
        # Fin de la fonction.
        return

    def _readAddress(self):
        """
            Cette fonction fetch une valeur d'une adresse.

            Cette fonction va chercher la valeur à une adresse selon le
            mode d'adressage.

        """
        adressage = self.regI & 0x00F0
        self.bus.mode = MODE.READ

        # 1. L'argument est l'adresse d'un registre.
        if adressage == ADRESSAGE.ADDR_OF_REG:
            self.bus.data = self._getReg(self.bus.data)
            return

        # 2. L'argument est l'adresse d'un registre qui pointe vers une
        # adresse.
        elif adressage == ADRESSAGE.ADDR_FROM_REG:
            # On fetch l'adresse indiquer dans ce registre.
            self.bus.address = self._getReg(self.bus.data)

        # 3. L'argument est une adresse.
        elif adressage == ADRESSAGE.ADDR:
            # On retourne l'adresse.
            self.bus.address = self.bus.data

        # 4. L'argument est une adresse qui pointe vers une adresse.
        elif adressage == ADRESSAGE.ADDR_FROM_ADDR:
            # Double-fetch.
            self.bus.address = self.bus.data
            self.bus.event()
            self.bus.mode = MODE.READ
            self.bus.address = self.bus.data

        # Fetch la valeur à cette adresse.
        self.bus.event()
        return

    def _fetch(self):
        """
            Cette fonction fetch la prochaine instruction à exécuter.

            Cette fonction permet prépare le bus pour que la mémoire lit
            la prochaine instruction à exécuter.

        """
        # On place le bus en mode lecture pour la prochaine adresse.
        self.bus.mode = MODE.READ
        self.bus.address = self.regP
        # On envoie le signal au bus.
        self.bus.event()

        # On lit l'instruction dans le bus.
        self.regI = self.bus.data
        # Fin.
        return

    def _decode(self):
        """
            Cette fonction décode l'instruction courante.

            Cette fonction refait un fetch pour les commandes néccessitant
            l'argument de droite (16 bits), sinon elle peut exécuter
            celle-ci.

        """
        # On vérifie si l'opération n'a pas besoin d'argument droit:
        if {OPCODE.NOT: True,
            OPCODE.EZ: True,
            OPCODE.NZ: True,
            OPCODE.NOP: True,
                OPCODE.HLT: True}.get(self.regI, False):
            return  # On quitte pour aller à l'étape d'exécution.
        # Sinon on fetch l'argument de droit:
        else:
            # On place le bus en mode lecture.
            self.bus.mode = MODE.READ
            self.bus.address = self.regP + 1
            # On envoie le signal au bus.
            self.bus.event()
        # Fin.
        return

    def _execute(self):
        """
            Cette fonction exécute l'instruction courante.

            Cette fonction exécute l'instruction courante et retourne
            les résultats appropriés dans le bus ou dans les registres.

        """
        # On extrait les données pour travailler.
        opcode = self.regI & 0xFF00
        adressage = self.regI & 0x00F0
        regG = self.regI & 0x000F
        valD = self.bus.data
        result = 0x0000

        # NOP
        if opcode == OPCODE.NOP:
            pass
        # ADD, SUB, MUL, DIV
        # OR, AND, XOR, NOT
        elif opcode & 0xF000 == 0x1000 \
                or opcode & 0xF000 == 0x2000:
            # Reset regS 0x00FF to 0x0000.
            self.regS = 0x0000

            # Execute
            # ADD, SUB, MUL, DIV
            # Si le OPCODE est ADD:
            if opcode == OPCODE.ADD:
                result = self.alu.fonctionADD(self._getReg(regG),
                                              self._getReg(valD))
            # Si le OPCODE est SUB:
            elif opcode == OPCODE.SUB:
                result = self.alu.fonctionSUB(self._getReg(regG),
                                              self._getReg(valD))
            # Si le OPCODE est MUL:
            elif opcode == OPCODE.MUL:
                result = self.alu.fonctionMUL(self._getReg(regG),
                                              self._getReg(valD))
            # Si le OPCODE est DIV:
            elif opcode == OPCODE.DIV:
                result = self.alu.fonctionDIV(self._getReg(regG),
                                              self._getReg(valD))

            # Execute
            # OR, AND, XOR, NOT
            # Si le OPCODE est OR:
            elif opcode == OPCODE.OR:
                result = self.alu.fonctionOR(self._getReg(regG),
                                             self._getReg(valD))
            # Si le OPCODE est AND:
            elif opcode == OPCODE.AND:
                result = self.alu.fonctionAND(self._getReg(regG),
                                              self._getReg(valD))
            # Si le OPCODE est XOR:
            elif opcode == OPCODE.XOR:
                result = self.alu.fonctionXOR(self._getReg(regG),
                                              self._getReg(valD))
            # Si le OPCODE est NOT:
            elif opcode == OPCODE.NOT:
                result = self.alu.fonctionNOT(self._getReg(regG))

            # Vérification pour registre STATUS.
            # --Parité.
            self.regS |= (result & STATUS.PARITY)

            # --Sign
            if result < 0:
                # Si le résultat est négatif, Sign = True
                self.regS |= STATUS.SIGN
                result = abs(result)

            # --Carry
            if result > 0xFFFF:
                # Si on a un overflow, carry = True
                self.regS |= STATUS.CARRY
                result &= 0xFFFF

            # --Zero
            if result == 0x0000:
                # Si le résultat est égal à zéro, Zero = True
                self.regS |= STATUS.ZERO

            # On mets le résultat dans le registre A-D.
            self._setReg(regG, result)

        # LT, GT, LE, GE, EQ, EZ
        elif opcode & 0xF000 == 0x3000:
            # Reset regS 0x00FF to 0x0000.
            self.regS = 0x0000
            # Execute
            # Si le OPCODE est LT:
            if opcode == OPCODE.LT:
                result = self.alu.fonctionLT(self._getReg(regG),
                                             self._getReg(valD))
            # Si le OPCODE est GT:
            elif opcode == OPCODE.GT:
                result = self.alu.fonctionGT(self._getReg(regG),
                                             self._getReg(valD))
            # Si le OPCODE est LE:
            elif opcode == OPCODE.LE:
                result = self.alu.fonctionLE(self._getReg(regG),
                                             self._getReg(valD))
            # Si le OPCODE est GE:
            elif opcode == OPCODE.GE:
                result = self.alu.fonctionGE(self._getReg(regG),
                                             self._getReg(valD))
            # Si le OPCODE est EQ:
            elif opcode == OPCODE.EQ:
                result = self.alu.fonctionEQ(self._getReg(regG),
                                             self._getReg(valD))
            # Si le OPCODE est EZ:
            elif opcode == OPCODE.EZ:
                result = self.alu.fonctionEZ(self._getReg(regG))
            # Si le OPCODE est NZ:
            elif opcode == OPCODE.NZ:
                result = self.alu.fonctionNZ(self._getReg(regG))
            # On applique le résultat.
            if result:
                self.regS |= STATUS.CND
        # JMP, JMZ, JMO, JMC, HLT, SET, LD, ST, MV
        elif opcode & 0xF000 == 0x0000:
            # Execute : JM*
            # Si le OPCODE est JMP (résoudre l'adresse)
            if opcode == OPCODE.JMP:
                self._readAddress()
                self.regP = self.bus.address
                self.bus.mode = MODE.END
                return
            # Si le OPCODE est JMZ et flag ZERO ON (résoudre l'adresse)
            elif opcode == OPCODE.JMZ \
                    and self.regS & STATUS.ZERO == STATUS.ZERO:
                self._readAddress()
                self.regP = self.bus.address
                self.bus.mode = MODE.END
                return
            # Si le OPCODE est JMO et flag CARRY ON (résoudre l'adresse)
            elif opcode == OPCODE.JMO \
                    and self.regS & STATUS.CARRY == STATUS.CARRY:
                self._readAddress()
                self.regP = self.bus.address
                self.bus.mode = MODE.END
                return
            # Si le OPCODE est JMC et flag CND ON (résoudre l'adresse)
            elif opcode == OPCODE.JMC \
                    and self.regS & STATUS.CND == STATUS.CND:
                self._readAddress()
                self.regP = self.bus.address
                self.bus.mode = MODE.END
                return
            # Execute : ***
            # Si le OPCODE est SET
            if opcode == OPCODE.SET:
                self._setReg(regG, valD)
            # Si le OPCODE est LD (résoudre l'adresse)
            elif opcode == OPCODE.LD:
                self._readAddress()
                self.bus.mode = MODE.READ
                self.bus.event()
                self._setReg(regG, self.bus.data)

            # Si le OPCODE est ST (résoudre l'adresse)
            elif opcode == OPCODE.ST:
                self._readAddress()
                self.bus.data = self._getReg(regG)
                self.bus.mode = MODE.WRITE
                self.bus.event()

            # Si le OPCODE est MV
            elif opcode == OPCODE.MV:
                self._setReg(regG, self._getReg(valD))
            # Si le OPCODE est HALT
            elif opcode == OPCODE.HLT:
                # On empêche toute prochaine exécution
                self.bus.mode = MODE.HALT
                return

        # On incrémente le Program Counter.
        self.regP += 2
        # On place le bus en MODE END (sauf pour les OPCODE's qui
        # requisent de résoudre une adresse).
        self.bus.mode = MODE.END
        # On empêche toute prochaine exécution si le pc est illégal.
        if self.regP > 0xFFFF:
            self.bus.mode = MODE.HALT
        # Fin.
        return


# Activation des doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod()
