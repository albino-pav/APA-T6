import re


PERIODO_RE = (
    r"de\s+la\s+mañana|"
    r"del\s+mediod[ií]a|"
    r"de\s+la\s+tarde|"
    r"de\s+la\s+noche|"
    r"de\s+la\s+madrugada"
)

PATRON_PERIODO = re.compile(
    rf"""
    (?<!\d)
    (?P<hora>\d{{1,2}})
    (?:
        h(?:(?P<min_h>\d{{1,2}})m)?
      |
        \s+(?P<expr>en\s+punto|y\s+cuarto|y\s+media|menos\s+cuarto)
    )?
    \s+(?P<periodo>{PERIODO_RE})
    (?!\w)
    """,
    re.IGNORECASE | re.VERBOSE,
)

PATRON_HM = re.compile(
    rf"""
    (?<!\d)
    (?P<hora>\d{{1,2}})h(?:(?P<minuto>\d{{1,2}})m)?
    (?!\w)
    (?!\s+(?:{PERIODO_RE}))
    """,
    re.IGNORECASE | re.VERBOSE,
)

PATRON_HABLADA = re.compile(
    r"""
    (?<!\d)
    (?P<hora>\d{1,2})
    \s+(?P<expr>en\s+punto|y\s+cuarto|y\s+media|menos\s+cuarto)
    (?!\w)
    """,
    re.IGNORECASE | re.VERBOSE,
)

PATRON_DOS_PUNTOS = re.compile(
    r"(?<!\d)(?P<hora>\d{1,2}):(?P<minuto>\d{2})(?!\d)"
)


def _formatea(hora, minuto):
    return f"{hora:02d}:{minuto:02d}"


def _periodo_clave(periodo):
    periodo = periodo.lower().replace("í", "i")
    periodo = re.sub(r"\s+", " ", periodo.strip())

    if periodo == "de la mañana":
        return "manana"
    if periodo == "del mediodia":
        return "mediodia"
    if periodo == "de la tarde":
        return "tarde"
    if periodo == "de la noche":
        return "noche"
    if periodo == "de la madrugada":
        return "madrugada"

    return ""


def _hora_segun_periodo(hora, periodo):
    if not 1 <= hora <= 12:
        return None

    clave = _periodo_clave(periodo)

    if clave == "manana" and 4 <= hora <= 12:
        return 12 if hora == 12 else hora

    if clave == "mediodia":
        if hora == 12:
            return 12
        if 1 <= hora <= 3:
            return hora + 12

    if clave == "tarde" and 3 <= hora <= 8:
        return hora + 12

    if clave == "noche":
        if hora == 12:
            return 0
        if 8 <= hora <= 11:
            return hora + 12
        if 1 <= hora <= 4:
            return hora

    if clave == "madrugada" and 1 <= hora <= 6:
        return hora

    return None


def _aplica_expresion(hora, expresion, periodo=None):
    if periodo is None:
        if not 1 <= hora <= 12:
            return None
        hora_24 = 0 if hora == 12 else hora
        modulo = 12
    else:
        hora_24 = _hora_segun_periodo(hora, periodo)
        modulo = 24

        if hora_24 is None:
            return None

    if expresion is None:
        minuto = 0
    else:
        expresion = re.sub(r"\s+", " ", expresion.lower().strip())

        if expresion == "en punto":
            minuto = 0
        elif expresion == "y cuarto":
            minuto = 15
        elif expresion == "y media":
            minuto = 30
        elif expresion == "menos cuarto":
            hora_24 = (hora_24 - 1) % modulo
            minuto = 45
        else:
            return None

    return hora_24, minuto


def _sustituye_periodo(coincidencia):
    original = coincidencia.group(0)
    hora = int(coincidencia.group("hora"))
    minuto_h = coincidencia.group("min_h")
    expresion = coincidencia.group("expr")
    periodo = coincidencia.group("periodo")

    if minuto_h is not None:
        minuto = int(minuto_h)

        if not 0 <= minuto <= 59:
            return original

        hora_24 = _hora_segun_periodo(hora, periodo)

        if hora_24 is None:
            return original

        return _formatea(hora_24, minuto)

    resultado = _aplica_expresion(hora, expresion, periodo)

    if resultado is None:
        return original

    return _formatea(*resultado)


def _sustituye_hm(coincidencia):
    original = coincidencia.group(0)
    hora = int(coincidencia.group("hora"))
    minuto = coincidencia.group("minuto")
    minuto = 0 if minuto is None else int(minuto)

    if 0 <= hora <= 23 and 0 <= minuto <= 59:
        return _formatea(hora, minuto)

    return original


def _sustituye_hablada(coincidencia):
    original = coincidencia.group(0)
    hora = int(coincidencia.group("hora"))
    expresion = coincidencia.group("expr")
    resultado = _aplica_expresion(hora, expresion)

    if resultado is None:
        return original

    return _formatea(*resultado)


def _sustituye_dos_puntos(coincidencia):
    original = coincidencia.group(0)
    hora = int(coincidencia.group("hora"))
    minuto = int(coincidencia.group("minuto"))

    if 0 <= hora <= 23 and 0 <= minuto <= 59:
        return _formatea(hora, minuto)

    return original


def _normaliza_linea(linea):
    linea = PATRON_PERIODO.sub(_sustituye_periodo, linea)
    linea = PATRON_HM.sub(_sustituye_hm, linea)
    linea = PATRON_HABLADA.sub(_sustituye_hablada, linea)
    linea = PATRON_DOS_PUNTOS.sub(_sustituye_dos_puntos, linea)

    return linea


def normalizaHoras(ficText, ficNorm):
    with open(ficText, encoding="utf-8") as entrada:
        with open(ficNorm, "w", encoding="utf-8") as salida:
            for linea in entrada:
                salida.write(_normaliza_linea(linea))