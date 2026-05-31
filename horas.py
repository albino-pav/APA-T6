"""
Módulo para la normalización de expresiones horarias en documentos de texto.
Autor: Fulano Mengano Zutano
Descripción: Detecta patrones de horas en castellano (estándar, verbales, con períodos)
             y las unifica al formato estándar de 24 horas (HH:MM).
"""

import re

def normalizaHoras(ficText, ficNorm):
    """
    Lee el fichero ficText, busca expresiones horarias, las normaliza al formato
    HH:MM y escribe el resultado en el fichero ficNorm.
    """
    
    # Expresión regular estructurada para capturar las diferentes variantes horarias:
    # Grupo 1: Dígito(s) de la hora
    # Grupo 2: Minutos en formato estándar (:MM)
    # Grupo 3: Minutos en formato compacto (MMm)
    # Grupo 4: Frase de minutos verbales (en punto, y cuarto, etc.)
    # Grupo 5: Período del día (de la mañana, de la tarde, etc.)
    patron_hora = re.compile(
        r'\b(\d{1,2})(?:'
        r':(\d{1,2})|'
        r'h(?:(\d{1,2})m)?|'
        r'\s+(en punto|y cuarto|y media|menos cuarto)'
        r')?'
        r'(?:\s+(de la mañana|del mediodía|de la tarde|de la noche|de la madrugada))?\b',
        re.IGNORECASE
    )

    def cambiar_formato(match):
        cadena_completa = match.group(0)
        h_str = match.group(1)
        m_dos_puntos = match.group(2)
        m_formato_h = match.group(3)
        m_verbal = match.group(4)
        periodo = match.group(5)

        tiene_letra_h = 'h' in cadena_completa or 'H' in cadena_completa

        # Filtrado preventivo: si es un número aislado sin contexto horario, se descarta
        if (m_dos_puntos is None and m_formato_h is None and m_verbal is None 
                and periodo is None and not tiene_letra_h):
            return cadena_completa

        try:
            hora_origen = int(h_str)
        except ValueError:
            return cadena_completa

        # --- 1. FORMATO ESTÁNDAR (Ej: 18:30 o 17:5) ---
        if m_dos_puntos is not None:
            # No se permiten mezclas con texto de períodos o formatos de letra 'h'
            if periodo is not None or m_verbal is not None or m_formato_h is not None or tiene_letra_h:
                return cadena_completa
            # Los minutos del formato estándar obligatoriamente deben tener 2 dígitos (Requisito "17:5" incorrecto)
            if len(m_dos_puntos) != 2:
                return cadena_completa
            minutos = int(m_dos_puntos)
            if 0 <= hora_origen <= 23 and 0 <= minutos <= 59:
                return f"{hora_origen:02d}:{minutos:02d}"
            return cadena_completa

        # --- 2. FORMATO CON LETRA 'H' SIN PERÍODO (Ej: 17h5m, 18h, 32h31m) ---
        if tiene_letra_h and periodo is None and m_verbal is None:
            minutos = int(m_formato_h) if m_formato_h is not None else 0
            if 0 <= hora_origen <= 23 and 0 <= minutos <= 59:
                return f"{hora_origen:02d}:{minutos:02d}"
            return cadena_completa

        # --- 3. CONTEXTOS DE RELOJ DE 12 HORAS (Formatos verbales o con Período) ---
        # En estos casos, la hora obligatoriamente debe estar comprendida entre 1 y 12
        if not (1 <= hora_origen <= 12):
            return cadena_completa

        # Validar consistencia estricta del período del día según las reglas fijadas
        if periodo is not None:
            p = periodo.lower()
            if p == "de la mañana" and not (4 <= hora_origen <= 12):
                return cadena_completa
            elif p == "del mediodía" and not (hora_origen == 12 or 1 <= hora_origen <= 3):
                return cadena_completa
            elif p == "de la tarde" and not (3 <= hora_origen <= 8):
                return cadena_completa
            elif p == "de la noche" and not (8 <= hora_origen <= 12 or 1 <= hora_origen <= 4):
                return cadena_completa
            elif p == "de la madrugada" and not (1 <= hora_origen <= 6):
                return cadena_completa

        # Asignar minutos base y desfase de horas para "menos cuarto"
        minutos = 0
        desfase_hora = 0

        if m_formato_h is not None:
            minutos = int(m_formato_h)
        elif m_verbal is not None:
            v = m_verbal.lower()
            if v == "en punto":
                minutos = 0
            elif v == "y cuarto":
                minutos = 15
            elif v == "y media":
                minutos = 30
            elif v == "menos cuarto":
                minutos = 45
                desfase_hora = -1

        if not (0 <= minutos <= 59):
            return cadena_completa

        # Calcular la base de 24 horas usando la hora original
        if periodo is not None:
            p = periodo.lower()
            if p == "de la mañana":
                base_24h = 12 if hora_origen == 12 else hora_origen
            elif p == "del mediodía":
                base_24h = 12 if hora_origen == 12 else hora_origen + 12
            elif p == "de la tarde":
                base_24h = hora_origen + 12
            elif p == "de la noche":
                base_24h = 0 if hora_origen == 12 else (hora_origen + 12 if hora_origen >= 8 else hora_origen)
            elif p == "de la madrugada":
                base_24h = hora_origen
        else:
            # Sin período explícito se asume el rango de 00:00 a 11:59
            base_24h = 0 if hora_origen == 12 else hora_origen

        # Aplicamos la modificación de hora (por ejemplo, retrasar una hora si es 'menos cuarto')
        hora_final = base_24h + desfase_hora
        if hora_final < 0:
            hora_final = 23
        elif hora_final >= 24:
            hora_final = 0

        return f"{hora_final:02d}:{minutos:02d}"

    # Lectura, procesamiento y escritura de ficheros
    with open(ficText, 'r', encoding='utf-8') as f_entrada, open(ficNorm, 'w', encoding='utf-8') as f_salida:
        for linea in f_entrada:
            linea_procesada = patron_hora.sub(cambiar_formato, linea)
            f_salida.write(linea_procesada)


if __name__ == '__main__':
    # Código de prueba local para verificar la función con tu archivo
    normalizaHoras('horas.txt', 'horas_normalizadas.txt')
    print("Fichero de horas procesado de manera exitosa en 'horas_normalizadas.txt'.")