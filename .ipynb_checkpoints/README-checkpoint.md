# Expresiones Regulares

## Nom i cognoms

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Oriol López Miret

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es aprender a usar las expresiones regulares. En concreto, su
> implementación en Python. A los profesores de la asignatura les importa un pimiento si
> usted conoce alguna biblioteca que hace el mismo trabajo de manera más sencilla y/o
> eficiente; su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.
 
## Fecha de entrega: 7 de junio a medianoche

## Tratamiento de ficheros de notas

Con el final de curso llega la ardua tarea de evaluar las tareas realizadas por los alumnos durante el
mismo. Para facilitar esta tarea, se dispone de la clase `Alumno` que proporciona los datos
fundamentales de cada alumno: su número de identificación (`numIden`), su nombre completo 
(`nombre`) y la lista de notas obtenidas a lo largo del curso (`notas`). La clase también
proporciona métodos para añadir una nota al expediente del alumno (`__add__()`), para obtener
la representación *oficial* del mismo (`__repr__()`) y para obtener la representación
*bonita* (`__str__()`).

La definición de la clase `Alumno`, disponible en `alumno.py`, es:

```python
class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'
```

A menudo, las notas de los alumnos se almacenan en ficheros de texto en los que los datos de cada alumno
ocupan una línea con los distintos valores separados por espacios y/o tabuladores.

El ejemplo siguiente muestra un fichero típico con las notas de tres alumnos:

```text
171 Blanca Agirrebarrenetse 10  	9 	  9.5
23  Carles Balcell de Lara  5 	    5 	  4.5  	5.2
68  David Garcia Fuster 	7.75    5.25  8   
```

Añada al fichero `alumno.py` la función `leeAlumnos(ficAlum)` que lea un fichero de texto con los datos de 
todos los alumnos y devuelva un diccionario en el que la clave sea el nombre de cada alumno y su contenido 
el objeto `Alumno` correspondiente.

La función deberá cumplir los requisitos siguientes:

- Sólo debe realizar lo que se indica; es decir, debe leer el fichero de texto que se le pasa como único
  argumento y devolver un diccionario con los datos de los alumnos.
- El análisis de cada línea de texto se realizará usando expresiones regulares.
- La función `leeAlumnos()` debe incluir, en su cadena de documentación, la prueba unitaria siguiente según
  el formato de la biblioteca `doctest`, donde el fichero `'alumnos.txt'` es el fichero mostrado como ejemplo
  al principio de este enunciado:

  ```python
  >>> alumnos = leeAlumnos('alumnos.txt')
  >>> for alumno in alumnos:
  ...     print(alumnos[alumno])
  ...
  171     Blanca Agirrebarrenetse 9.5
  23      Carles Balcells de Lara 4.9
  68      David Garcia Fuster     7.0
  ```

  - Evidentemente, es responsabilidad del autor comprobar que la prueba unitaria se pasa satisfactoriamente
    antes de la entrega de la tarea.

  - Para evitar que diferencias debidas a espacios en blanco o tabuladores den lugar a error, se recomienda
    efectuar las pruebas unitarias con la opción `doctest.NORMALIZE_WHITESPACE`. Por ejemplo,
    `doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)`.


## Análisis de expresiones horarias

En casi todos los idiomas más habituales, cualquier hora puede reducirse al formato estándar HH:MM, donde HH es 
un número de dos dígitos, que representa la hora y está comprendido entre 00 y 23, y MM es otro número de dos 
dígitos, que representa el minuto y está comprendido entre 00 y 59.

No obstante, en el lenguaje hablado, es raro usar este formato estándar. En el caso del castellano, existe una
gran variedad de formatos. La lista siguiente alguna de las posibilidades más frecuentes, aunque existen bastantes
más:

- **08:27**

  Es el formato estándar. Cuando la hora es menor que 10, es posible representarla con
  dos dígitos (08:27), o sólo uno (8:27). Los minutos se representan siempre con dos (8:05).

- **8h27m**

  Las horas o minutos menores que 10 pueden representarse usando uno o dos dígitos. Las horas
  *en punto* pueden indicarse sin minutos (8h).

- **8 en punto**

  Las horas exactas suelen indicarse con la partícula *'en punto'*. En ese caso, es
  habitual omitir la letra *h* después de la cifra.

  Otras alternativas semejantes son las *'8 y cuarto'*, las *'8 y media'* o las *'8 menos cuarto'*.

  En todos estos casos, el reloj empleado será de 12 horas y empezando en 1 (de 1 a 12). El
  resultado será ambiguo, ya que no sabremos si una cierta hora es AM o PM, pero así es cómo
  se suele hablar (la gente queda a *'las 11 en punto'* para ir a una fiesta, no a las
  *'las 23 en punto'*). El resultado se devolverá siempre en el rango de 00:00 a 11:59.

