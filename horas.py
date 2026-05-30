# ==================== horas.py ====================
import re

def normalizaHoras(ficText, ficNorm):
    """
    Lee un texto, busca expresiones horarias y las normaliza a HH:MM.
    Las incorrectas se dejan como están.
    """
    with open(ficText, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    
    resultado = []
    for linea in lineas:
        linea_original = linea.rstrip('\n')
        linea_nueva = linea_original

        def cambia_hhmm(m):
            h = int(m.group(1))
            m2 = int(m.group(2))
            if 0 <= h <= 23 and 0 <= m2 <= 59:
                return f"{h:02d}:{m2:02d}"
            else:
                return m.group(0)
        linea_nueva = re.sub(r'(\d{1,2}):(\d{1,2})', cambia_hhmm, linea_nueva)

        def cambia_hhmm_sin_puntos(m):
            h = int(m.group(1))
            if m.group(2):
                mins = int(m.group(2))
            else:
                mins = 0
            if 0 <= h <= 23 and 0 <= mins <= 59:
                return f"{h:02d}:{mins:02d}"
            else:
                return m.group(0)
        linea_nueva = re.sub(r'(\d{1,2})h\s*(?:(\d{1,2})m?)?', cambia_hhmm_sin_puntos, linea_nueva)

        def cambia_cuarto(m):
            h = int(m.group(1))
            tipo = m.group(2)
            if not (1 <= h <= 12):
                return m.group(0)
            if tipo == 'cuarto':
                return f"{h:02d}:15"
            elif tipo == 'media':
                return f"{h:02d}:30"
            elif tipo == 'menos cuarto':
                h2 = h - 1 if h > 1 else 12
                return f"{h2:02d}:45"
            else:
                return m.group(0)
        linea_nueva = re.sub(r'(\d{1,2})\s+y\s+(cuarto|media|menos cuarto)', cambia_cuarto, linea_nueva)

        def cambia_en_punto(m):
            h = int(m.group(1))
            if 1 <= h <= 12:
                return f"{h:02d}:00"
            else:
                return m.group(0)
        linea_nueva = re.sub(r'(\d{1,2})\s+en\s+punto', cambia_en_punto, linea_nueva)

        def cambia_periodo(m):
            h = int(m.group(1))
            p = m.group(2)
            if not (1 <= h <= 12):
                return m.group(0)
            if p == 'mediodia':
                if h == 12:
                    return "12:00"
                else:
                    return m.group(0)
            elif p == 'mañana':
                if h == 12:
                    return m.group(0)
                return f"{h:02d}:00"
            elif p == 'tarde':
                if h == 12:
                    return m.group(0)
                if 1 <= h <= 7:
                    return f"{h+12:02d}:00"
                else:
                    return m.group(0)
            elif p == 'noche':
                if h == 12:
                    return "00:00"
                elif 8 <= h <= 11:
                    return f"{h+12:02d}:00"
                else:
                    return m.group(0)
            elif p == 'madrugada':
                if 1 <= h <= 5:
                    return f"{h:02d}:00"
                else:
                    return m.group(0)
            else:
                return m.group(0)
        linea_nueva = re.sub(r'(\d{1,2})\s+de\s+la\s+(mañana|tarde|noche|madrugada|mediodia)', cambia_periodo, linea_nueva)

        resultado.append(linea_nueva)

    with open(ficNorm, 'w', encoding='utf-8') as f:
        f.write('\n'.join(resultado))


if __name__ == "__main__":
    normalizaHoras('horas.txt', 'horas_normalizado.txt')
    print("ok")
