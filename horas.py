# P6- VICTORIA BLANCO I MAIDER DURÓ
# import re
# rehh = r'(?P<hh>\d{1,2})'
# remm = r'(?P<mm>\d{1,2})'
# rehhmm = rf'{rehh}[hH]({remm}[mM])?'

# def normalizaHoras(ficText,ficNorm):
#     with open(ficText,'rt') as fpText, open(ficNorm,'wt') as fpNorm:
#         for linea in fpText:
#             while(match := re.search(rehhmm, linea)):
#                 fpNorm.write(linea[:match.start()])
#                 linea = linea[match.end():]
#                 hora = int(match['hh'])
#                 minuto = int(match['mm']) if match['mm'] else 0
#                 fpNorm.write(f'{hora:02d}:{minuto:02d}')
#             fpNorm.write(linea)

import re

# Patrones para diferentes formatos de horas
rehhmm_24h = re.compile(r'(?P<hh>\d{1,2}):(?P<mm>\d{1,2})')
rehh = re.compile(r'(?P<hh>\d{1,2})[hH]')
rehhmm = re.compile(r'(?P<hh>\d{1,2})[hH](?P<mm>\d{1,2})[mM]')
re_fracciones = re.compile(r'(?P<hh>\d{1,2}) (menos cuarto|y media)')
re_periodos = re.compile(r'(?P<hh>\d{1,2}) de la (mañana|tarde|noche)')
re_punto = re.compile(r'(?P<hh>\d{1,2}) en punto')

# Diccionario para convertir periodos a formato 24h
periodos = {
    'mañana': lambda h: h if h < 12 else h - 12,
    'tarde': lambda h: h + 12 if h < 12 else h,
    'noche': lambda h: (h + 12) % 24 if h < 12 else h,
}

def normalizaHoras(ficText, ficNorm):
    with open(ficText, 'rt') as fpText, open(ficNorm, 'wt') as fpNorm:
        for linea in fpText:
            # Procesar expresiones horarias con formato hhH y hhHmm
            linea = normaliza_horas(linea, rehhmm, rehh, re_fracciones, re_periodos, re_punto)
            # Procesar expresiones horarias 24h
            linea = normaliza_horas_24h(linea, rehhmm_24h)
            fpNorm.write(linea)

def normaliza_horas(linea, rehhmm, rehh, re_fracciones, re_periodos, re_punto):
    # Normalizar hhHmm (con minutos mayores que 60)
    linea = rehhmm.sub(lambda m: normaliza_hhmm(m.group("hh"), m.group("mm")), linea)
    # Normalizar hhH
    linea = rehh.sub(lambda m: f'{int(m.group("hh")):02d}:00', linea)
    # Normalizar "menos cuarto" y "y media"
    linea = re_fracciones.sub(lambda m: fracciones_to_hhmm(m.group("hh"), m.group(2)), linea)
    # Normalizar periodos (mañana, tarde, noche)
    linea = re_periodos.sub(lambda m: f'{periodos[m.group(2)](int(m.group("hh"))):02d}:00', linea)
    # Normalizar "en punto"
    linea = re_punto.sub(lambda m: f'{int(m.group("hh")):02d}:00', linea)
    return linea

def normaliza_horas_24h(linea, rehhmm_24h):
    # Normalizar hh:mm
    linea = rehhmm_24h.sub(lambda m: f'{int(m.group("hh")):02d}:{int(m.group("mm")):02d}', linea)
    return linea

def normaliza_hhmm(hora, minuto):
    hora = int(hora)
    minuto = int(minuto)
    # Manejar minutos mayores que 60
    if minuto >= 60:
        hora += minuto // 60
        minuto = minuto % 60
    return f'{hora:02d}:{minuto:02d}'

def fracciones_to_hhmm(hora, tipo):
    hora = int(hora)
    if tipo == 'menos cuarto':
        hora -= 1
        minuto = 45
    elif tipo == 'y media':
        minuto = 30
    else:
        minuto = 0
    return f'{hora:02d}:{minuto:02d}'

# Ejemplo de uso:
normalizaHoras('horas.txt', 'horas_normalizadas.txt')