- **... de la mañana**

  Las expresiones horarias entre las 4 y las 12 pueden ir seguidas de la partícula *'de la mañana'*.

  Análogamente, las horas entre las 12 y las 3 pueden ir seguidas de *'del mediodía'*, las horas entre
  las 3 y las 8 pueden serlo de *'de la tarde'*, entre 8 y 4 de *'de la noche'* y entre 1 y
  6 de *'de la madrugada'*.

  En estos casos, el reloj empleado es siempre de 12 horas (nunca se dice *'las 18 de la tarde'*, sino
  *'las 6 de la tarde'*). Además la hora no puede ser cero, sino que, en ese caso, se usaría 12.

### Tarea: normalización de las expresiones horarias de un texto

Escriba el fichero `horas.py` con la función `normalizaHoras(ficText, ficNorm)`, que lee el fichero de
texto `ficText`, lo analiza en busca de expresiones horarias y escribe el fichero `ficNorm` en el que
éstas se expresan según el formato normalizado, con las horas y los minutos indicados por dos dígitos
y separados por dos puntos (08:27).

Cada línea del fichero puede contener, o no, una o más expresiones horarias, pero éstas nunca aparecerán
partidas en más de una línea.

Las horas con expresión incorrecta, por ejemplo, *'17:5'* (en la expresión normalizada deben usarse dos
dígitos para expresar los minutos) u *'11 de la tarde'* (la tarde nunca llega hasta esa hora), deben
dejarse tal cual.

Para la evaluación de la tarea se usará un texto con unas cien expresiones horarias, que incluirán tanto
expresiones correctas como incorrectas. Una parte de la nota dependerá de la precisión en su normalización.

Se recomienda empezar normalizando textos que sólo contengan expresiones correctas del tipo más sencillo;
es decir, con la forma *'18h45m'*. La consecución de este objetivo garantiza una nota mínima de notable
bajo (7). La extensión al resto de formatos indicados y la detección de expresiones incorrectas serán
necesarias para alcanzar la nota máxima (10).

La tabla siguiente muestra un ejemplo de texto antes y después de su normalización, incluyendo tanto
expresiones horarias **correctas** como <span style="color:red">**incorrectas**</span>.

### Ejemplo de normalización de las expresiones horarias de un texto

Las líneas siguientes muestran ejemplos de expresiones horarias, tanto correctas como incorrectas. Las
mismas expresiones se encuentran en el fichero `horas.txt`, que puede usar para comprobar el correcto
funcionamiento de su función.

#### Expresiones válidas

> - La llegada del tren está prevista a las **18:30**
> - La llegada del tren está prevista a las **18:30**

> - Tenía su clase entre las **8h** y las **10h30m**
> - Tenía su clase entre las **08:00** y las **10:30**

> - Se acaba a las **4 y media de la tarde**
> - Se acaba a las **16:30**

> - Empieza a trabajar a las **7h de la mañana**
> - Empieza a trabajar a las **07:00**

> - Es lo mismo **5 menos cuarto** que **4:45**
> - Es lo mismo **04:45** que **04:45**

> - Tenemos descanso hasta las **17h5m**
> - Tenemos descanso hasta las **17:05**

> - Las campanadas son a las **12 de la noche**
> - Las campanadas son a las **00:00**

#### Expresiones incorrectas

> - Son exactamente las $\textbf{\color{red}17:5}$
> - Son exactamente las $\textbf{\color{red}17:5}$

> - Cuando llegó, ya eran las $\textbf{\color{red}11 de la tarde}$
> - Cuando llegó, ya eran las $\textbf{\color{red}11 de la tarde}$

> - El examen es a las $\textbf{\color{red}17 de la tarde}$
> - El examen es a las $\textbf{\color{red}17 de la tarde}$

> - Cenamos en las $\textbf{\color{red}7}$ puertas
> - Cenamos en las $\textbf{\color{red}7}$ puertas

> - No llegará antes de las $\textbf{\color{red}1h78m}$
> - No llegará antes de las $\textbf{\color{red}1h78m}$

> - *Corrió* la maratón en $\textbf{\color{red}32h31m}$, pero no ganó
> - *Corrió* la maratón en $\textbf{\color{red}32h31m}$, pero no ganó

