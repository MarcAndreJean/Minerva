#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projet          : Editeur, Compilateur et Micro-Ordinateur pour
                      un langage assembleur.
    Nom du fichier  : 03-Compileur.py

    Identification  : 03-Compileur
    Titre           : Compilateur
    Auteurs         : Marc-André Jean
    Date            : 13-04-2017
    Description     : Compilateur pour le langage assembleur.


    Le module ``Compileur``
    ================================

    Ce module contient la fonction compile(str) pour compiler le langage
    assembleur donné en argument. Les informations sur la syntaxe et les
    mots-clés du langage assembleur sont disponibles dans le manuel et
    dans le document de spécification. La fonction compile() utilise
    la fonction interne du module __compileEx(str, str) qui compile une
    simple ligne de code. Le module utilise plusieurs énumérations et
    dictionaires pour la rapidité du code et pour éviter les erreurs
    de programmation.


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
OPCODE = modEnum.OPCODE
ADRESSAGE = modEnum.ADRESSAGE
REGISTRE = modEnum.REGISTRE


def compile(code):
    """
        Fonction central pour la compilation du code assembleur.

        Cette fonction prend un texte (plusieurs lignes) et convertit
        celui-ci en tableau de 16 bits représentant le bytecode ROM du
        code assembleur.

        :example:
        >>> expect = [True,
        ...          [OPCODE.SET | REGISTRE.A,
        ...          83,
        ...          OPCODE.ST | REGISTRE.A | ADRESSAGE.ADDR,
        ...          16892,
        ...          OPCODE.HLT,
        ...          0]]
        ...
        >>> result = compile('SETA 83\\nSTA 16892\\nHLT')
        >>> expect == result
        True

        :param code: Code (plusieurs lignes) à compiler.
        :type code: str

        :return: True et un tableau de 16 bits de bytcode machine si la
                 compilation est un succès, autrement il renvoit False
                 et un message d'erreur.
        :rtype: [boolean, int[]] ou [boolean, str]

    """
    bytecode = []
    dictComment = {';': True, '#': True}
    # On parcourt le texte ligne par ligne.
    linenum = 1
    for line in iter(code.splitlines()):
        # On «split» la ligne en mots.
        words = line.split()
        # Si nous avons aucun mot OU que nous avons plus qu'un mot et
        # que le premier est un commentaire: nous ignorons la ligne.
        if len(words) == 0 \
                or (len(words) >= 1 and dictComment.get(words[0][0], False)):
            continue
        # Si nous avons un mot et que celui-ci n'est pas un commentaire,
        # OU que nous avons plus que deux mots et que le deuxième est
        # un commentaire: nous essayons de compiler le potentiel opcode
        # (en ignorant le reste de la phrase si commentaire).
        elif (len(words) == 1 and not dictComment.get(words[0][0], False)) \
                or (len(words) >= 2 and dictComment.get(words[1][0], False)):
            opcode = words[0]
            valg = ''
            vald = ''
        # Si nous avons deux mot et que le deuxième n'est pas un
        # commentaire, OU que nous avons plus que trois mots et que
        # le troisième est un commentaire: nous essayons de compiler le
        # potentiel opcode et le potentiel argument (en ignorant le reste
        # de la phrase si commentaire).
        elif (len(words) == 2 and not dictComment.get(words[1][0], False)) \
                or (len(words) >= 3 and dictComment.get(words[2][0], False)):
            opcode = words[0]
            valg = words[1]
            vald = ''
        # Si nous avons deux mot et que le deuxième n'est pas un
        # commentaire, OU que nous avons plus que trois mots et que
        # le troisième est un commentaire: nous essayons de compiler le
        # potentiel opcode et le potentiel argument (en ignorant le reste
        # de la phrase si commentaire).
        elif (len(words) == 3 and not dictComment.get(words[2][0], False)) \
                or (len(words) >= 4 and dictComment.get(words[3][0], False)):
            opcode = words[0]
            valg = words[1]
            vald = words[2]
        # Sinon, il s'agit d'une ligne illégale.
        else:
            return [False, "Ligne " + str(linenum) + " : ligne illégale."]

        # On essaie de compiler la ligne.
        try:
            result = __compileEx(opcode, valg, vald)
            bytecode.append(result[0])
            bytecode.append(result[1])
        # On gère les exceptions
        except IndexError:
            return [False, "Ligne " + str(linenum) +
                    " : OPCODE/ARG incorrect."]
        except ValueError:
            return [False, "Ligne " + str(linenum) +
                    " : ARG incorrect. Impossible de convertir" +
                    " l'argument en nombre."]
        except CompilationErreur as e:
            if e.value == "INVALID OPCODE":
                return [False, "Ligne " + str(linenum) +
                        " : OPCODE invalide."]
            elif e.value == "INVALID OPCODE-REG":
                return [False, "Ligne " + str(linenum) +
                        " : L'option registre de l'OPCODE est invalide."]
            elif e.value == "INVALID RIGHT REG":
                return [False, "Ligne " + str(linenum) +
                        " : Le registre dans l'argument de droite est " +
                        "invalide."]
            elif e.value == "INVALID RIGHT ADDRESS":
                return [False, "Ligne " + str(linenum) +
                        " : L'adresse dans l'argument de droite est " +
                        "invalide."]
            elif e.value == "INVALID RIGHT ARG":
                return [False, "Ligne " + str(linenum) +
                        " : L'argument de droite est invalide."]
        linenum += 1
        # On vérifie si la taille de la ROM ne fait pas de buffer overflow.
        if linenum > 0x40FB:
            return [False, "Erreur : Dépassement de la mémoire ROM."]
    # On envoie les résultats à la fin.
    return [True, bytecode]


