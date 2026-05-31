# Expresiones Regulares

## Nom i cognoms

Pedro Muñoz Álvarez

## Ejecución de los tests unitarios de alumno.py

A continuación se muestra el resultado de ejecutar los tests unitarios con la opción verbosa:

![Captura de los tests unitarios 1](Captura%201%20P6%20APA.PNG)

![Captura de los tests unitarios 2](Captura%202%20P6%20APA.PNG)

## Código desarrollado

### `alumno.py`

```python
import re
import doctest

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
    Lee un fichero de texto con los datos de todos los alumnos y devuelve un
    diccionario en el que la clave es el nombre de cada alumno y su contenido
    el objeto Alumno correspondiente.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171	Blanca Agirrebarrenetse	9.5
    23	Carles Balcell de Lara	4.9
    68	David Garcia Fuster	7.0
    """
    
    patron = re.compile(r'^\s*(\d+)\s+([A-Za-zÀ-ÿ\s]+?)\s+([\d\.\s]+)$')
    diccionario_alumnos = {}
    
    with open(ficAlum, 'r', encoding='utf-8') as fichero:
        for linea in fichero:
            linea = linea.strip() 
            if not linea:
                continue
                
            match = patron.match(linea)
            if match:
                numIden = int(match.group(1))
                nombre = match.group(2).strip()
                
                notas_str = match.group(3).split()
                notas = [float(nota) for nota in notas_str]
                
                diccionario_alumnos[nombre] = Alumno(nombre, numIden, notas)
                
    return diccionario_alumnos

if __name__ == "__main__":
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
```

### `horas.py`

```python
import re

def procesar_coincidencia(match):
    """
    Función auxiliar que decide si una coincidencia de la expresión regular
    es una hora válida y, si lo es, la transforma al formato HH:MM.
    """
    texto_original = match.group(0)
    
    h_str = match.group('h1') or match.group('h2') or match.group('h3')
    if not h_str: 
        return texto_original
    
    hora = int(h_str)
    minutos = 0
    
    if match.group('minutos'):
        minutos = int(match.group('minutos'))
        if minutos > 59 or hora > 23: 
            return texto_original

    elif match.group('texto_min'):
        texto_min = match.group('texto_min').lower()
        if 'y cuarto' in texto_min: minutos = 15
        elif 'y media' in texto_min: minutos = 30
        elif 'menos cuarto' in texto_min:
            minutos = 45
            hora -= 1 
        elif 'en punto' in texto_min: minutos = 0
        
        hora_original = int(h_str)
        if not (1 <= hora_original <= 12): 
            return texto_original
        
        if hora == 0: hora = 12 
        elif hora == -1: hora = 11

    modificador = match.group('mod')
    
    if modificador:
        modificador = modificador.lower()
        hora_original = int(h_str) 
        
        if not (1 <= hora_original <= 12):
            return texto_original
            
        if 'mañana' in modificador: 
            if not (4 <= hora_original <= 12): return texto_original
            if hora == 12: hora = 0
        elif 'mediodía' in modificador:
            if not (1 <= hora_original <= 3 or hora_original == 12): return texto_original
            if hora != 12: hora += 12
        elif 'tarde' in modificador: 
            if not (3 <= hora_original <= 8): return texto_original
            if hora != 12: hora += 12
        elif 'noche' in modificador: 
            if not (8 <= hora_original <= 12 or 1 <= hora_original <= 4): return texto_original
            if hora == 12: hora = 0
            elif hora < 12: hora += 12
        elif 'madrugada' in modificador: 
            if not (1 <= hora_original <= 6): return texto_original
    else:
        if match.group('texto_min'):
            if hora == 12: hora = 0
    
    return f"{hora:02d}:{minutos:02d}"

def normalizaHoras(ficText, ficNorm):
    """
    Autor: Pedro
    Lee ficText, busca expresiones horarias mediante regex y las normaliza a 
    formato estándar HH:MM en el archivo ficNorm.
    """
    patron = re.compile(
        r'\b(?:'
        r'(?P<h1>\d{1,2})(?P<sep>[:h])(?P<minutos>\d{2})m?\b|' 
        r'(?P<h2>\d{1,2})h\b|'
        r'(?P<h3>\d{1,2})\s+(?P<texto_min>en punto|y cuarto|y media|menos cuarto)\b'
        r')'
        r'(?:\s+(?P<mod>de la mañana|del mediodía|de la tarde|de la noche|de la madrugada))?',
        re.IGNORECASE
    )

    with open(ficText, 'r', encoding='utf-8') as f_in, \
         open(ficNorm, 'w', encoding='utf-8') as f_out:
        for linea in f_in:
            linea_mod = patron.sub(procesar_coincidencia, linea)
            f_out.write(linea_mod)

if __name__ == "__main__":
    normalizaHoras('horas.txt', 'horas_normalizadas.txt')
```
