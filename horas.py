"""
Nombre: Yago Carballo Barroso
"""
import re

re_ex1 = r"(?P<hh>\d\d?)[hH\:]((?P<mm>\d\d?)(?:[mM])*)"
re_ex2 = r"\s(?P<h>\d\d?)\w?\s(?:(?P<en_punto>en punto)|(?P<y_media>y media)|(?P<menos_cuarto>menos cuarto)|(?P<y_cuarto>y cuarto))?\s?(?:(?P<mañana>de la mañana)|(?P<tarde>de la tarde)|(?P<noche>de la noche)|(?P<mediodia>del mediodia)|(?P<madrugada>de la madrugada))?"

def normalizaHoras(ficIn, ficOut):
    with open(ficIn, "rt") as fIn, open(ficOut, "wt") as fOut:
        for linea in fIn:
            while any([(match1 := re.search(re_ex1, linea)), (match2 := re.search(re_ex2, linea))]):
                if match1:
                    hora = int(match1["hh"])
                    minuto = int(match1["mm"]) if match1["mm"] else 0
                    if hora < 24 and minuto < 60:
                        linea = f'{linea[:match1.start()]}{hora:02d}:{minuto:02d}{linea[match1.end():]}'
                        if not match2:
                            fOut.write(linea[:match1.end()])
                            linea = linea[match1.end():]
                    else:
                        fOut.write(linea[:match1.end()])
                        if match2:
                            if match2.start() > match1.start():
                                linea = linea[match1.end():]
                        else:
                            linea = linea[match1.end():]

                    


                if match2 := re.search(re_ex2, linea):
                    hora = int(match2["h"])
                    alone = True
                    error = False
                    if hora > 12:
                        fOut.write(linea[:match2.end()])
                        linea = linea[match2.end():]
                        continue
                    if match2["mañana"]:
                        alone = False
                        if hora < 6:
                            error = True
                            fOut.write(linea[:match2.end()])
                            linea = linea[match2.end():]
                            continue
                    elif match2["tarde"]:
                        alone = False
                        if hora < 1 or hora > 8:
                            error = True
                            fOut.write(linea[:match2.end()])
                            linea = linea[match2.end():]
                            continue
                        else: 
                            hora += 12
                    elif match2["noche"]:
                        alone = False
                        if hora < 9:
                            error = True
                            fOut.write(linea[:match2.end()])
                            linea = linea[match2.end():]
                            continue
                        elif hora == 12:
                            hora = 0
                        else:
                            hora += 12
                    elif match2["madrugada"]:
                        alone = False
                        if hora > 5:
                            error = True
                            fOut.write(linea[:match2.end()])
                            linea = linea[match2.end():]
                            continue
                    
                    if match2["y_media"]:
                        alone = False
                        hora_formateada = f' {hora:02d}:30 '
                    elif match2["menos_cuarto"]:
                        alone = False
                        hora_formateada = f' {hora-1:02d}:45 '
                    elif match2["y_cuarto"]:
                        alone = False
                        hora_formateada = f' {hora:02d}:15 '
                    else:
                        hora_formateada = f' {hora:02d}:00 '

                    if re.match(r"^\d+\s?$", linea[match2.start()+1:match2.end()]):
                        alone = True
                    else:
                        alone = False
                    
                    if not (alone or error):
                        fOut.write(linea[:match2.start()])
                        fOut.write(hora_formateada)
                        linea = linea[match2.end():]

                    else:
                        fOut.write(linea[:match2.end()])
                        linea = linea[match2.end():]
                        
            fOut.write(linea)


if __name__ == "__main__":
    normalizaHoras(ficIn="horas.txt", ficOut="salida.txt")
