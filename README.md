# Expresiones Regulares

## Nom i cognoms

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Carolina Villarraga Pérez

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

![Ejecución de los tests unitarios](./captura_doctest.png)

##### Código desarrollado


## Código desarrollado

### Código de `alumno.py`

```python
"""
Tratamiento de ficheros de notas de alumnos.

Autora: Carolina Villarraga Pérez

Este módulo contiene la clase Alumno y la función leeAlumnos(), que permite
leer un fichero de texto con los datos de varios alumnos usando expresiones
regulares.
"""

import doctest
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
    """
    Lee un fichero de alumnos y devuelve un diccionario.

    La clave del diccionario es el nombre completo del alumno y el valor es
    el objeto Alumno correspondiente.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171     Blanca Agirrebarrenetse 9.5
    23      Carles Balcells de Lara 4.9
    68      David Garcia Fuster     7.0
    """
    alumnos = {}

    patron_linea = re.compile(
        r"^\s*"
        r"(?P<num_iden>\d+)"
        r"\s+"
        r"(?P<nombre>[^\d]+?)"
        r"\s+"
        r"(?P<notas>(?:\d+(?:\.\d+)?\s*)+)"
        r"$"
    )

    with open(ficAlum, encoding="utf-8") as fichero:
        for linea in fichero:
            coincidencia = patron_linea.fullmatch(linea)

            if coincidencia:
                num_iden = int(coincidencia.group("num_iden"))
                nombre = " ".join(coincidencia.group("nombre").split())
                notas_texto = coincidencia.group("notas")

                notas = [
                    float(nota)
                    for nota in re.findall(r"\d+(?:\.\d+)?", notas_texto)
                ]

                alumnos[nombre] = Alumno(nombre, num_iden, notas)

    return alumnos


if __name__ == "__main__":
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE, verbose=True)
```

### Código de `horas.py`

