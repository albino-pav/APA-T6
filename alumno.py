import re
from alumno_class import Alumno

def leeAlumnos(ficAlum):
    """
    Lee un fichero de texto con los datos de todos los alumnos y devuelve un diccionario
    donde la clave es el nombre de cada alumno y el valor es el objeto Alumno correspondiente,
    con la media de las notas calculada.

    :param ficAlum: Nombre del fichero de texto con los datos de los alumnos.
    :return: Diccionario con los datos de los alumnos y su media de notas.
    
    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171     Blanca Agirrebarrenetse 9.5
    23      Carles Balcells de Lara 4.9
    68      David Garcia Fuster     7.0
    """
    alumnos_dict = {}
    with open(ficAlum, 'r') as file:
        for line in file:
            match = re.match(r'(\d+)\s+([^\d]+)\s+((?:\d*\.?\d+\s+)+)', line)
            if match:
                numIden = int(match.group(1))
                nombre = match.group(2)
                todas = [float(nota) for nota in match.group(3).split()]

                alumno = Alumno(nombre, numIden, todas)
                alumnos_dict[nombre] = alumno
                for alumno in alumnos_dict.values():
                    alumno.notas = [alumno.media()]

    return alumnos_dict

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE, verbose=True)
