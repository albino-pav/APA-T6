import re

def procesar_coincidencia(match):
    """
    Función auxiliar que decide si una coincidencia de la expresión regular
    es una hora válida y, si lo es, la transforma al formato HH:MM.
    """
    texto_original = match.group(0)
    
    # Obtenemos la hora dependiendo de en qué parte de la regex encajó
    h_str = match.group('h1') or match.group('h2') or match.group('h3')
    if not h_str: 
        return texto_original
    
    hora = int(h_str)
    minutos = 0
    
    # 1. Si tiene formato con minutos en dígitos (ej. 18:30 o 8h27m)
    if match.group('minutos'):
        minutos = int(match.group('minutos'))
        # Filtramos barbaridades de tiempo
        if minutos > 59 or hora > 23: 
            return texto_original

    # 2. Si tiene formato de texto (ej. en punto, y media)
    elif match.group('texto_min'):
        texto_min = match.group('texto_min').lower()
        if 'y cuarto' in texto_min: minutos = 15
        elif 'y media' in texto_min: minutos = 30
        elif 'menos cuarto' in texto_min:
            minutos = 45
            hora -= 1 
        elif 'en punto' in texto_min: minutos = 0
        
        # En lenguaje hablado sin formato militar, la hora base debe ser de 1 a 12
        hora_original = int(h_str)
        if not (1 <= hora_original <= 12): 
            return texto_original
        
        # Ajuste por si restamos horas (ej. 1 menos cuarto -> 00:45)
        if hora == 0: hora = 12 
        elif hora == -1: hora = 11

    modificador = match.group('mod')
    
    # 3. Validamos si hay modificador (de la mañana, tarde, etc.)
    if modificador:
        modificador = modificador.lower()
        hora_original = int(h_str) 
        
        # Con modificador, el reloj siempre es de 1 a 12
        if not (1 <= hora_original <= 12):
            return texto_original
            
        if 'mañana' in modificador: 
            if not (4 <= hora_original <= 12): return texto_original
            if hora == 12: hora = 0
        elif 'mediodía' in modificador:
            if not (1 <= hora_original <= 3 or hora_original == 12): return texto_original
            if hora != 12: hora += 12
        elif 'tarde' in modificador: 
            if not (3 <= hora_original <= 8): return texto_original
            if hora != 12: hora += 12
        elif 'noche' in modificador: 
            if not (8 <= hora_original <= 12 or 1 <= hora_original <= 4): return texto_original
            if hora == 12: hora = 0
            elif hora < 12: hora += 12
        elif 'madrugada' in modificador: 
            if not (1 <= hora_original <= 6): return texto_original
    else:
        # Si es formato hablado SIN modificador (ej. "8 en punto")
        # El enunciado dice que se devuelve en rango 00:00 a 11:59
        if match.group('texto_min'):
            if hora == 12: hora = 0
    
    return f"{hora:02d}:{minutos:02d}"

def normalizaHoras(ficText, ficNorm):
    """
    Autor: Pedro
    Lee ficText, busca expresiones horarias mediante regex y las normaliza a 
    formato estándar HH:MM en el archivo ficNorm.
    """
    # Regex para capturar horas (con/sin dígitos, con/sin texto, con/sin modificadores)
    patron = re.compile(
        r'\b(?:'
        r'(?P<h1>\d{1,2})(?P<sep>[:h])(?P<minutos>\d{2})m?\b|' 
        r'(?P<h2>\d{1,2})h\b|'
        r'(?P<h3>\d{1,2})\s+(?P<texto_min>en punto|y cuarto|y media|menos cuarto)\b'
        r')'
        r'(?:\s+(?P<mod>de la mañana|del mediodía|de la tarde|de la noche|de la madrugada))?',
        re.IGNORECASE
    )

    with open(ficText, 'r', encoding='utf-8') as f_in, \
         open(ficNorm, 'w', encoding='utf-8') as f_out:
        for linea in f_in:
            # sub() busca todos los patrones y los pasa por nuestra función procesar_coincidencia
            linea_mod = patron.sub(procesar_coincidencia, linea)
            f_out.write(linea_mod)

# Bloque de prueba
if __name__ == "__main__":
    # Lee el horas.txt que ya subiste y genera uno nuevo con los resultados
    normalizaHoras('horas.txt', 'horas_normalizadas.txt')
    print("¡Archivo normalizado generado con éxito!")