def __compileEx(opcode, valg='', vald=''):
    """
        Fonction interne pour la fonction compile() du module.

        Cette fonction prend deux strings et les analyses avec des
        dictionnaires et retourne deux ints de 16 bits (8 bits pour
        la commande et 8 bits pour le registre).


        :param opcode: Partie de gauche d'une ligne de code assembleur.
        :type opcode: str
        :param valg: Partie du complémentaire de gauche ou central d'une
                     ligne de code assembleur.
        :type valg: str
        :param vald: Partie de droite d'une ligne de code assembleur.
        :type vald: str

        :return: Retourne un tableau de deux cases. La case [0]
                 représente les 16 bits de gauche et la case [1]
                 représente les 16 bits de droite.
        :rtype: [int, int]

        ..note: -Une exception IndexError sera lancée si une des strings
                 n'est pas assez longue.
                -Une exception ValueError sera lancée si la string
                 d'argument n'est pas convertible en Integer.
                -Une exception CompilationErreur sera lancée si une des
                 strings est trop longue, si l'OPCODE est invalide, si
                 si l'OPCODE n'obtient pas correctement ses argurments
                 ou si un des arguments est invalide.


    """
    opcode.upper()
    _16bitsLeft = 0x0000
    _16bitsRight = 0x0000
    # Dictionnaire utilisé plus qu'une fois :
    dictREG = {'A': REGISTRE.A, 'a': REGISTRE.A,
               'B': REGISTRE.B, 'b': REGISTRE.B,
               'C': REGISTRE.C, 'c': REGISTRE.C,
               'D': REGISTRE.D, 'd': REGISTRE.D}

    # 16 Bits de gauche (OPCODE[REG]) de format OO[O][R]
    # ==========================================================
    # On vérifie si le bytecode est dans le premier dictionnaire
    # (2 caractères)
    _16bitsLeft = {
        'LD': OPCODE.LD,
        'ST': OPCODE.ST,
        'MV': OPCODE.MV,
        'OR': OPCODE.OR,
        'LT': OPCODE.LT,
        'GT': OPCODE.GT,
        'LE': OPCODE.LE,
        'GE': OPCODE.GE,
        'EQ': OPCODE.EQ,
        'EZ': OPCODE.EZ,
        'NZ': OPCODE.NZ,
    }.get(opcode[0:2], None)
    # Sinon on vérifie si le bytecode est dans le deuxième
    # dictionnaire (3 caractères)
    if _16bitsLeft is None:
        _16bitsLeft = {
            'NOP': OPCODE.NOP,
            'JMP': OPCODE.JMP,
            'JMZ': OPCODE.JMZ,
            'JMO': OPCODE.JMO,
            'JMC': OPCODE.JMC,
            'SET': OPCODE.SET,
            'HLT': OPCODE.HLT,
            'ADD': OPCODE.ADD,
            'SUB': OPCODE.SUB,
            'MUL': OPCODE.MUL,
            'DIV': OPCODE.DIV,
            'AND': OPCODE.AND,
            'XOR': OPCODE.XOR,
            'NOT': OPCODE.NOT,
            'DTA': OPCODE.DTA
        }.get(opcode[0:3], None)
        # Si aucun OPCODE n'a été trouvé, on lance une exception.
        if _16bitsLeft is None:
            raise CompilationErreur("INVALID OPCODE")
        # Sinon on note la longueur de l'OPCODE (pour trouver
        # la valeur du registre)
        else:
            indexReg = 3
    else:
        indexReg = 2

    # On garde en mémoire le OPCODE
    _16bitsOPCODE = _16bitsLeft

    # Maintenant on vérifie le registre (gauche) pour les OPCODES
    # concernées :
    if {OPCODE.JMC: False, OPCODE.JMZ: False,
        OPCODE.JMO: False, OPCODE.JMC: False,
        OPCODE.NOP: False, OPCODE.HLT: False,
            OPCODE.DTA: False, OPCODE.JMP: False}.get(_16bitsOPCODE, True):
        # On cherche dans le dictionnaire si la valeur est présente:
        try:
            reg = dictREG.get(opcode[indexReg], None)
            vald = valg
            indexReg += 1
        except IndexError:
            if valg is "":
                raise IndexError()
            reg = dictREG.get(valg, None)
            # On teste si le REGISTRE est valide en terme de longueur
            if len(valg) > 1:
                raise CompilationErreur("INVALID OPCODE-REG")
        # Si oui, on ajoute (avec OR bitwise) dans la valeur du
        # bytecode gauche. Sinon on lance une exception.
        if reg is None:
            raise CompilationErreur("INVALID OPCODE-REG")
        else:
            _16bitsLeft |= reg
    else:
        if vald is not "":
            raise CompilationErreur("INVALID RIGHT VALUE")
        vald = valg

    # On teste si le OPCODE est valide en terme de longueur
    if len(opcode) > indexReg:
        raise CompilationErreur("INVALID OPCODE")

    # 16 Bits de droite ([REG || VALUE || ADDRESS]) de format [R || V || A]
    # ==========================================================
    # Si l'OPCODE a une valeur de registre [A:D] dans les bits droits
    if {OPCODE.MV: True, OPCODE.ADD: True,
        OPCODE.SUB: True, OPCODE.MUL: True,
        OPCODE.DIV: True, OPCODE.OR: True,
        OPCODE.AND: True, OPCODE.XOR: True,
        OPCODE.LT: True, OPCODE.GT: True,
        OPCODE.LE: True, OPCODE.GE: True,
            OPCODE.EQ: True, }.get(_16bitsOPCODE, False):
        # Donnez la valeur de ce registre
        _16bitsRight = dictREG.get(vald, None)
        if _16bitsRight is None:
            raise CompilationErreur("INVALID RIGHT REG")
    # Si l'OPCODE a une valeur dans les bits droits
    elif OPCODE.SET == _16bitsOPCODE:
        _16bitsRight = stringToInt(vald)
        if _16bitsRight > 0xFFFF:
            raise CompilationErreur("INVALID RIGHT VALUE")
    # Si l'OPCODE a une adresse* dans les bits droits
    elif {OPCODE.LD: True, OPCODE.ST: True}.get(_16bitsOPCODE, False):
        _16bitsRight = dictREG.get(vald, None)
        if _16bitsRight is None:
            _16bitsRight = stringToInt(vald)
            if _16bitsRight > 0xFFFF:
                raise CompilationErreur("INVALID RIGHT ARG")
            # Mode d'adressage en mode « Argument est une adresse ».
            _16bitsLeft |= ADRESSAGE.ADDR
        else:
            # Mode d'adressage en mode « Argument est une adresse vers un
            # registre ».
            _16bitsLeft |= ADRESSAGE.ADDR_FROM_REG
    # Si l'OPCODE a une adresse dans les bits droits
    elif {OPCODE.JMP: True, OPCODE.JMZ: True,
          OPCODE.JMO: True, OPCODE.JMC: True,
          }.get(_16bitsOPCODE, False):
        _16bitsRight = stringToInt(vald)
        if _16bitsRight > 0xFFFF:
            raise CompilationErreur("INVALID RIGHT ADDRESS")
        # Ajoute le mode d'adressage en mode « Argument est une ADRESSE ».
        _16bitsLeft |= ADRESSAGE.ADDR
    elif OPCODE.DTA == _16bitsOPCODE:
        _16bitsLeft = stringToInt(vald)
        _16bitsRight = stringToInt(vald)

    # On retourne nos deux 16 bits de données.
    return [_16bitsLeft, _16bitsRight]


