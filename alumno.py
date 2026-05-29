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
    Lee un fichero de texto con los datos de todos los alumnos y devuelve 
    un diccionario en el que la clave sea el nombre de cada alumno y su 
    contenido el objeto Alumno correspondiente.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171\tBlanca Agirrebarrenetse\t9.5
    23\tCarles Balcell de Lara\t4.9
    68\tDavid Garcia Fuster\t7.0
    """
    diccionario_alumnos = {}
    
    # Expresión regular para capturar: ID, Nombre (mínimo emparejamiento) y bloque de notas
    patron = r'^\s*(\d+)\s+(.+?)\s+((?:\d+(?:\.\d+)?\s*)+)\s*$'
    
    with open(ficAlum, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
                
            match = re.match(patron, linea)
            if match:
                num_id = int(match.group(1))
                nombre = match.group(2).strip()
                bloque_notas = match.group(3)
                
                # Extraemos todas las notas individuales del bloque final
                notas = [float(n) for n in re.findall(r'\d+(?:\.\d+)?', bloque_notas)]
                
                # Creamos el objeto Alumno y lo guardamos
                diccionario_alumnos[nombre] = Alumno(nombre, num_id, notas)
                
    return diccionario_alumnos


if __name__ == "__main__":
    import doctest
    # NORMALIZE_WHITESPACE evita fallos por diferencias entre pestañas y espacios
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE, verbose=True)
