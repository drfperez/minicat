# 🐱 MiniCat

Un mini llenguatge de programació funcional inspirat en Lisp, escrit íntegrament en català.

MiniCat permet experimentar amb conceptes de llenguatges de programació, interpretació, compilació, macros i programació funcional utilitzant una sintaxi senzilla i educativa.

---

## ✨ Característiques principals

- Sintaxi Lisp amb notació prefixada
- Paraules clau en català
- Variables i funcions
- Closures i funcions d'ordre superior
- Recursió i optimització de cua (TCO)
- Llistes i vectors
- Diccionaris
- Macros definides per l'usuari
- Gestió d'errors
- Mode de traça per depuració
- Compilació a funcions Python natives
- REPL interactiu
- Tests automatitzats

---

## 📦 Requisits

- Python 3.8 o superior
- Cap dependència externa

---

## 🚀 Instal·lació

```bash
git clone https://github.com/el-teu-usuari/minicat.git
cd minicat
python minicat.py
```

---

## 🎮 Ús

### REPL interactiu

```bash
python minicat.py
```

Exemple:

```text
MiniCat REPL. Escriu 'sortir' per acabar.

minicat> (+ 1 2)
3

minicat> (definir saluda (funció (nom)
             (concat "Hola, " nom)))

minicat> (saluda "Pere")
Hola, Pere
```

---

### Executar un fitxer

```bash
python minicat.py programa.cat
```

---

# 📖 Guia ràpida

## Variables

```lisp
(definir x 10)
(definir y (* x 2))
```

---

## Operacions matemàtiques

```lisp
(+ 1 2)
(- 10 3)
(* 4 5)
(/ 10 2)

(modul 10 3)
(expon 2 8)
(arrel 16)
```

---

## Condicionals

```lisp
(si (> 5 3)
    "cert"
    "fals")
```

---

## Funcions

```lisp
(definir suma
  (funció (a b)
    (+ a b)))

(suma 3 4)
```

---

## Recursió

```lisp
(definir-funció factorial (n)
  (si (<= n 1)
      1
      (* n (factorial (- n 1)))))
```

---

## Llistes

```lisp
(llista 1 2 3)

(cons 0 (llista 1 2 3))

(car (llista 10 20 30))

(cdr (llista 10 20 30))
```

---

## Cadenes

```lisp
(concat "Hola" " " "món")

(subcadena "abcdef" 2 4)

(cadena 123)
```

---

## Diccionaris

```lisp
(definir persona
  (diccionari
      :nom "Anna"
      :edat 25))

(obté persona :nom)

(assigna persona :edat 26)
```

---

## Gestió d'errors

```lisp
(provar (/ 1 0) 999)
```

Retorna:

```text
999
```

---

## Macros

```lisp
(definir-macro quan
  (funció (cond . cos)
    (llista 'si cond
      (cons 'prova cos))))
```

Ús:

```lisp
(quan (> 3 2)
   (escriure "OK"))
```

---

## Compilació a Python

```lisp
(definir calcul
  (compila
    (+ 3 4)))

(calcul)
```

Resultat:

```text
7
```

També es poden compilar funcions:

```lisp
(definir doble-comp
  (compila
    (funció (x)
      (* x 2))))
```

---

## Traça d'execució

```lisp
(activar-traça)

(+ 1 2)

(desactivar-traça)
```

Sortida:

```text
-> (+ 1 2)
<- 3
```

---

# 🧪 Tests

Executa tota la bateria de proves:

```bash
python test_minicat_complet.py
```

Els tests cobreixen:

- aritmètica
- lògica
- variables
- funcions
- condicionals
- bucles
- excepcions
- llistes
- vectors
- cadenes
- diccionaris
- macros
- compilació
- TCO
- entrada/sortida
- càrrega de fitxers

---

# 📁 Estructura del projecte

```text
minicat/
├── minicat.py
├── test_minicat.py
├── LICENSE
└── README.md
```

---

# 👨‍💻 Autor

**Francesc Pérez García**

Projecte educatiu orientat a l'aprenentatge de:

- Llenguatges de programació
- Intèrprets
- Compiladors
- Programació funcional
- Metaprogramació amb macros

---

# 📜 Llicència

Aquest projecte es distribueix sota la llicència MIT.

Consulta el fitxer:

```text
LICENSE
```

per veure'n els detalls.

---

# 🌱 Possibles millores futures

- Sistema de mòduls
- Biblioteca estàndard ampliada
- Compilador WASM
- Compilador a C
- Editor gràfic propi
- Documentació interactiva
- Entorn educatiu per a instituts

---

**Gaudeix programant en català amb MiniCat! 🐾**
```````
