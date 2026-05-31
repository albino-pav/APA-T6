"""
Tarea APA-T6: Expresiones regulares.

Autor: Hug Feijoo Giralt

Este fichero contiene la función 'normalizaHoras()', que lee un fichero de
texto, busca en él expresiones horarias en los formatos habituales del
castellano y escribe un fichero nuevo en el que dichas expresiones se han
normalizado al formato HH:MM. Las expresiones incorrectas se dejan tal cual.
El análisis se realiza únicamente mediante expresiones regulares.
"""

import re

# Partículas relativas y partes del día.
_RELS = r'en\s+punto|y\s+cuarto|y\s+media|menos\s+cuarto'
_PERS = (
    r'de\s+la\s+mañana|de\s+la\s+tarde|de\s+la\s+noche|'
    r'de\s+la\s+madrugada|del\s+mediodía'
)

# Expresión regular que reconoce todos los formatos horarios contemplados.
_HORA = re.compile(
    r'\b(?:'
    r'(?P<est_h>\d{1,2}):(?P<est_m>\d{1,2})'              # 8:27
    r'|(?P<hm_h>\d{1,2})h(?:(?P<hm_m>\d{1,2})m)?'         # 8h / 8h27m
    r'(?:\s+(?P<hm_per>' + _PERS + r'))?'                # ... de la mañana
    r'|(?P<rel_h>\d{1,2})\s+(?P<rel>' + _RELS + r')'     # 8 en punto
    r'(?:\s+(?P<rel_per>' + _PERS + r'))?'               # ... de la tarde
    r'|(?P<per_h>\d{1,2})\s+(?P<per>' + _PERS + r')'     # 12 de la noche
    r')'
)


def _horaPeriodo(hora, periodo):
    """
    Convierte una hora hablada (reloj de 12) al formato de 24 horas según la
    parte del día indicada. Devuelve 'None' si la hora no es válida para esa
    parte del día.
    """
    periodo = re.sub(r'\s+', ' ', periodo)
    if periodo == 'de la madrugada':
        return hora if 1 <= hora <= 6 else None
    if periodo == 'de la mañana':
        return hora if 4 <= hora <= 12 else None
    if periodo == 'del mediodía':
        if hora == 12:
            return 12
        return hora + 12 if 1 <= hora <= 3 else None
    if periodo == 'de la tarde':
        return hora + 12 if 3 <= hora <= 8 else None
    if periodo == 'de la noche':
        if 8 <= hora <= 11:
            return hora + 12
        if hora == 12:
            return 0
        return hora if 1 <= hora <= 4 else None
    return None


def _normaliza(encaje):
    """
    Recibe un objeto 'match' y devuelve la expresión horaria normalizada al
    formato HH:MM o, si la expresión es incorrecta, el texto original.
    """
    txt = encaje.group(0)
    g = encaje.groupdict()
    periodo = g['hm_per'] or g['rel_per'] or g['per']
    rel = g['rel']

    # Determinación de la hora hablada, los minutos y el tipo de reloj.
    if g['est_h'] is not None:                  # Formato estándar H:MM
        hora, minStr = int(g['est_h']), g['est_m']
        if len(minStr) != 2:                    # los minutos exigen 2 cifras
            return txt
        minuto, doce = int(minStr), False
    elif g['hm_h'] is not None:                 # Formato Hh / HhMm
        hora = int(g['hm_h'])
        minuto = int(g['hm_m']) if g['hm_m'] is not None else 0
        doce = False
    elif g['rel_h'] is not None:                # Formato relativo
        hora, minuto, doce = int(g['rel_h']), 0, True
    else:                                       # Número escueto + periodo
        hora, minuto, doce = int(g['per_h']), 0, True

    # Desplazamiento de horas/minutos según la partícula relativa.
    despHora = 0
    if rel == 'en punto':
        minuto = 0
    elif rel == 'y cuarto':
        minuto = 15
    elif rel == 'y media':
        minuto = 30
    elif rel == 'menos cuarto':
        minuto, despHora = 45, -1

    if not 0 <= minuto <= 59:
        return txt

    if periodo is not None:                     # Reloj de 12 con parte del día
        base = _horaPeriodo(hora, periodo)
        if base is None:
            return txt
        hora = (base + despHora) % 24
    elif doce:                                  # Reloj de 12 sin parte del día
        if not 1 <= hora <= 12:
            return txt
        hora = (hora + despHora) % 12
    elif not 0 <= hora <= 23:                   # Reloj de 24 (estándar / Hh)
        return txt

    return f'{hora:02d}:{minuto:02d}'


def normalizaHoras(ficText, ficNorm):
    """
    Lee el fichero de texto 'ficText', normaliza todas las expresiones
    horarias que encuentra al formato HH:MM y escribe el resultado en el
    fichero 'ficNorm'. Las expresiones horarias incorrectas se mantienen sin
    cambios.
    """
    with open(ficText, encoding='utf-8') as fpText, \
            open(ficNorm, 'w', encoding='utf-8') as fpNorm:
        for linea in fpText:
            fpNorm.write(_HORA.sub(_normaliza, linea))
