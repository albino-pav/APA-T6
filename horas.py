import re

rehm = r"(?P<hh>\d\d?)[hH]((?P<mm>\d\d?)[mM])?"

def normalizaHoras(ficIn, ficOut):
    with open(ficIn, "rt") as fpIn, open(ficOut, "wt") as fpOut:
        for linia in fpIn:
            while (match := re.search(rehm, linia)):
                fpOut.write(linia[:match.start()])
                hora = int(match["hh"])
                minuto = int(match["mm"]) if match["mm"] else 0
                fpOut.write(f"{hora:02d}:{minuto:02d}")
                linia = linia[match.end():]
            fpOut.write(linia)

