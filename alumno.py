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