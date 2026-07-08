"""
MiniCat v6
lexer.py
"""

from dataclasses import dataclass


# ==========================================================
# TOKEN
# ==========================================================

@dataclass
class Token:

    tipus: str
    valor: object
    linia: int
    columna: int


# ==========================================================
# LEXER
# ==========================================================

class Lexer:

    def __init__(self, text):

        self.text = text

        self.pos = 0

        self.linia = 1

        self.columna = 1

        self.tokens = []

    # ------------------------------------------------------

    def eof(self):

        return self.pos >= len(self.text)

    # ------------------------------------------------------

    def actual(self):

        if self.eof():
            return None

        return self.text[self.pos]

    # ------------------------------------------------------

    def seguent(self):

        c = self.actual()

        self.pos += 1

        if c == "\n":
            self.linia += 1
            self.columna = 1
        else:
            self.columna += 1

        return c

    # ------------------------------------------------------

    def afegir(self, tipus, valor):

        self.tokens.append(

            Token(

                tipus,

                valor,

                self.linia,

                self.columna

            )

        )

    # ------------------------------------------------------

    def comentari(self):

        while not self.eof():

            if self.actual() == "\n":
                return

            self.seguent()

    # ------------------------------------------------------

    def cadena(self):

        self.seguent()

        resultat = ""

        while True:

            if self.eof():
                raise SyntaxError("Cadena sense tancar")

            c = self.seguent()

            if c == '"':
                break

            if c == "\\":

                if self.eof():
                    raise SyntaxError("Escape incomplet")

                e = self.seguent()

                escapes = {

                    "n": "\n",

                    "t": "\t",

                    '"': '"',

                    "\\": "\\"

                }

                resultat += escapes.get(e, e)

            else:

                resultat += c

        self.afegir("STRING", resultat)

    # ------------------------------------------------------

    def numero(self):

        inici = self.pos

        punt = False

        while not self.eof():

            c = self.actual()

            if c == ".":

                if punt:
                    break

                punt = True

            elif not c.isdigit():
                break

            self.seguent()

        text = self.text[inici:self.pos]

        if punt:

            valor = float(text)

        else:

            valor = int(text)

        self.afegir("NUMBER", valor)

    # ------------------------------------------------------

    def simbol(self):

        inici = self.pos

        while not self.eof():

            c = self.actual()

            if c.isspace():

                break

            if c in "()'":

                break

            self.seguent()

        text = self.text[inici:self.pos]

        self.afegir("SYMBOL", text)

    # ------------------------------------------------------

    def tokenitza(self):

        while not self.eof():

            c = self.actual()

            if c.isspace():

                self.seguent()

                continue

            if c == ";":

                self.comentari()

                continue

            if c == "(":

                self.afegir("LPAREN", "(")

                self.seguent()

                continue

            if c == ")":

                self.afegir("RPAREN", ")")

                self.seguent()

                continue

            if c == "'":

                self.afegir("QUOTE", "'")

                self.seguent()

                continue

            if c == '"':

                self.cadena()

                continue

            if c.isdigit():

                self.numero()

                continue

            self.simbol()

        self.afegir("EOF", None)

        return self.tokens


# ==========================================================
# FUNCIÓ D'UTILITAT
# ==========================================================

def tokenitza(text):

    return Lexer(text).tokenitza()


# ==========================================================
# PROVES
# ==========================================================

if __name__ == "__main__":

    codi = """
    ; prova

    (definir x 12)

    (escriure (+ x 3))

    "Hola\\nMon"

    '(1 2 3)
    """

    for t in tokenitza(codi):

        print(t)
