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
    Lee el fichero de alumnos y devuelve un diccionario con nombre -> Alumno.
    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in sorted(alumnos.keys()):
    ...     print(alumnos[alumno])
    171	Blanca Agirrebarrenetse	9.5
    23	Carles Balcell de Lara	4.9
    68	David Garcia Fuster	7.0
    """
    alumnos = {}
    
    with open(ficAlum, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            
            # Separar por espacios en blanco
            partes = linea.split()
            if len(partes) < 2:
                continue
            
            # Primera parte: ID
            numIden = int(partes[0])
            
            # Buscar dónde empiezan las notas (buscamos números)
            notas = []
            idx_primer_numero = len(partes)
            
            for i in range(1, len(partes)):
                try:
                    float(partes[i])
                    idx_primer_numero = i
                    break
                except:
                    pass
            
            # Nombre es todo entre el ID y las notas
            nombre = ' '.join(partes[1:idx_primer_numero])
            
            # Notas son los números al final
            for i in range(idx_primer_numero, len(partes)):
                try:
                    notas.append(float(partes[i]))
                except:
                    pass
            
            alumno = Alumno(nombre, numIden, notas)
            alumnos[nombre] = alumno
    
    return alumnos


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
