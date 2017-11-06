# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

#Temperaturstufen abfragen
prog = {}
instance = 0
rep = input('Temperaturstufe hinzufügen? ')
while rep == 'yes':
    instance +=1
    temperature_input = int(input('Bitte Zieltemperatur eingeben [°C]: '))
    zeit_input = int(input('Bitte Dauer eingeben [min]: '))
    prog[instance] = [temperature_input,zeit_input]
    rep = input('Weitere Temperaturstufe hinzufügen? ')

#Temperdauer berechnen
time_abs = 0
for key in prog:
    time_abs += prog[key][1]

#Gesamtzahl der Stufen berechnen. Abhängig von time_abs, da Ofen nicht im Sekundenbereich arbeiten kann und somit keine Nachkommastellen in der Zeitberechnung aufweisen darf
steps = 98
if time_abs % 98 != 0:
    while time_abs % steps != 0:
        steps -=1

#Zeitdauer je Stufe berechnen
time_step = time_abs/steps
#Minuten-Format in hh:mm Format umwandeln
time_step_h = int(time_step // 60)
time_step_min = int(time_step % 60)
if time_step_h < 10:
    time_step_h_str = '0' + str(time_step_h)
if time_step_min < 10:
    time_step_min_str = '0' + str(time_step_min)
time_step_str = time_step_h_str + ':' + time_step_min_str




#Stufenanteil berechnen und dem Programmdictionary hinzufügen
for key in prog:
    instance_step =prog[key][1] / time_abs * steps #Verhältnis aus zugewiesener und absoluter Zeit wird mit den Anzahl der Stufen multipliziert
    prog[key].append(instance_step)

#Heizrate (in Stufen) berechnen und dem Programmdictionary hinzufügen
for key in prog:
    # Heizen von Starttemperatur auf erste Zieltemperatur
    if key == 1:
        Temp_per_step = (prog[key][0]-25) / prog[key][2]
    # Wenn zwei aufeinanderfolgende Zieltemperaturen gleich sind, soll die Temperatur gehalten werden, Heizrate entspricht also 0
    elif prog[key][0] == prog[key-1][0]:
        Temp_per_step = 0
    # Heizen von einer Zieltemperatur auf eine Größere
    else:
        Temp_per_step = (prog[key][0]-prog[key-1][0]) / prog[key][2]
    prog[key].append(Temp_per_step)


#Programm schreiben
#Header auslesen
with open('Data/test_firas.prg', 'r', encoding="iso-8859-1") as prg:
    header = prg.readlines()[0:5]
prg.close()

#Zeilenaufbau definieren
row = '{No}\t{Value_T}\t{Length}\t-999\t999\t0\t0\t{End}\t{Value_F}\t{Length}\t-999\t999\t0\t0\t{End}\t{Jump}\t\n'

#Temperaturprogramm erstellen
temp_step = 25.0 #Starttemperatur
No = 0 #Erste Stufe
with open('test2.prg', 'w', encoding="iso-8859-1") as file:
    #Header schreiben
    for i in header:
            file.write(i)
    #Erste Zeile schreiben
    row_first = row.format(No=No,Value_T='25.0', Length='00:10', End='98', Value_F='50.0',Jump='Jump')
    file.write(row_first)
    #Temperaturprogramm schreiben
    for key in prog:
        instance_step_current = 0 #Mithilfe instance_step_current kann ermittelt werden, ob alle Stufen einer Instanz berücksihtig wurden
        while instance_step_current < prog[key][2]: #Jeder Instanz wurde eine absolute Anzahl an Stufen zugeschrieben, solange instance_step_current dieser Zahl nicht entspricht wurden noch nicht alle Stufen der Instanz berücksichtigt
            instance_step_current += 1
            temp_step += prog[key][3]
            temp_step_str = str(round(temp_step,1))
            No += 1
            row_step = row.format(No=No, Value_T=temp_step_str, End='', Length=time_step_str, Value_F='25.0',Jump='')
            file.write(row_step)
    #Restliche Zeilen mit Kühlzeilen ausfüllen
    while No < 99:
        No += 1
        row_fill =  row.format(No=No, Value_T='20', End='', Length='00:10', Value_F='50.0',Jump='')
        file.write(row_fill)
file.close()

#Temperaturprogramm plotten
data = open('test2.prg', 'r', encoding="iso-8859-1")

content = data.readlines()[5:]

data.close()

time = 0

temp_ar = np.array([])
time_ar = np.array([])
plot_data = np.array([])
bundle = np.array([])

for i in content:
    values = i.split('\t')

    temp = values[1]
    temp_ar = np.append(temp_ar, temp)

    time_frac = values[2].split(':')
    time += int(time_frac[0]) + (int(time_frac[1]) / 60)
    time_ar = np.append(time_ar, time)

plt.plot(time_ar, temp_ar)
plt.show()
