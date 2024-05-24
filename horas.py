import re

form_hm = r'(?P<h>\d\d?)[hH]((?P<m>\d\d?)[mM])?'
form_hora = r'(?P<h>\d\d?) (?P<c>(en punto|y cuarto|y media|menos cuarto))'
form_dia = r'(?P<h>\d\d?):?(?P<m>\d\d)?(( de)(l|( la) )(?P<d>(mañana|mediodía|tarde|noche|madrugada)))'

def normaliza_form_hm(linia):
    """
    Normaliza las horas en formato "hh[hH]mm[mM]" a formato digital (hh:mm).
    
    Args:
        linia (str): La línea de texto que contiene las horas a normalizar.
    
    Returns:
        str: La línea de texto con las horas normalizadas en formato "hh:mm".
    """
    result = []
    while (match := re.search(form_hm, linia)):
        result.append(linia[:match.start()])
        hora = int(match["h"])
        minutos = int(match["m"]) if match["m"] else 0
        if hora < 24 and minutos < 60:
            result.append(f'{hora:02d}:{minutos:02d}')
        else:
            result.append(linia[match.start():match.end()])
        linia = linia[match.end():]
    result.append(linia)
    return ''.join(result)

def normaliza_form_hora(linia):
    """
    Normaliza las horas en formato de palabras (en punto, y media...) a formato digital (hh:mm).
    
    Args:
        linia (str): La línea de texto que contiene las horas a normalizar.
    
    Returns:
        str: La línea de texto con las horas normalizadas en formato "hh:mm".
    """
    result = []
    while (match := re.search(form_hora, linia)):
        result.append(linia[:match.start()])
        hora = int(match["h"])
        if match["c"] == "en punto":
            hora = hora - 12 if hora > 12 else hora
            result.append(f'{hora:02d}')
        elif match["c"] == "y cuarto":
            result.append(f'{hora:02d}:15')
        elif match["c"] == "y media":
            result.append(f'{hora:02d}:30')
        elif match["c"] == "menos cuarto":
            hora -= 1
            result.append(f'{hora:02d}:45')
        else:
            result.append(linia[match.start():match.end()])
        linia = linia[match.end():]
    result.append(linia)
    return ''.join(result)

def normaliza_form_dia(linia):
    """
    Normaliza las horas en formato "hh:mm de [periodo del día]" a formato digital (hh:mm).
    
    Args:
        linia (str): La línea de texto que contiene las horas a normalizar.
    
    Returns:
        str: La línea de texto con las horas normalizadas en formato "hh:mm".
    """
    match = re.search(form_dia, linia)
    if not match:
        return linia
    result = linia[:match.start()]
    hora = int(match["h"])
    minutos = int(match["m"]) if match["m"] else 0
    periodo = match["d"]
    
    if minutos == 0:
        if (periodo == "mediodía" and hora > 12 and hora < 16) or (periodo in ["tarde", "noche"] and hora >= 12):
            hora -= 12
    else:
        if (periodo == "mediodía" and hora < 4) or (periodo in ["tarde", "noche"] and hora < 12):
            hora += 12
    if minutos != 0:
        result += f'{hora:02d}:{minutos:02d}' 
    elif minutos == 0 and hora == 0:
        result += f'00:00'
    else:
        result += f'{hora}'

    if hora < 13 and hora != 0:
        result += linia[match.end("h"):]
    else:
        result += linia[match.end()]
    return result


def normalizaHoras(ficText, ficNorm):
    """
    Nombre: Ona Bonastre Martí
    Clase utilizada para normalizar las expresiones horarias de un archivo de texto

    Args:
        ficText (str): ruta del archivo de entrada que contiene el texto a normalizar.
        ficNorm (str): ruta del archivo de salida donde se escribirá el texto normalizado.
    
    """
    with open(ficText) as fpIn, open(ficNorm, "wt") as fpOut:
        for linia in fpIn:
            linia_aux = normaliza_form_hm(linia)
            linia_aux = normaliza_form_hora(linia_aux)
            linia_aux = normaliza_form_dia(linia_aux)
            fpOut.write(linia_aux)

salida = "APA-T6\\ficheros\salida.txt"
a = normalizaHoras("APA-T6\\ficheros\horas.txt", salida)

