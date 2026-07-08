#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import math
import random

# =====================================================
# LEXER
# =====================================================

def tokenitza(codi):

    tokens = []
    pos = 0

    while pos < len(codi):

        if codi[pos].isspace():
            pos += 1
            continue

        if codi[pos] == ';':
            while pos < len(codi) and codi[pos] != '\n':
                pos += 1
            continue

        if codi[pos] == '(':
            tokens.append('(')
            pos += 1
            continue

        if codi[pos] == ')':
            tokens.append(')')
            pos += 1
            continue

        if codi[pos] == "'":
            tokens.append("'")
            pos += 1
            continue

        if codi[pos] == '"':

            fi = pos + 1

            while fi < len(codi) and codi[fi] != '"':
                fi += 1

            if fi >= len(codi):
                raise SyntaxError("Cadena sense tancar")

            tokens.append(codi[pos:fi + 1])

            pos = fi + 1
            continue

        fi = pos

        while (
            fi < len(codi)
            and not codi[fi].isspace()
            and codi[fi] not in "()"
        ):
            fi += 1

        tokens.append(codi[pos:fi])

        pos = fi

    return tokens


# =====================================================
# PARSER
# =====================================================

def atom(token):

    if token.startswith('"') and token.endswith('"'):
        return token[1:-1]

    try:
        return int(token)
    except:
        pass

    try:
        return float(token)
    except:
        pass

    return token


def analitza(tokens):

    if len(tokens) == 0:
        raise SyntaxError("Expressió incompleta")

    token = tokens.pop(0)

    if token == '(':

        resultat = []

        while tokens[0] != ')':
            resultat.append(analitza(tokens))

        tokens.pop(0)

        return resultat

    elif token == ')':
        raise SyntaxError("')' inesperat")

    elif token == "'":
        return ["citar", analitza(tokens)]

    return atom(token)


def analitza_programa(codi):

    tokens = tokenitza(codi)

    programa = []

    while tokens:
        programa.append(analitza(tokens))

    return programa


# =====================================================
# ENTORN
# =====================================================

class Entorn(dict):

    def __init__(self, pare=None):
        super().__init__()
        self.pare = pare

    def buscar(self, nom):

        if nom in self:
            return self[nom]

        if self.pare:
            return self.pare.buscar(nom)

        raise NameError(
            f"Símbol no definit: {nom}"
        )


# =====================================================
# FUNCIONS MINICAT
# =====================================================

class FuncioMiniCat:

    def __init__(
        self,
        params,
        cos,
        entorn
    ):
        self.params = params
        self.cos = cos
        self.entorn = entorn

    def __call__(self, *args):

        local = Entorn(self.entorn)

        for p, a in zip(self.params, args):
            local[p] = a

        return avalua(self.cos, local)

    def __repr__(self):
        return "<funció>"


# =====================================================
# UTILITATS
# =====================================================

def convertir_numero(x):

    if isinstance(x, (int, float)):
        return x

    s = str(x)

    if "." in s:
        return float(s)

    return int(s)


def assigna_diccionari(d, clau, valor):

    d[clau] = valor

    return d


# =====================================================
# BIBLIOTECA ESTÀNDARD
# =====================================================

def entorn_inicial():

    e = Entorn()

    e.update({

        "cert": True,
        "fals": False,

        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,

        "=": lambda a, b: a == b,

        "<": lambda a, b: a < b,
        ">": lambda a, b: a > b,
        "<=": lambda a, b: a <= b,
        ">=": lambda a, b: a >= b,

        "i": lambda a, b: a and b,
        "o": lambda a, b: a or b,
        "no": lambda a: not a,

        "pi": math.pi,

        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "arrel": math.sqrt,

        "aleatori": lambda: random.random(),

        "llista": lambda *x: list(x),

        "car":
            lambda l: l[0],

        "cdr":
            lambda l: l[1:],

        "longitud":
            lambda x: len(x),

        "concat":
            lambda *x:
                "".join(str(v) for v in x),

        "cadena":
            lambda x: str(x),

        "numero":
            convertir_numero,

        "diccionari":
            lambda: {},

        "assigna":
            assigna_diccionari,

        "obté":
            lambda d,k:
                d.get(k),

        "escriure":
            lambda *x:
                print(*x),

    })

    return e


# =====================================================
# AVALUADOR
# =====================================================

def avalua(expr, entorn):

    if isinstance(expr, str):
        return entorn.buscar(expr)

    if not isinstance(expr, list):
        return expr

    if len(expr) == 0:
        return None

    cap = expr[0]

    # ----------------------

    if cap == "citar":
        return expr[1]

    # ----------------------

    if cap == "definir":

        _, nom, valor_expr = expr

        valor = avalua(
            valor_expr,
            entorn
        )

        entorn[nom] = valor

        return valor

    # ----------------------

    if cap == "funció":

        _, params, cos = expr

        return FuncioMiniCat(
            params,
            cos,
            entorn
        )

    # ----------------------

    if cap == "definir-funció":

        _, nom, params, cos = expr

        f = FuncioMiniCat(
            params,
            cos,
            entorn
        )

        entorn[nom] = f

        return f

    # ----------------------

    if cap == "si":

        if len(expr) == 4:

            _, cond, a, b = expr

            if avalua(cond, entorn):
                return avalua(a, entorn)

            return avalua(b, entorn)

        raise SyntaxError(
            "si requereix 3 arguments"
        )

    # ----------------------

    if cap == "mentre":

        _, cond, cos = expr

        resultat = None

        while avalua(cond, entorn):
            resultat = avalua(
                cos,
                entorn
            )

        return resultat

    # ----------------------

    if cap == "provar":

        _, cos, recupera = expr

        try:
            return avalua(cos, entorn)

        except Exception:
            return avalua(
                recupera,
                entorn
            )

    # ----------------------

    funcio = avalua(cap, entorn)

    args = [
        avalua(a, entorn)
        for a in expr[1:]
    ]

    if not callable(funcio):
        raise TypeError(
            f"{cap} no és cridable"
        )

    return funcio(*args)


# =====================================================
# EXECUCIÓ
# =====================================================

entorn_global = entorn_inicial()

def executa(codi):

    programa = analitza_programa(codi)

    resultat = None

    for expr in programa:
        resultat = avalua(
            expr,
            entorn_global
        )

    return resultat


# =====================================================
# REPL
# =====================================================

def repl():

    print(
        "MiniCat v5"
    )

    buffer = ""

    while True:

        try:

            linia = input("minicat> ")

            if linia.strip() == "sortir":
                break

            buffer += linia + "\n"

            if (
                buffer.count("(")
                ==
                buffer.count(")")
            ):

                resultat = executa(buffer)

                if resultat is not None:
                    print(resultat)

                buffer = ""

        except Exception as e:

            print(
                f"Error: {e}"
            )

            buffer = ""


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    repl()
