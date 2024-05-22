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

format_hm = r"(?P<hh>\d\d?)[hH]((?P<mm>\d\d?)[mM])?"
format_dig = r"(?P<hh>\d\d?):(?P<mm>\d\d?)"
format_rodo = r"(?P<hh>\d\d?)h?" #(?P<reloj>[(en punto)(y cuarto)(y media)(menos cuarto)])?"
# format_dia = r"(((?P<hh>\d\d?):(?P<mm>\d\d?))|((?P<hh>\d\d?)h?))"
format_dia = r"(((?P<hh>\d\d?):(?P<mm>\d\d?))|((?P<hh>\d\d?)h?))(?P<mig>\w*)(?P<momento>(madrugada)|(mañana)|(mediodía)|(tarde)|(noche))"
#mañana, tarde, noche
# en punto

def normalizaHoras(ficIn, ficOut):
    with open(ficIn, "rt") as fpIn, open(ficOut, "wt") as fpOut:
        for linia in fpIn:
            while (match := re.search(format_hm, linia)):
                fpOut.write(linia[:match.start()])
                hora = int(match["hh"])
                minuto = int(match["mm"]) if match["mm"] else 0
                if hora < 24:
                    fpOut.write(f"{hora:02d}:{minuto:02d}")
                else:
                    fpOut.write(f"{hora} horas y {minuto} minutos")
                linia = linia[match.end():]
            while (match := re.search(format_dig, linia)):
                fpOut.write(linia[:match.start()])
                hora = int(match["hh"])
                minuto = int(match["mm"])
                fpOut.write(f"{hora:02d}:{minuto:02d}")
                linia = linia[match.end():]
            while (match := re.search(format_rodo, linia)):
                fpOut.write(linia[:match.start()])
                hora = int(match["hh"])
                if hora > 12 and hora < 24:
                    hora -= 12
                else:
                    ValueError("Aquesta hora no existeix")
                fpOut.write(f"{hora}")
                linia = linia[match.end():]
            while (match := re.search(format_dia, linia)):
                fpOut.write(linia[:match.start()])
                hora = int(match["h"])
                momento = match["momento"]
                mig = match["mig"]
                # if hora < 24 and hora > 13:
                #     hora += 12
                if hora > 6 and hora < 13 and momento != "mañana":
                    momento = "mañana"
                elif hora > 12 and hora < 16 and momento != "mediodía":
                    momento = "mediodía"
                elif hora > 15 and hora < 21 and momento != "tarde":
                    momento = "tarde"
                elif hora > 20 and hora < 25 and hora < 4 and momento != "noche":
                    momento = "noche"
                elif hora > 0 and hora < 7 and momento != "noche":
                    momento = "noche"
                fpOut.write(f"{hora} {mig} {momento}")

            fpOut.write(linia)

salida = "salida.txt"
a = normalizaHoras("horas.txt", salida)