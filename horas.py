#!/usr/bin/python3

import re

regex1 = r"(?P<hh>\d{1,2}):(?P<mm>\d{1,2})"
regex2 = r"(?P<hh>\d{1,2})h(?P<mm>\d{1,2})m"
regex3 = r"(?P<hh>\d{1,2}) de la noche"
regex4 = r"(?P<hh>\d{1,2})h de la mañana"
regex5 = r"(?P<hh>\d{1,2}) de la tarde"


def normalizaHoras(ficIn, ficOut):
    with open(ficIn, "rt") as fin, open(ficOut, "wt") as fout:
        for linia in fin:
            
            if (temps := re.search(regex1, linia)):
                 
                print("regex1 =>",linia)
                
                print("hh=>",temps["hh"])
                print("mm=>",temps["mm"])
                
                 
                print(linia[:temps.start()]);
                fout.write(linia[:temps.start()])
                
                hora = int(temps["hh"])
                minuto = int(temps["mm"]) if temps["mm"] else 0
                
                while(minuto>59):
                    minuto-=60
                    hora+=1
                
                while(hora>23):
                    hora-=23
                
                
                print(f"{hora:02d}:{minuto:02d}")
                fout.write(f"{hora:02d}:{minuto:02d}")
                
                print(linia[temps.end():]);
                fout.write(linia[temps.end():])
                
            elif (temps := re.search(regex2, linia)):
                 
                print("regex2 =>",linia)
                
                print("hh=>",temps["hh"])
                print("mm=>",temps["mm"])
                
                 
                print(linia[:temps.start()]);
                fout.write(linia[:temps.start()])
                
                hora = int(temps["hh"])
                minuto = int(temps["mm"]) if temps["mm"] else 0
                
                while(minuto>59):
                    minuto-=60
                    hora+=1
                
                while(hora>23):
                    hora-=23
                
                
                print(f"{hora:02d}:{minuto:02d}")
                fout.write(f"{hora:02d}:{minuto:02d}")
                
                print(linia[temps.end():]);
                fout.write(linia[temps.end():])
                
            elif (temps := re.search(regex3, linia)):
                 
                print("regex3 =>",linia)
                
                print("hh=>",temps["hh"])
                
                print(linia[:temps.start()]);
                fout.write(linia[:temps.start()])
                
                hora = int(temps["hh"])
                minuto = 0
                
                while(minuto>59):
                    minuto-=60
                    hora+=1
                
                while(hora>23):
                    hora-=23
                
                
                print(f"{hora:02d}:{minuto:02d}")
                fout.write(f"{hora:02d}:{minuto:02d}")
                
                print(linia[temps.end():]);
                fout.write(linia[temps.end():])
                
            elif (temps := re.search(regex4, linia)):
                 
                print("regex4 =>",linia)
                
                print("hh=>",temps["hh"])
                
                print(linia[:temps.start()]);
                fout.write(linia[:temps.start()])
                
                hora = int(temps["hh"])
                minuto = 0
                
                while(minuto>59):
                    minuto-=60
                    hora+=1
                
                while(hora>23):
                    hora-=23
                
                
                print(f"{hora:02d}:{minuto:02d}")
                fout.write(f"{hora:02d}:{minuto:02d}")
                
                print(linia[temps.end():]);
                fout.write(linia[temps.end():])
            elif (temps := re.search(regex5, linia)):
                 
                print("regex5 =>",linia)
                
                print("hh=>",temps["hh"])
                
                print(linia[:temps.start()]);
                fout.write(linia[:temps.start()])
                
                hora = int(temps["hh"])+12
                minuto = 0
                
                while(minuto>59):
                    minuto-=60
                    hora+=1
                
                while(hora>23):
                    hora-=23
                
                
                print(f"{hora:02d}:{minuto:02d}")
                fout.write(f"{hora:02d}:{minuto:02d}")
                
                print(linia[temps.end():]);
                fout.write(linia[temps.end():])
            else:
                print("no =>",linia)
                

normalizaHoras("horas.txt","horas2.txt")
