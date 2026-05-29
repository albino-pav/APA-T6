"""
Fichero: horas.py
Descripción: Filtro de normalización de expresiones horarias en castellano
             mediante expresiones regulares.
"""

import re

def _obtener_desplazamiento_periodo(hh_orig, hh_adj, periodo):
    """
    Valida la hora según el periodo lingüístico y devuelve el valor en formato 24h.
    Si la combinación es incorrecta, devuelve None.
    """
    if periodo == 'de la mañana':
        if not (4 <= hh_orig <= 12): 
            return None
        return hh_adj
        
    elif periodo == 'del mediodía':
        if hh_orig not in [12, 1, 2, 3]: 
            return None
        return hh_adj if hh_adj == 12 else hh_adj + 12
        
    elif periodo == 'de la tarde':
        if not (3 <= hh_orig <= 8): 
            return None
        return hh_adj + 12
        
    elif periodo == 'de la noche':
        if hh_orig not in [8, 9, 10, 11, 12, 1, 2, 3, 4]: 
            return None
        if 8 <= hh_adj <= 11: 
            return hh_adj + 12
        if hh_adj == 12: 
            return 0
        if 1 <= hh_adj <= 4: 
            return hh_adj
            
    elif periodo == 'de la madrugada':
        if not (1 <= hh_orig <= 6): 
            return None
        return hh_adj
        
    return None


def normalizaHoras(ficText, ficNorm):
    """
    Lee ficText, busca expresiones horarias válidas, las convierte
    al formato HH:MM de 24 horas y escribe el resultado en ficNorm.
    """
    
    # -------------------------------------------------------------------------
    # PATRÓN 1: Formato estándar con dos puntos 
    # -------------------------------------------------------------------------
    pat_colon = r'\b(\d{1,2}):(\d{2})(?:\s+(de la mañana|del mediodía|de la tarde|de la noche|de la madrugada))?\b'
    
    def repl_colon(m):
        hh = int(m.group(1))
        mm = int(m.group(2))
        periodo = m.group(3)
        
        if hh >= 24 or mm >= 60:
            return m.group(0)  # Incorrecto, no se toca
            
        if periodo:
            if not (1 <= hh <= 12): 
                return m.group(0)
            hh_24 = _obtener_desplazamiento_periodo(hh, hh, periodo)
            if hh_24 == None: 
                return m.group(0)
            return f"{hh_24:02d}:{mm:02d}"
        else:
            return f"{hh:02d}:{mm:02d}"

    # -------------------------------------------------------------------------
    # PATRÓN 2: Formato compacto con letras 'h' y 'm'
    # -------------------------------------------------------------------------
    pat_hm = r'\b(\d{1,2})h(?:(\d{1,2})m)?(?:\s+(de la mañana|del mediodía|de la tarde|de la noche|de la madrugada))?\b'
    
    def repl_hm(m):
        hh = int(m.group(1))
        mm = int(m.group(2)) if m.group(2) else 0
        periodo = m.group(3)
        
        if mm >= 60:
            return m.group(0)
            
        if periodo:
            if not (1 <= hh <= 12): 
                return m.group(0)
            hh_24 = _obtener_desplazamiento_periodo(hh, hh, periodo)
            if hh_24 == None: 
                return m.group(0)
            return f"{hh_24:02d}:{mm:02d}"
        else:
            if hh >= 24: 
                return m.group(0)
            return f"{hh:02d}:{mm:02d}"

    # -------------------------------------------------------------------------
    # PATRÓN 3: Expresiones verbales completas 
    # -------------------------------------------------------------------------
    pat_palabras = (
        r'\b(\d{1,2})(?:\s+(en punto|y cuarto|y media|menos cuarto))?\s+(de la mañana|del mediodía|de la tarde|de la noche|de la madrugada)\b|'
        r'\b(\d{1,2})\s+(en punto|y cuarto|y media|menos cuarto)\b'
    )
    
    def repl_palabras(m):
        if m.group(1) is not None:
            hh_orig = int(m.group(1))
            modificador = m.group(2)
            periodo = m.group(3)
        else:
            hh_orig = int(m.group(4))
            modificador = m.group(5)
            periodo = None
            
        if not (1 <= hh_orig <= 12):
            return m.group(0)
            
        # Calcular los minutos correspondientes y la hora ajustada si resta
        if modificador == 'en punto' or modificador is None:
            mm = 0
            hh_adj = hh_orig
        elif modificador == 'y cuarto':
            mm = 15
            hh_adj = hh_orig
        elif modificador == 'y media':
            mm = 30
            hh_adj = hh_orig
        elif modificador == 'menos cuarto':
            mm = 45
            hh_adj = 12 if hh_orig == 1 else hh_orig - 1
            
        if periodo:
            hh_24 = _obtener_desplazamiento_periodo(hh_orig, hh_adj, periodo)
            if hh_24 == None: 
                return m.group(0)
            return f"{hh_24:02d}:{mm:02d}"
        else:
            # Al no tener contexto AM/PM se asume el rango 00:00 a 11:59 obligatoriamente
            hh_24 = hh_adj % 12
            return f"{hh_24:02d}:{mm:02d}"

    # Procesado del fichero línea a línea
    with open(ficText, 'r', encoding='utf-8') as f_in, open(ficNorm, 'w', encoding='utf-8') as f_out:
        for linea in f_in:
            linea_mod = re.sub(pat_colon, repl_colon, linea)
            linea_mod = re.sub(pat_hm, repl_hm, linea_mod)
            linea_mod = re.sub(pat_palabras, repl_palabras, linea_mod)
            f_out.write(linea_mod)