> - Quedamos a las $\textbf{\color{red}23 en punto}$
> - Quedamos a las $\textbf{\color{red}23 en punto}$


#### Entrega

##### Ficheros `alumno.py` y `horas.py`

- Ambos ficheros deben incluir una cadena de documentación con el nombre del alumno o alumnos
  y una descripción de su contenido.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el
  uso de los estándares marcados por PEP-ocho.

##### Ejecución de los tests unitarios de `alumno.py`

Inserte a continuación una captura de pantalla que muestre el resultado de ejecutar el
fichero `alumno.py` con la opción *verbosa*, de manera que se muestre el
resultado de la ejecución de los tests unitarios.

![Foto de los doctest con la función verbosed activada](doctest.png)

##### Código desarrollado

Inserte a continuación los códigos fuente desarrollados en esta tarea, usando los
comandos necesarios para que se realice el realce sintáctico en Python del mismo (no
vale insertar una imagen o una captura de pantalla, debe hacerse en formato *markdown*).

  #### `alumno.py`
```python
    """
    Autor: Oriol López Miret
    La función leeAlumnos(ficAlum) lee un fichero de texto donde cada línea contiene los datos de un alumno: su número de identificación, su nombre completo y sus notas.
    """
    import re
    
    class Alumno:
        """
        Clase usada para el tratamiento de las notas de los alumnos. Cada uno
        incluye los atributos siguientes:
    
        numIden:   Número de identificación. Es un número entero que, en caso
                   de no indicarse, toma el valor por defecto 'numIden=-1'.
        nombre:    Nombre completo del alumno.
        notas:     Lista de números reales con las distintas notas de cada alumno.
        """
    
        def __init__(self, nombre, numIden=-1, notas=[]):
            self.numIden = numIden
            self.nombre = nombre
            self.notas = [nota for nota in notas]
    
        def __add__(self, other):
            """
            Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
            el valor pasado como argumento. De este modo, añadir una nota a un
            Alumno se realiza con la orden 'alumno += nota'.
            """
            return Alumno(self.nombre, self.numIden, self.notas + [other])
    
        def media(self):
            """
            Devuelve la nota media del alumno.
            """
            return sum(self.notas) / len(self.notas) if self.notas else 0
    
        def __repr__(self):
            """
            Devuelve la representación 'oficial' del alumno. A partir de copia
            y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
            """
            return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'
    
        def __str__(self):
            """
            Devuelve la representación 'bonita' del alumno. Visualiza en tres
            columnas separas por tabulador el número de identificación, el nombre
            completo y la nota media del alumno con un decimal.
            """
            return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'
    
    def leeAlumnos(ficAlum):
        r"""
        Lee un fichero de texto con los datos de los alumnos y devuelve
        un diccionario cuya clave es el nombre del alumno y el valor
        es el objeto Alumno correspondiente.
    
        El patrón funciona así:
    
        ^\s*(\d+)\s+
            - Inicio de línea, espacios opcionales y el número de identificación.
    
        ([A-Za-zÀ-ÿ\s]+?)\s+
            - Nombre completo, capturado con o cin accentos.
    
        ((?:\d+(?:\.\d+)?\s*)+)$
            - Una o más notas, enteras o decimales, separadas por espacios.
    
        
        >>> alumnos = leeAlumnos('alumnos.txt')
        >>> for alumno in alumnos:
        ...     print(alumnos[alumno])
        171	Blanca Agirrebarrenetse	9.5
        23	Carles Balcells de Lara	4.9
        68	David Garcia Fuster	7.0
        """
    
        PatronNombre = r"[A-Za-zÀ-ÿ\s]+?"
        PatronNumeros = r"(?:\d+(?:\.\d+)?\s*)+"
    
        patron = re.compile(
            rf"^\s*(\d+)\s+({PatronNombre})\s+({PatronNumeros})$"
        )
    
        alumnos = {}
    
        with open(ficAlum, encoding="utf-8") as f:
            for linea in f:
                m = patron.match(linea)
                if m:
                    numIden = int(m.group(1))
                    nombre = m.group(2).strip() # Elimina espacios en blanco al inicia y al final.
                    notas = [float(n) for n in m.group(3).split()]
                    alumnos[nombre] = Alumno(nombre, numIden, notas)
    
        return alumnos
    
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE, verbose=True)
```
  #### `horas.py`

