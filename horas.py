"""
Autor: Oriol López Miret
El programa implementa un sistema completo de normalización de expresiones horarias en castellano, capaz de reconocer múltiples formatos habituales en el lenguaje escrito y hablado, y convertirlos al formato estándar HH:MM, con dos dígitos para la hora y dos para los minutos.
"""

import re

def convierte_franja(h, m, franja):
    h = int(h)
    m = int(m)

    # Validación de minutos
    if not (0 <= m <= 59):
        return None

    # Reglas del enunciado
    if franja == "mañana":       # 4–12
        if not (4 <= h <= 12): return None
        return f"{h%12:02d}:{m:02d}"

    if franja == "mediodía":    # 12–15
        if not (12 <= h <= 3+12): return None
        return f"{h:02d}:{m:02d}"

    if franja == "tarde":       # 15–20
        if not (3 <= h <= 8): return None
        return f"{(h+12)%24:02d}:{m:02d}"

    if franja == "noche":       # 20–4
        if 1 <= h <= 4:
            return f"{h:02d}:{m:02d}"
        if 8 <= h <= 12:
            return f"{(h+12)%24:02d}:{m:02d}"
        return None

    if franja == "madrugada":   # 1–6
        if not (1 <= h <= 6): return None
        return f"{h:02d}:{m:02d}"

    return None

def normaliza_franjas(texto):
    patron = re.compile(
        r"\b(1[0-2]|[1-9])"                  # hora
        r"(?:h([0-5]?\d)m?)?"                # minutos opcionales
        r"\s+de la (mañana|tarde|noche|madrugada|mediodía)\b",
        re.IGNORECASE
    )

    def repl(m):
        h = m.group(1)
        mm = m.group(2) or "0"
        franja = m.group(3).lower()
        res = convierte_franja(h, mm, franja)
        return res if res else m.group(0)

    return patron.sub(repl, texto)

def normaliza_hablado(texto):
    patron = re.compile(
        r"\b(1[0-2]|[1-9])\s+"
        r"(en punto|y cuarto|y media|menos cuarto)\b",
        re.IGNORECASE
    )

    def repl(m):
        h = int(m.group(1))
        exp = m.group(2).lower()

        if exp == "en punto":
            return f"{h%12:02d}:00"
        if exp == "y cuarto":
            return f"{h%12:02d}:15"
        if exp == "y media":
            return f"{h%12:02d}:30"
        if exp == "menos cuarto":
            h = (h - 1) % 12
            if h == 0: h = 12
            return f"{h:02d}:45"

        return m.group(0)

    return patron.sub(repl, texto)

def normaliza_hm(texto):
    patron = re.compile(
        r"\b([01]?\d|2[0-3])h(?:([0-5]?\d)m)?\b"
    )

    def repl(m):
        h = int(m.group(1))
        mm = m.group(2)
        if mm is None:
            mm = 0
        else:
            mm = int(mm)
        if not (0 <= mm <= 59):
            return m.group(0)
        return f"{h:02d}:{mm:02d}"

    return patron.sub(repl, texto)

def normaliza_estandar(texto):
    patron = re.compile(
        r"\b([01]?\d|2[0-3]):([0-5]\d)\b"
    )

    def repl(m):
        h = int(m.group(1))
        mm = int(m.group(2))
        return f"{h:02d}:{mm:02d}"

    return patron.sub(repl, texto)

def normalizaHoras(ficText, ficNorm):
    with open(ficText, encoding="utf-8") as f_in, \
         open(ficNorm, "w", encoding="utf-8") as f_out:

        for linea in f_in:
            nueva = linea

            # Orden correcto: de más complejas a más simples
            nueva = normaliza_franjas(nueva)
            nueva = normaliza_hablado(nueva)
            nueva = normaliza_hm(nueva)
            nueva = normaliza_estandar(nueva)

            f_out.write(nueva)
