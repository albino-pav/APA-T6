"""
Sonia Sahuquillo Guillén
Marcel Farelo de la Orden

Este código se encarga de normalizar y formatear horas en un texto, identificando y 
transformando diferentes formatos de horas en un formato estándar de 24 horas (HH).

"""
import re

# Definir los patrones de expresión regular
pattern_hours = re.compile(r'(?P<hours>\d{1,2})(?P<sep>[:hH]?)?(?P<minutes>\d{2})?(?P<min_digit>\d?)')
pattern_time_of_day = re.compile(r'de la (?P<period>tarde|noche|mañana)')
pattern_half_hour = re.compile(r'\bmedia\b')
pattern_quarters = re.compile(r'(?P<direction>y|menos) cuarto')
pattern_special_cases = re.compile(r'(?P<full_match>(?P<hours>\d{1,2})h(?P<minutes>\d{1,2})m)')

def normalize_hours(input_file, output_file):
    with open(input_file, "rt") as infile, open(output_file, "wt") as outfile:
        for line in infile:
            # Procesar las horas en formato especial
            for match in re.finditer(pattern_special_cases, line):
                hour = int(match.group("hours"))
                minute = int(match.group("minutes"))
                if minute > 59:
                    outfile.write(line[:match.start()] + line[match.end():])
                    continue
                normalized_time = f"{hour:02d}:{minute:02d}"
                line = line[:match.start()] + normalized_time + line[match.end():]

            while (match := re.search(pattern_hours, line)):
                hour = int(match.group("hours"))
                minute = int(match.group("minutes") or 0)
                sep = match.group("sep")
                min_digit = match.group("min_digit")

                if minute > 59 or hour > 23:
                    outfile.write(line[:match.end()])
                    line = line[match.end():]
                else:
                    outfile.write(line[:match.start()])
                    line = line[match.end():]

                    if (match_half := re.search(pattern_half_hour, line)):
                        if hour > 12:
                            outfile.write(f"{hour}")
                            outfile.write(line[:match_half.end()])
                            line = line[match_half.end():]
                            continue
                        if match_half.group() == "media":
                            minute = 30
                            if not re.search(pattern_time_of_day, line):
                                line = line[match_half.end():]
                                outfile.write(f"{hour:02d}:{minute:02d}")
                                continue

                    if (match_quarter := re.search(pattern_quarters, line)):
                        if not re.search(pattern_time_of_day, line):
                            if match_quarter.group("direction") == "y":
                                minute = 15
                            else:
                                minute = 45
                                hour -= 1
                            line = line[match_quarter.end():]
                            outfile.write(f"{hour:02d}:{minute:02d}")
                            continue

                    if (match_period := re.search(pattern_time_of_day, line)):
                        if hour > 12:
                            outfile.write(f"{hour}")
                            outfile.write(line[:match_period.end()])
                            line = line[match_period.end():]
                            continue
                        elif match_period.group("period") == "mañana":
                            if 6 <= hour <= 12:
                                pass
                            else:
                                outfile.write(f"{hour}")
                                outfile.write(line[:match_period.end()])
                                line = line[match_period.end():]
                                continue
                        elif match_period.group("period") == "tarde":
                            if hour == 12 or 1 <= hour <= 7:
                                hour += 12
                            else:
                                outfile.write(f"{hour}")
                                outfile.write(line[:match_period.end()])
                                line = line[match_period.end():]
                                continue
                        elif match_period.group("period") == "noche":
                            if 7 <= hour <= 12:
                                hour += 12
                                if hour == 24:
                                    hour = 0
                            else:
                                outfile.write(f"{hour}")
                                outfile.write(line[:match_period.end()])
                                line = line[match_period.end():]
                                continue

                        line = line[match_period.end():]
                        outfile.write(f"{hour:02d}:{minute:02d}")
                        continue

                    if sep:
                        if sep == ":":
                            outfile.write(f"{hour:02d}:{minute:02d}")
                        else:
                            outfile.write(f"{hour}{sep}{minute:02d}")
                    else:
                        outfile.write(f"{hour:02d}:{minute:02d}")

            outfile.write(line)

if __name__ == "__main__":
    normalize_hours("horas.txt", "salida.txt")
