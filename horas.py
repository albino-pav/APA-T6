"""

This function reads a text file with time expressions, normalizes them to the
HH:MM format, and writes the result to another file.

>>> import os
>>> texto_prueba = "test_input.txt"
>>> output_prueba = "test_output.txt"
>>> contenido = ('La llegada del tren está prevista a las 18:30\\n' +
...              'Tenía su clase entre las 8h y las 10h30m\\n' +
...              'Se acaba a las 4 y media de la tarde\\n' +
...              'Empieza a trabajar a las 7h de la mañana\\n' +
...              'Es lo mismo 5 menos cuarto que 4:45\\n' +
...              'Tenemos descanso hasta las 17h5m\\n' +
...              'Las campanadas son a las 12 de la noche\\n')
>>> with open(texto_prueba, 'w') as f:
...     _ = f.write(contenido)
>>> normalizahoras(texto_prueba, output_prueba)
>>> with open(output_prueba, 'r') as f:
...     output_lines = f.readlines()
>>> output_lines == ['La llegada del tren está prevista a las 18:30\\n',
...                  'Tenía su clase entre las 08:00 y las 10:30\\n',
...                  'Se acaba a las 16:30\\n',
...                  'Empieza a trabajar a las 07:00\\n',
...                  'Es lo mismo 04:45 que 04:45\\n',
...                  'Tenemos descanso hasta las 17:05\\n',
...                  'Las campanadas son a las 00:00\\n']
True
>>> os.remove(texto_prueba)
>>> os.remove(output_prueba)

"""

import re

def normalizahoras(ficText, ficNorm):
    rehh = r'\d{1,2}'
    remm = r'\d{2}'
    rehhmm_standard = rf'(?P<hh_standard>{rehh}):(?P<mm_standard>{remm})'
    rehhmm_hhmm = rf'(?P<hh_hhmm>{rehh})h(?P<mm_hhmm>{remm})m'
    rehh_en_punto = rf'(?P<hh_en_punto>{rehh}) en punto'
    rehh_y_cuarto = rf'(?P<hh_y_cuarto>{rehh}) y cuarto'
    rehh_y_media = rf'(?P<hh_y_media>{rehh}) y media'
    rehh_menos_cuarto = rf'(?P<hh_menos_cuarto>{rehh}) menos cuarto'

    pattern = re.compile(
        rf'({rehhmm_standard}|{rehhmm_hhmm}|{rehh_en_punto}|{rehh_y_cuarto}|{rehh_y_media}|{rehh_menos_cuarto})',
        re.IGNORECASE)

    with open(ficText, 'rt') as fpText, open(ficNorm, 'wt') as fpNorm:
        for linea in fpText:
            while (match := pattern.search(linea)):
                fpNorm.write(linea[:match.start()])
                if match.group('hh_standard'):
                    hh = int(match.group('hh_standard'))
                    mm = int(match.group('mm_standard'))
                elif match.group('hh_hhmm'):
                    hh = int(match.group('hh_hhmm'))
                    mm = int(match.group('mm_hhmm'))
                elif match.group('hh_en_punto'):
                    hh = int(match.group('hh_en_punto'))
                    mm = 0
                elif match.group('hh_y_cuarto'):
                    hh = int(match.group('hh_y_cuarto'))
                    mm = 15
                elif match.group('hh_y_media'):
                    hh = int(match.group('hh_y_media'))
                    mm = 30
                elif match.group('hh_menos_cuarto'):
                    hh = int(match.group('hh_menos_cuarto')) - 1 if int(match.group('hh_menos_cuarto')) > 1 else 23
                    mm = 45
                fpNorm.write(f'{hh:02}:{mm:02}')
                linea = linea[match.end():]
            fpNorm.write(linea)

if __name__ == "__main__":
    import doctest
    doctest.testmod()