```python
"""
Normalización de expresiones horarias.

Autora: Carolina Villarraga Pérez

Este módulo contiene la función normalizaHoras(), que lee un fichero de texto,
detecta expresiones horarias mediante expresiones regulares y escribe otro
fichero con dichas horas normalizadas al formato HH:MM.
"""

import re


PERIODO_RE = (
    r"de\s+la\s+mañana|"
    r"del\s+mediod[ií]a|"
    r"de\s+la\s+tarde|"
    r"de\s+la\s+noche|"
    r"de\s+la\s+madrugada"
)

PATRON_PERIODO = re.compile(
    rf"""
    (?<!\d)
    (?P<hora>\d{{1,2}})
    (?:
        h(?:(?P<min_h>\d{{1,2}})m)?
      |
        \s+(?P<expr>en\s+punto|y\s+cuarto|y\s+media|menos\s+cuarto)
    )?
    \s+(?P<periodo>{PERIODO_RE})
    (?!\w)
    """,
    re.IGNORECASE | re.VERBOSE,
)

PATRON_HM = re.compile(
    rf"""
    (?<!\d)
    (?P<hora>\d{{1,2}})h(?:(?P<minuto>\d{{1,2}})m)?
    (?!\w)
    (?!\s+(?:{PERIODO_RE}))
    """,
    re.IGNORECASE | re.VERBOSE,
)

PATRON_HABLADA = re.compile(
    r"""
    (?<!\d)
    (?P<hora>\d{1,2})
    \s+(?P<expr>en\s+punto|y\s+cuarto|y\s+media|menos\s+cuarto)
    (?!\w)
    """,
    re.IGNORECASE | re.VERBOSE,
)

PATRON_DOS_PUNTOS = re.compile(
    r"(?<!\d)(?P<hora>\d{1,2}):(?P<minuto>\d{2})(?!\d)"
)


def _formatea(hora, minuto):
    return f"{hora:02d}:{minuto:02d}"


def _periodo_clave(periodo):
    periodo = periodo.lower().replace("í", "i")
    periodo = re.sub(r"\s+", " ", periodo.strip())

    if periodo == "de la mañana":
        return "manana"
    if periodo == "del mediodia":
        return "mediodia"
    if periodo == "de la tarde":
        return "tarde"
    if periodo == "de la noche":
        return "noche"
    if periodo == "de la madrugada":
        return "madrugada"

    return ""


def _hora_segun_periodo(hora, periodo):
    if not 1 <= hora <= 12:
        return None

    clave = _periodo_clave(periodo)

    if clave == "manana" and 4 <= hora <= 12:
        return 12 if hora == 12 else hora

    if clave == "mediodia":
        if hora == 12:
            return 12
        if 1 <= hora <= 3:
            return hora + 12

    if clave == "tarde" and 3 <= hora <= 8:
        return hora + 12

    if clave == "noche":
        if hora == 12:
            return 0
        if 8 <= hora <= 11:
            return hora + 12
        if 1 <= hora <= 4:
            return hora

    if clave == "madrugada" and 1 <= hora <= 6:
        return hora

    return None


def _aplica_expresion(hora, expresion, periodo=None):
    if periodo is None:
        if not 1 <= hora <= 12:
            return None
        hora_24 = 0 if hora == 12 else hora
        modulo = 12
    else:
        hora_24 = _hora_segun_periodo(hora, periodo)
        modulo = 24

        if hora_24 is None:
            return None

    if expresion is None:
        minuto = 0
    else:
        expresion = re.sub(r"\s+", " ", expresion.lower().strip())

        if expresion == "en punto":
            minuto = 0
        elif expresion == "y cuarto":
            minuto = 15
        elif expresion == "y media":
            minuto = 30
        elif expresion == "menos cuarto":
            hora_24 = (hora_24 - 1) % modulo
            minuto = 45
        else:
            return None

    return hora_24, minuto


def _sustituye_periodo(coincidencia):
    original = coincidencia.group(0)
    hora = int(coincidencia.group("hora"))
    minuto_h = coincidencia.group("min_h")
    expresion = coincidencia.group("expr")
    periodo = coincidencia.group("periodo")

    if minuto_h is not None:
        minuto = int(minuto_h)

        if not 0 <= minuto <= 59:
            return original

        hora_24 = _hora_segun_periodo(hora, periodo)

        if hora_24 is None:
            return original

        return _formatea(hora_24, minuto)

    resultado = _aplica_expresion(hora, expresion, periodo)

    if resultado is None:
        return original

    return _formatea(*resultado)


def _sustituye_hm(coincidencia):
    original = coincidencia.group(0)
    hora = int(coincidencia.group("hora"))
    minuto = coincidencia.group("minuto")
    minuto = 0 if minuto is None else int(minuto)

    if 0 <= hora <= 23 and 0 <= minuto <= 59:
        return _formatea(hora, minuto)

    return original


def _sustituye_hablada(coincidencia):
    original = coincidencia.group(0)
    hora = int(coincidencia.group("hora"))
    expresion = coincidencia.group("expr")
    resultado = _aplica_expresion(hora, expresion)

    if resultado is None:
        return original

    return _formatea(*resultado)


def _sustituye_dos_puntos(coincidencia):
    original = coincidencia.group(0)
    hora = int(coincidencia.group("hora"))
    minuto = int(coincidencia.group("minuto"))

    if 0 <= hora <= 23 and 0 <= minuto <= 59:
        return _formatea(hora, minuto)

    return original


def _normaliza_linea(linea):
    linea = PATRON_PERIODO.sub(_sustituye_periodo, linea)
    linea = PATRON_HM.sub(_sustituye_hm, linea)
    linea = PATRON_HABLADA.sub(_sustituye_hablada, linea)
    linea = PATRON_DOS_PUNTOS.sub(_sustituye_dos_puntos, linea)

    return linea


def normalizaHoras(ficText, ficNorm):
    with open(ficText, encoding="utf-8") as entrada:
        with open(ficNorm, "w", encoding="utf-8") as salida:
            for linea in entrada:
                salida.write(_normaliza_linea(linea))
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
