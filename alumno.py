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
        self.nombre = nombre
        self.numIden = numIden
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

info_alumno = r"(?P<id>\d+)\s+(?P<nom>[a-zA-ZàÀèÈéÉòÒóÓíÍúÚçÇ\s]+)\s+(?P<notas>(\d+(?:[.,]\d+)?(?:\s+|$))*)"

def leeAlumnos(ficAlum):
    alumnos = {}
    with open(ficAlum, "rt") as fpIn:
        for linia in fpIn:
            while (match := re.search(info_alumno, linia)):
                lista_notas = list(map(float, match["notas"].split()))
                alumno = Alumno(match["id"], match["nom"], match["notas"])
                alumno.media()
                alumnos[match['id']] = alumno
            #     fpOut.write(linia[:match.start()])
            #     hora = int(match["hh"])
            #     minuto = int(match["mm"]) if match["mm"] else 0
            #     fpOut.write(f"{hora:02d}:{minuto:02d}")
            #     linia = linia[match.end():]
            # fpOut.write(linia)

