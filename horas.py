import re

re_ex1 = r"(?P<hh>\d\d?)[hH]((?P<mm>\d\d?)[mM])?"

def normalizaHoras(ficIn, ficOut):
    with open(ficIn, "rt") as fIn, open(ficOut, "wt") as fOut:
        for linea in fIn:
            while (match := re.search(re_ex1, linea)):
                fOut.write(linea[:match.start()])
                hora = int(match["hh"])
                minuto = int(match["mm"]) if match["mm"] else 0
                fOut.write(f"{hora:02d}:{minuto:02d}")
                linea = linea[match.end():]
            fOut.write(linea)