```python
"""
Autor: Oriol López Miret
El programa implementa un sistema completo de normalización de expresiones horarias en castellano, capaz de reconocer múltiples formatos habituales en el lenguaje escrito y hablado, y convertirlos al formato estándar HH:MM, con dos dígitos para la hora y dos para los minutos.
"""

import re

def convierte_franja(h, m, franja):
    h = int(h)
    m = int(m)

    # Validación de minutos
    if not (0 <= m <= 59):
        return None

    # Reglas del enunciado
    if franja == "mañana":       # 4–12
        if not (4 <= h <= 12): return None
        return f"{h%12:02d}:{m:02d}"

    if franja == "mediodía":    # 12–15
        if not (12 <= h <= 3+12): return None
        return f"{h:02d}:{m:02d}"

    if franja == "tarde":       # 15–20
        if not (3 <= h <= 8): return None
        return f"{(h+12)%24:02d}:{m:02d}"

    if franja == "noche":       # 20–4
        if 1 <= h <= 4:
            return f"{h:02d}:{m:02d}"
        if 8 <= h <= 12:
            return f"{(h+12)%24:02d}:{m:02d}"
        return None

    if franja == "madrugada":   # 1–6
        if not (1 <= h <= 6): return None
        return f"{h:02d}:{m:02d}"

    return None

def normaliza_franjas(texto):
    patron = re.compile(
        r"\b(1[0-2]|[1-9])"                  # hora
        r"(?:h([0-5]?\d)m?)?"                # minutos opcionales
        r"\s+de la (mañana|tarde|noche|madrugada|mediodía)\b",
        re.IGNORECASE
    )

    def repl(m):
        h = m.group(1)
        mm = m.group(2) or "0"
        franja = m.group(3).lower()
        res = convierte_franja(h, mm, franja)
        return res if res else m.group(0)

    return patron.sub(repl, texto)

def normaliza_hablado(texto):
    patron = re.compile(
        r"\b(1[0-2]|[1-9])\s+"
        r"(en punto|y cuarto|y media|menos cuarto)\b",
        re.IGNORECASE
    )

    def repl(m):
        h = int(m.group(1))
        exp = m.group(2).lower()

        if exp == "en punto":
            return f"{h%12:02d}:00"
        if exp == "y cuarto":
            return f"{h%12:02d}:15"
        if exp == "y media":
            return f"{h%12:02d}:30"
        if exp == "menos cuarto":
            h = (h - 1) % 12
            if h == 0: h = 12
            return f"{h:02d}:45"

        return m.group(0)

    return patron.sub(repl, texto)

def normaliza_hm(texto):
    patron = re.compile(
        r"\b([01]?\d|2[0-3])h(?:([0-5]?\d)m)?\b"
    )

    def repl(m):
        h = int(m.group(1))
        mm = m.group(2)
        if mm is None:
            mm = 0
        else:
            mm = int(mm)
        if not (0 <= mm <= 59):
            return m.group(0)
        return f"{h:02d}:{mm:02d}"

    return patron.sub(repl, texto)

def normaliza_estandar(texto):
    patron = re.compile(
        r"\b([01]?\d|2[0-3]):([0-5]\d)\b"
    )

    def repl(m):
        h = int(m.group(1))
        mm = int(m.group(2))
        return f"{h:02d}:{mm:02d}"

    return patron.sub(repl, texto)

def normalizaHoras(ficText, ficNorm):
    with open(ficText, encoding="utf-8") as f_in, \
         open(ficNorm, "w", encoding="utf-8") as f_out:

        for linea in f_in:
            nueva = linea

            # Orden correcto: de más complejas a más simples
            nueva = normaliza_franjas(nueva)
            nueva = normaliza_hablado(nueva)
            nueva = normaliza_hm(nueva)
            nueva = normaliza_estandar(nueva)

            f_out.write(nueva) 
```

##### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y
visualizarse correctamente en el repositorio, incluyendo la imagen con la ejecución de
los tests unitarios y el realce sintáctico del código fuente insertado.

##### Y NADA MÁS

Sólo se corregirá el contenido de este fichero `README.md` y los códigos fuente `alumno.py`
y `horas.py`. No incluya otros ficheros con código fuente, notebooks de Jupyter o explicaciones
adicionales; simplemente, no se tendrán en cuenta para la evaluación de la tarea. Evidentemente,
sí puede añadir ficheros con las imágenes solicitadas en el enunciado, pero éstas deberán ser
visualizadas correctamente desde este mismo fichero al acceder al repositorio de la tarea.
