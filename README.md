
# MiniCat 🐱

**MiniCat** és un mini-llenguatge de programació funcional amb sintaxi Lisp i **paraules clau en català**.  
El seu intèrpret complet ocupa menys de 200 línies de Python i està pensat per ser didàctic, entenedor i fàcil de modificar.

## ✨ Característiques

- Sintaxi mínima basada en expressions S (tot entre parèntesis)
- Paraules reservades en català: `definir`, `funció`, `si`, `escriure`...
- Tipus de dades: nombres, cadenes de text, llistes i funcions (clausures)
- Àmbit lèxic: les funcions capturen l'entorn on es defineixen
- 100% funcional: totes les expressions retornen un valor
- REPL interactiu i capacitat d'executar fitxers `.cat`
- Pont amb Python mitjançant la funció `carrega`

## 📦 Requisits

- Python 3.6 o superior (cap dependència externa)

## 🚀 Instal·lació i ús

1. **Descarrega o clona el repositori:**

   ```bash
   git clone https://github.com/drfperez/minicat.git
   cd minicat
```

2. Executa en mode interactiu (REPL):
   ```bash
   python minicat.py
   ```
   Sortida:
   ```
   MiniCat REPL. Escriu 'sortir' per acabar.
   minicat> 
   ```
3. Executa un fitxer d'exemple:
   ```bash
   python minicat.py exemples/hola_mon.cat
   ```
   Altres exemples:
   ```bash
   python minicat.py exemples/factorial.cat
   python minicat.py exemples/funcions.cat
   ```

📖 Sintaxi bàsica

Tot en MiniCat són expressions entre parèntesis amb notació prefixada (la funció va al davant):

```lisp
(funció arguments...)
```

Exemples ràpids

Hola món:

```lisp
(escriure "Hola món!")
```

Variables i condicionals:

```lisp
(definir x 10)
(si (> x 5) (escriure "gran") (escriure "petit"))
```

Funcions:

```lisp
(definir doble (funció (x) (* x 2)))
(escriure (doble 5))   ; mostra 10
```

Factorial recursiu:

```lisp
(definir factorial
  (funció (n)
    (si (<= n 1)
        1
        (* n (factorial (- n 1))))))

(escriure "El factorial de 5 és:" (factorial 5))
```

Funcions d'ordre superior:

```lisp
(definir aplica (funció (f x) (f x)))
(escriure (aplica doble 7))   ; mostra 14
```

Llistes:

```lisp
(definir nums (llista 1 2 3 4 5))
(escriure nums)
```

Ús de mòduls Python:

```lisp
(definir math (carrega "math"))
(escriure "Pi val:" math.pi)
```

📚 Paraules clau i primitives

| Paraula       | Descripció |
|---------------|------------|
| `definir`     | Assigna un valor a un nom |
| `funció`      | Crea una funció anònima (lambda) |
| `si`          | Condicional (expressió) |
| `escriure`    | Mostra text per pantalla |
| `prova`       | Seqüència d'expressions (retorna l'última) |
| `llista`      | Crea una llista amb els arguments |
| `carrega`     | Importa un mòdul de Python |
| `+`, `-`, `*`, `/` | Operadors aritmètics |
| `=`, `<`, `>`, `<=`, `>=` | Comparacions |
| `i`, `o`, `no` | Operadors lògics |

🎯 Filosofia

MiniCat demostra que es pot construir un llenguatge de programació complet amb molt poques línies de codi, fent servir la llengua materna per facilitar l'aprenentatge. És una eina ideal per a cursos d'introducció a la programació o per entendre com funcionen els intèrprets per dins.

📄 Estructura del repositori

```
minicat/
├── README.md
├── LICENSE
├── .gitignore
├── minicat.py              ← l'intèrpret principal
└── exemples/
    ├── hola_mon.cat
    ├── factorial.cat
    └── funcions.cat
```

📝 Llicència

Aquest projecte es distribueix sota la llicència MIT. Consulteu el fitxer LICENSE per a més informació.

