"""
horas.py - Normalización de expresiones horarias en castellano.
Autor: Sandra Cots Agüera
"""

import re

_PER = r'la mañana|la tarde|la noche|la madrugada|el mediodía|mediodía'

_PATRON = re.compile(
    r'\d{1,2}h(?:\d{1,2}m)?(?:\s+de\s+(?:' + _PER + r'))?'
    r'|\d{1,2}:\d{2}'
    r'|\d{1,2}\s+(?:en punto|y cuarto|y media|menos cuarto)\s+de\s+(?:' + _PER + r')'
    r'|\d{1,2}\s+de\s+(?:' + _PER + r')'
    r'|\d{1,2}\s+(?:en punto|y cuarto|y media|menos cuarto)'
)


def _periodo_a_h24(h, periodo):
    """Convierte hora 1-12 + periodo a hora 0-23, o None si inválido."""
    rangos = {
        'la mañana':    (4, 12),
        'el mediodía':  (12, 3),
        'mediodía':     (12, 3),
        'la tarde':     (3, 8),
        'la noche':     (8, 12),
        'la madrugada': (1, 6),
    }
    ini, fin = rangos[periodo]

    def en_rango(x, i, f):
        return (i <= x <= f) if i <= f else (x >= i or x <= f)

    if not en_rango(h, ini, fin):
        return None

    if periodo == 'la mañana':
        return 0 if h == 12 else h
    if periodo in ('el mediodía', 'mediodía'):
        return 12 if h == 12 else h + 12
    if periodo == 'la tarde':
        return h + 12
    if periodo == 'la noche':
        return 0 if h == 12 else h + 12
    if periodo == 'la madrugada':
        return 0 if h == 12 else h
    return None


def _mod_a_mn(mod):
    return {'en punto': 0, 'y cuarto': 15, 'y media': 30, 'menos cuarto': -15}[mod]


def _normaliza(match):
    texto = match.group(0)

    # HH:MM
    m = re.fullmatch(r'(\d{1,2}):(\d{2})', texto)
    if m:
        h, mn = int(m.group(1)), int(m.group(2))
        if 0 <= h <= 23 and 0 <= mn <= 59:
            return f'{h:02d}:{mn:02d}'
        return texto

    # Hh[MMm] [de periodo]
    m = re.fullmatch(r'(\d{1,2})h(?:(\d{1,2})m)?(?:\s+de\s+(' + _PER + r'))?', texto)
    if m:
        h = int(m.group(1))
        mn = int(m.group(2)) if m.group(2) else 0
        periodo = m.group(3)
        if periodo:
            if not (1 <= h <= 12 and 0 <= mn <= 59):
                return texto
            h24 = _periodo_a_h24(h, periodo)
            return f'{h24:02d}:{mn:02d}' if h24 is not None else texto
        if 0 <= h <= 23 and 0 <= mn <= 59:
            return f'{h:02d}:{mn:02d}'
        return texto

    # H mod de periodo
    m = re.fullmatch(
        r'(\d{1,2})\s+(en punto|y cuarto|y media|menos cuarto)\s+de\s+(' + _PER + r')',
        texto)
    if m:
        h, mod, periodo = int(m.group(1)), m.group(2), m.group(3)
        if not (1 <= h <= 12):
            return texto
        mn = _mod_a_mn(mod)
        if mn < 0:
            h, mn = (h - 1) or 12, mn + 60
        h24 = _periodo_a_h24(h, periodo)
        return f'{h24:02d}:{mn:02d}' if h24 is not None else texto

    # H de periodo
    m = re.fullmatch(r'(\d{1,2})\s+de\s+(' + _PER + r')', texto)
    if m:
        h, periodo = int(m.group(1)), m.group(2)
        if not (1 <= h <= 12):
            return texto
        h24 = _periodo_a_h24(h, periodo)
        return f'{h24:02d}:00' if h24 is not None else texto

    # H mod (reloj 12h, ambiguo)
    m = re.fullmatch(r'(\d{1,2})\s+(en punto|y cuarto|y media|menos cuarto)', texto)
    if m:
        h, mod = int(m.group(1)), m.group(2)
        if not (1 <= h <= 12):
            return texto
        mn = _mod_a_mn(mod)
        if mn < 0:
            h, mn = (h - 1) or 12, mn + 60
        return f'{h % 12:02d}:{mn:02d}'

    return texto


def normalizaHoras(ficText, ficNorm):
    """
    Lee ficText, sustituye las expresiones horarias válidas por su forma
    normalizada HH:MM y escribe el resultado en ficNorm.
    """
    with open(ficText, encoding='utf-8') as fin, \
         open(ficNorm, 'w', encoding='utf-8') as fout:
        for linea in fin:
            fout.write(_PATRON.sub(_normaliza, linea))


if __name__ == '__main__':
    normalizaHoras('horas.txt', 'horas_norm.txt')
    with open('horas_norm.txt', encoding='utf-8') as f:
        print(f.read())
