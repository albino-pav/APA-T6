"""
Alicia Varón López

Módulo para normalizar expresiones horarias

Incluye la función normalizaHoras(), que lee un fichero de texto, detecta
expresiones horarias válidas mediante expresiones regulares y escribe otro
fichero con las horas normalizadas en formato HH:MM.
"""

import re


def _normaliza_hora(hora, minuto=0, periodo=None):
    """
    Devuelve una hora normalizada en formato HH:MM o None si no es válida.
    """
    hora = int(hora)
    minuto = int(minuto)

    if minuto < 0 or minuto > 59:
        return None

    if periodo:
        periodo = periodo.lower()

        if hora < 1 or hora > 12:
            return None

        if periodo == "mañana":
            if not 4 <= hora <= 12:
                return None

        elif periodo == "tarde":
            if 3 <= hora <= 8:
                hora += 12
            else:
                return None

        elif periodo == "noche":
            if hora == 12:
                hora = 0
            elif 8 <= hora <= 11:
                hora += 12
            elif not 1 <= hora <= 4:
                return None

        elif periodo == "madrugada":
            if not 1 <= hora <= 6:
                return None

    elif hora < 0 or hora > 23:
        return None

    return f"{hora:02d}:{minuto:02d}"


def _reemplaza(coincidencia):
    """
    Normaliza cada expresión horaria encontrada.
    """
    grupos = coincidencia.groupdict()

    if grupos["hora_dos_puntos"]:
        return _normaliza_hora(
            grupos["hora_dos_puntos"],
            grupos["min_dos_puntos"],
        )

    if grupos["hora_h"]:
        return _normaliza_hora(
            grupos["hora_h"],
            grupos["min_h"] or 0,
            grupos["periodo_h"],
        )

    if grupos["hora_media"]:
        return _normaliza_hora(
            grupos["hora_media"],
            30,
            grupos["periodo_media"],
        )

    if grupos["hora_menos_cuarto"]:
        hora = int(grupos["hora_menos_cuarto"]) - 1

        if hora == 0:
            hora = 12

        return _normaliza_hora(
            hora,
            45,
            grupos["periodo_menos_cuarto"],
        )

    if grupos["hora_punto"]:
        return _normaliza_hora(
            grupos["hora_punto"],
            0,
            grupos["periodo_punto"],
        )

    if grupos["hora_periodo"]:
        return _normaliza_hora(
            grupos["hora_periodo"],
            0,
            grupos["periodo"],
        )

    return coincidencia.group(0)


def normalizaHoras(ficText, ficNorm):
    """
    Lee un fichero de texto, normaliza sus expresiones horarias válidas y
    escribe el resultado en otro fichero.

    >>> normalizaHoras('horas.txt', 'horas_norm.txt')
    """
    patron = re.compile(
        r"\b(?P<hora_dos_puntos>[01]?\d|2[0-3]):"
        r"(?P<min_dos_puntos>[0-5]\d)\b"
        r"|"
        r"\b(?P<hora_h>[01]?\d|2[0-3])h"
        r"(?:(?P<min_h>[0-5]\d?)m)?"
        r"(?:\s+de\s+la\s+(?P<periodo_h>"
        r"mañana|tarde|noche|madrugada))?\b"
        r"|"
        r"\b(?P<hora_media>[1-9]|1[0-2])\s+y\s+media"
        r"(?:\s+de\s+la\s+(?P<periodo_media>"
        r"mañana|tarde|noche|madrugada))?\b"
        r"|"
        r"\b(?P<hora_menos_cuarto>[1-9]|1[0-2])\s+menos\s+cuarto"
        r"(?:\s+de\s+la\s+(?P<periodo_menos_cuarto>"
        r"mañana|tarde|noche|madrugada))?\b"
        r"|"
        r"\b(?P<hora_punto>[1-9]|1[0-2])\s+en\s+punto"
        r"(?:\s+de\s+la\s+(?P<periodo_punto>"
        r"mañana|tarde|noche|madrugada))?\b"
        r"|"
        r"\b(?P<hora_periodo>[1-9]|1[0-2])\s+de\s+la\s+"
        r"(?P<periodo>mañana|tarde|noche|madrugada)\b",
        re.IGNORECASE,
    )

    with open(ficText, encoding="utf-8") as entrada:
        texto = entrada.read()

    texto = patron.sub(
        lambda coincidencia: _reemplaza(coincidencia) or coincidencia.group(0),
        texto,
    )

    with open(ficNorm, "w", encoding="utf-8") as salida:
        salida.write(texto)


if __name__ == "__main__":
    import doctest

    doctest.testmod()