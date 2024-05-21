import re

rehoras = r"(?P<hh>\d\d?)(?P<h>[hH:]?)(?P<mm>\d(?P<min_digit>\d?))?[mM]?"
redia = r"de la (?P<mom>tarde|noche|mañana)"
repartes = r"\w+\s+(?P<parte>punto|media)"
recuartos = r"(?P<ym>y|menos)\s+(?P<cuarto>cuarto)"

def normalizaHoras(fin, fout):
    with open(fin, "rt") as fi, open(fout, "wt") as fo:
        for linea in fi:
            #if (match:=re.match(rehoras, linea)):
                while (match:=re.search(rehoras, linea)):
                    hora = int(match["hh"])
                    minuto = int(match["mm"]) if match["mm"] else 0
                    h = match["h"]
                    min_digit = match["min_digit"]
                    if minuto > 59 or hora > 23:
                        fo.write(linea[:match.end()])
                        linea = linea[match.end():]
                    
                    else:
                        fo.write(linea[:match.start()])
                        linea = linea[match.end():]

                        if match:=re.search(redia, linea):
                            if hora > 12:
                                fo.write(f"{hora}")
                                fo.write(linea[:match.end()])
                                linea = linea[match.end():]
                                continue
                            elif match["mom"] == "mañana":
                                if 6 <= hora <= 12:
                                    pass
                                else:
                                    fo.write(f"{hora}")
                                    fo.write(linea[:match.end()])
                                    linea = linea[match.end():]
                                    continue
                            elif match["mom"] == "tarde":
                                if hora == 12 or 1 <= hora <= 7:
                                    hora += 12
                                else:
                                    fo.write(f"{hora}")
                                    fo.write(linea[:match.end()])
                                    linea = linea[match.end():]
                                    continue
                            elif match["mom"] == "noche":
                                if 7 <= hora <= 12:
                                    hora += 12
                                    if hora == 24:
                                        hora = 0
                                else:
                                    fo.write(f"{hora}")
                                    fo.write(linea[:match.end()])
                                    linea = linea[match.end():]
                                    continue
                            linea = linea[match.end():] 
                            fo.write(f"{hora:02d}:{minuto:02d}")

                        elif match:=re.search(repartes, linea):
                            if hora > 12:
                                fo.write(f"{hora}")
                                fo.write(linea[:match.end()])
                                linea = linea[match.end():]
                                continue
                            if match["parte"] == "media":
                                minuto = 30
                            linea = linea[match.end():]  
                            fo.write(f"{hora:02d}:{minuto:02d}") 

                        elif match:=re.search(recuartos, linea):
                            if match["ym"] == "y":
                                minuto = 15
                            else:
                                minuto = 45
                                hora -= 1
                            linea = linea[match.end():]
                            fo.write(f"{hora:02d}:{minuto:02d}")

                        elif h:
                            if h == ":" and not min_digit:
                                fo.write(f"{hora}{h}{minuto}")
                            else:
                                fo.write(f"{hora:02d}:{minuto:02d}")

                        else:
                            fo.write(f"{hora}")
                                           
                fo.write(linea)