def stringToInt(val):
    """
        Fonction pour compilateur qui convertit l'argument.

        Cette fonction convertit (selon la représentation) un
        string en int.

        :example:
        >>> stringToInt("99")
        99
        >>> stringToInt("'a'")
        97
        >>> stringToInt("0b1001")
        9
        >>> stringToInt("0o07")
        7
        >>> stringToInt("0x0A")
        10

        :param val: String avec une représentation quelconque.
        :type val: str
        :return: Nombre égal à la représentation.
        :rtype: int

    """
    # Conversion ASCII vers Int. Eg. 'a'
    if len(val) == 3 and val[0] == '\'' and val[2] == '\'':
        return ord(val[1])
    # Sinon, conversion String/Décimal vers int. Eg.: 10
    try:
        return abs(int(val))  # Décimal
    except ValueError:
        # Sinon, conversion String/Binaire vers int. Eg.: 0b0101
        try:
            return abs(int(val, 2))  # Binaire
        except ValueError:
            # Sinon, conversion String/Octal vers int. Eg.: 0o76
            try:
                return abs(int(val, 8))  # Octal
            except ValueError:
                # Sinon, conversion String/Hex vers int. Eg.: 0xA6
                return abs(int(val, 16))  # Hex


class CompilationErreur(Exception):
    """
        Classe d'exception pour la compilation.

        Il s'agit simplement d'un classe qui hérite de la classe
        Exception de base de Python. Elle sera utilisée lors d'une
        exception lors de la compilation ligne par ligne
        (voir __compileEx).

        :example:
        >>> val = CompilationErreur("TEST")
        >>> val.value
        'TEST'


    """

    def __init__(self, value):
        """
            Constructeur de l'exception.

            :param value: Code d'erreur ou message d'erreur.
            :type value: int or str

        """
        self.value = value


# Activation des doctest
if __name__ == "__main__":
    import doctest
    doctest.testfile("doctest-03-Compileur.txt")
    doctest.testmod()
