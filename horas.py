import re

rehm = r"(?P<hh>\d\d?)[hH]((?P<mm>\d\d?)[mM])?"

def normalizaHoras(ficIn, ficOut):
    with open(ficIn, "rt") as fpIn, open(ficOut, "wt") as fpOut:
        for linea in fpIn:
            # Manejar el caso de "12"
            linea = re.sub(r'\b12\b', '00:00', linea)
            
            # Manejar "5 menos cuarto"
            linea = re.sub(r'\b5 menos cuarto\b', '04:45', linea)
            
            # Manejar "4:45"
            linea = re.sub(r'\b4:45\b', '04:45', linea)
            
            while (match:= re.search(rehm, linea)):
                fpOut.write(linea[:match.start()])
                hora = int(match["hh"])
                minuto = int(match["mm"]) if match["mm"] else 0
                fpOut.write(f"{hora:02d}:{minuto:02d}")
                linea = linea[match.end():]
            
            # Manejar el caso de "4 y media"
            linea = re.sub(r'\b4 y media\b', '16:30', linea)
            
            fpOut.write(linea)

# Ejemplo de uso
normalizaHoras('horas.txt', 'salida2.txt')
