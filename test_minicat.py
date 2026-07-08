#!/usr/bin/env python3
"""
Tests complets de MiniCat v4.
Cobreix: aritmètica, lògica, definicions, funcions, si, mentre, provar,
llistes, vectors, cadenes, diccionaris, macros, TCO, compilació (simple i potent),
traça, errors, E/S simulada, càrrega de fitxers, i més.
"""

import sys, io, unittest, math, tempfile, os
from minicat_v4 import executa, entorn_global, entorn_inicial

class TestMiniCatV4_Complet(unittest.TestCase):
    def setUp(self):
        global entorn_global
        entorn_global = entorn_inicial()

    # ================================================================
    # Aritmètica i constants
    # ================================================================
    def test_aritmetica_basica(self):
        self.assertEqual(executa("(+ 2 3)"), 5)
        self.assertAlmostEqual(executa("(/ 7 2)"), 3.5)
        self.assertEqual(executa("(modul 10 3)"), 1)
        self.assertAlmostEqual(executa("(expon 2 8)"), 256)

    def test_constants_math(self):
        self.assertAlmostEqual(executa("pi"), math.pi)
        self.assertAlmostEqual(executa("e"), math.e)

    def test_funcions_math(self):
        self.assertAlmostEqual(executa("(sin 0)"), 0.0)
        self.assertAlmostEqual(executa("(cos 0)"), 1.0)
        self.assertAlmostEqual(executa("(arrel 16)"), 4.0)
        self.assertAlmostEqual(executa("(abs -5)"), 5)

    # ================================================================
    # Booleans i lògica
    # ================================================================
    def test_bools_i_logica(self):
        self.assertTrue(executa("cert"))
        self.assertFalse(executa("fals"))
        self.assertTrue(executa("(i cert cert)"))
        self.assertFalse(executa("(i cert fals)"))
        self.assertTrue(executa("(o fals cert)"))
        self.assertFalse(executa("(no cert)"))

    # ================================================================
    # definicions i variables
    # ================================================================
    def test_definir_i_us(self):
        executa("(definir x 10)")
        self.assertEqual(executa("(+ x 5)"), 15)

    # ================================================================
    # Funcions anònimes (lambda)
    # ================================================================
    def test_funcio_lambda(self):
        executa("(definir doble (funció (x) (* x 2)))")
        self.assertEqual(executa("(doble 4)"), 8)

    def test_funcio_dos_args(self):
        executa("(definir suma (funció (a b) (+ a b)))")
        self.assertEqual(executa("(suma 3 4)"), 7)

    # ================================================================
    # Condicionals (si)
    # ================================================================
    def test_si_complet(self):
        self.assertEqual(executa("(si (> 3 2) 100 200)"), 100)
        self.assertEqual(executa("(si (< 5 2) 100 200)"), 200)
        self.assertIsNone(executa("(si fals 42)"))
        self.assertEqual(executa("(si cert 1)"), 1)

    # ================================================================
    # Bucles (mentre)
    # ================================================================
    def test_mentre_bucle(self):
        executa("(definir i 0)")
        executa("(mentre (< i 3) (definir i (+ i 1)))")
        self.assertEqual(executa("i"), 3)

    # ================================================================
    # Captura d'errors (provar)
    # ================================================================
    def test_provar(self):
        self.assertEqual(executa("(provar 42 99)"), 42)
        self.assertEqual(executa("(provar (/ 1 0) 99)"), 99)

    # ================================================================
    # Llistes i vectors
    # ================================================================
    def test_llistes(self):
        self.assertEqual(executa("(llista 1 2 3)"), [1, 2, 3])
        self.assertEqual(executa("(cons 0 (llista 1 2))"), [0, 1, 2])
        self.assertEqual(executa("(car (llista 10 20 30))"), 10)
        self.assertEqual(executa("(cdr (llista 10 20 30))"), [20, 30])
        self.assertTrue(executa("(buit? (llista))"))
        self.assertEqual(executa("(longitud (llista 1 2 3))"), 3)

    def test_vectors(self):
        self.assertEqual(executa("(vector 4 5 6)"), [4, 5, 6])

    # ================================================================
    # Cadenes
    # ================================================================
    def test_cadenes(self):
        self.assertEqual(executa('(concat "Hola" " " "món")'), "Hola món")
        self.assertEqual(executa('(subcadena "abcdef" 2 4)'), "cd")
        self.assertEqual(executa('(cadena (+ 2 3))'), "5")

    # ================================================================
    # Diccionaris
    # ================================================================
    def test_diccionari(self):
        executa('(definir d (diccionari :nom "Pere" :edat 30))')
        self.assertEqual(executa('(obté d :nom)'), "Pere")
        executa('(assigna d :edat 31)')
        self.assertEqual(executa('(obté d :edat)'), 31)
        claus = executa('(claus d)')
        self.assertIn(':nom', claus)
        self.assertIn(':edat', claus)

    # ================================================================
    # Macros
    # ================================================================
    def test_macro_quan(self):
        executa('(definir-macro quan (funció (cond . cos) (llista \'si cond (cons \'prova cos))))')
        self.assertEqual(executa("(quan (> 3 2) 10)"), 10)

    def test_macro_repeteix(self):
        executa('''(definir-macro repeteix (funció (n . cos)
            (llista 'prova
                (llista 'definir 'i 0)
                (llista 'mentre (llista '< 'i n)
                    (llista 'prova
                        (cons 'prova cos)
                        (llista 'definir 'i (llista '+ 'i 1))))
                'i)))''')
        f = io.StringIO()
        import sys
        old = sys.stdout
        sys.stdout = f
        try:
            executa("(repeteix 3 (escriure \"hola\"))")
        finally:
            sys.stdout = old
        sortida = f.getvalue().strip()
        self.assertEqual(sortida.count("hola"), 3)
        self.assertEqual(executa("i"), 3)

    # ================================================================
    # TCO (recursió de cua amb trampolí)
    # ================================================================
    def test_tco_factorial(self):
        executa('''(definir-funció fact-aux (n acc)
            (si (<= n 1)
                acc
                (fact-aux (- n 1) (* n acc))))''')
        executa('(definir fact (funció (n) (fact-aux n 1)))')
        self.assertEqual(executa("(fact 5)"), 120)
        self.assertEqual(executa("(fact 20)"), 2432902008176640000)

    # ================================================================
    # Compilació a Python (potent)
    # ================================================================
    def test_compilacio_suma_simple(self):
        executa("(definir suma-comp (compila (+ 3 4)))")
        f = executa("suma-comp")
        self.assertEqual(f(), 7)

    def test_compilacio_amb_var(self):
        executa("(definir x 10)")
        executa("(definir f (compila (+ x 1)))")
        self.assertEqual(executa("(f)"), 11)

    def test_compilacio_si(self):
        executa("(definir f (compila (si (> 3 2) 100 200)))")
        self.assertEqual(executa("(f)"), 100)

    def test_compilacio_lambda(self):
        executa("(definir doble-comp (compila (funció (x) (* x 2))))")
        f = executa("doble-comp")
        self.assertEqual(f(4), 8)

    def test_compilacio_definir_funcio_recursiva(self):
        executa("(definir fact-comp (compila (definir-funció fact (n) (si (<= n 1) 1 (* n (fact (- n 1)))))))")
        f = executa("fact-comp")
        self.assertEqual(f(5), 120)

    def test_compilacio_mentre(self):
        codi = """
        (definir comptar-comp (compila (funció (n)
            (definir i 0)
            (mentre (< i n)
                (definir i (+ i 1)))
            i)))
        """
        executa(codi)
        f = executa("comptar-comp")
        self.assertEqual(f(3), 3)

    def test_compilacio_provar(self):
        executa("(definir segur-comp (compila (funció (x) (provar (/ 1 x) 999))))")
        f = executa("segur-comp")
        self.assertEqual(f(0), 999)
        self.assertAlmostEqual(f(2), 0.5)

    def test_compilacio_crida_funcio_interpretada(self):
        executa("(definir quadrat (funció (x) (* x x)))")
        executa("(definir aplica-comp (compila (funció (y) (quadrat y))))")
        f = executa("aplica-comp")
        self.assertEqual(f(3), 9)

    def test_compilacio_llista(self):
        executa("(definir l-comp (compila (llista 1 2 3)))")
        self.assertEqual(executa("(l-comp)"), [1, 2, 3])

    def test_compilacio_cons_car_cdr(self):
        executa("(definir f (compila (funció (x) (cons x (llista 2 3)))))")
        f = executa("f")
        self.assertEqual(f(1), [1, 2, 3])

    # ================================================================
    # Traça
    # ================================================================
    def test_traça_activada(self):
        f = io.StringIO()
        import sys
        old = sys.stdout
        sys.stdout = f
        try:
            executa("(activar-traça)")
            executa("(+ 1 2)")
            executa("(desactivar-traça)")
        finally:
            sys.stdout = old
        sortida = f.getvalue()
        self.assertIn("-> (+ 1 2)", sortida)
        self.assertIn("<- 3", sortida)

    # ================================================================
    # Errors i gestió de línies
    # ================================================================
    def test_error_parentesi_faltant(self):
        with self.assertRaises(SyntaxError) as cm:
            executa("(+ 1 2")
        self.assertIn("falta", str(cm.exception).lower())

    def test_error_simbol_no_definit(self):
        with self.assertRaises(NameError):
            executa("simbol_inexistent")

    # ================================================================
    # E/S simulada
    # ================================================================
    def test_llegir_numero_simulat(self):
        import builtins
        orig_input = builtins.input
        try:
            builtins.input = lambda: "42"
            self.assertEqual(executa("(llegir-numero)"), 42.0)
        finally:
            builtins.input = orig_input

    def test_llegir_text_simulat(self):
        import builtins
        orig_input = builtins.input
        try:
            builtins.input = lambda: "text"
            self.assertEqual(executa("(llegir)"), "text")
        finally:
            builtins.input = orig_input

    def test_escriure_captura(self):
        f = io.StringIO()
        import sys
        old = sys.stdout
        sys.stdout = f
        try:
            executa('(escriure "Hola, món!")')
        finally:
            sys.stdout = old
        self.assertEqual(f.getvalue().strip(), "Hola, món!")

    # ================================================================
    # Càrrega de fitxers
    # ================================================================
    def test_carrega_fitxer_suma(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cat', delete=False, encoding='utf-8') as tf:
            tf.write("(+ 10 20)")
            ruta = tf.name
        try:
            self.assertEqual(executa(f'(carrega-fitxer "{ruta}")'), 30)
        finally:
            os.unlink(ruta)

if __name__ == '__main__':
    unittest.main()
