"""
Alumno - Tratamiento de notas de alumnos con expresiones regulares.
Autor: Sandra Cots Agüera
"""

import re
import doctest


def leeAlumnos(ficAlum):
    """
    Lee un fichero de texto con datos de alumnos y devuelve un diccionario
    cuya clave es el nombre del alumno y el valor es el objeto Alumno.

    Cada línea del fichero tiene el formato:
        numIden  Nombre Completo  nota1  nota2  ...

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171     Blanca Agirrebarrenetse 9.5
    23      Carles Balcell de Lara  4.9
    68      David Garcia Fuster     7.0
    """
    alumnos = {}
    patron = re.compile(
        r'^\s*(\d+)\s+'           # numIden
        r'([A-Za-záéíóúÁÉÍÓÚüÜñÑ]+'  # primera palabra del nombre
        r'(?:\s+[A-Za-záéíóúÁÉÍÓÚüÜñÑ]+)*)\s+'  # resto de palabras del nombre
        r'([\d.]+(?:\s+[\d.]+)*)\s*$'  # notas
    )
    with open(ficAlum, encoding='utf-8') as f:
        for linea in f:
            m = patron.match(linea)
            if not m:
                continue
            numIden = int(m.group(1))
            nombre = m.group(2)
            notas = [float(n) for n in re.findall(r'[\d.]+', m.group(3))]
            alumnos[nombre] = Alumno(nombre, numIden, notas)
    return alumnos


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


if __name__ == '__main__':
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE, verbose=True)
