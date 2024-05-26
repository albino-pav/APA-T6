import re

rehh = r'(?P<hh>\d{1,2})'
remm = r'(?P<mm>\d{1,2})'
rehhmm = rf'{rehh}[hH]({remm}[mM])?'
reexpr = r'(?P<expr>en punto|y cuarto|y media)'

def expr2mins(expr):
    if expr == 'en punto':
        return 0
    elif expr == 'y cuarto':
        return 15
    elif expr == 'y media':
        return 30
    else:
        return None
    

def normalizaHoras(ficText, ficNorm):
    with open(ficText,'rt') as fpText, open(ficNorm,'wt') as fpNorm:
        for linea in fpText:
             while (match := re.search(reexpr, linea)):
                fpNorm.write(linea[:match.start()])
                expr = match['expr']
                mins = expr2mins(expr)
                if mins is not None:
                    fpNorm.write(f':{mins:02d}')
                else:
                    fpNorm.write(match.group())
                linea = linea[match.end():]

             while (match := re.search(rehhmm, linea)):
                fpNorm.write(linea[:match.start()])
                linea = linea[match.end():]
                hora = int(match['hh'])
                minuto = int(match['mm']) if match['mm'] else 0
                fpNorm.write(f'{hora:02d}:{minuto:02d}')

             fpNorm.write(linea)