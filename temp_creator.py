# -*- coding: utf-8 -*-

from tools.plot import diagram

#Temperaturstufen abfragen
prog = []
instance = 0
rep = input('Temperaturstufe hinzufügen? ')
while rep == 'yes':
    instance +=1
    temperature_input = int(input('Bitte Zieltemperatur eingeben [°C]: '))
    zeit_input = int(input('Bitte Dauer eingeben [min]: '))
    prog.append([instance, temperature_input, zeit_input])
    rep = input('Weitere Temperaturstufe hinzufügen? ')

#prog = [[1,50,30],[2,70,60],[3,180,120]]

#Temperdauer berechnen
time_abs = 0
for i in prog:
    time_abs += i[2]

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
else:
    time_step_h_str = str(time_step_h)
if time_step_min < 10:
    time_step_min_str = '0' + str(time_step_min)
else:
    time_step_min_str = str(time_step_min)
time_step_str = time_step_h_str + ':' + time_step_min_str




#Stufenanteil berechnen und dem Programmdictionary hinzufügen
for i in prog:
    instance_step =i[2] / time_abs * steps #Verhältnis aus zugewiesener und absoluter Zeit wird mit den Anzahl der Stufen multipliziert
    i.append(instance_step)

#Heizrate (in Stufen) berechnen und dem Programmdictionary hinzufügen
n = -1
for i in prog:
    # Heizen von Starttemperatur auf erste Zieltemperatur
    if n == -1:
        Temp_per_step = (i[1]-25) / i[3]
        n += 1
        # Heizen von einer Zieltemperatur auf eine Größere
    else:
        Temp_per_step = (i[1]-prog[n][1]) / i[3]
        n += 1
    i.append(Temp_per_step)


#Programm schreiben
#Header auslesen
with open('Data/Header.prg', 'r', encoding="UTF-8") as prg:
    header = prg.readlines()[0:5]
prg.close()

#Zeilenaufbau definieren
row = '{No}\t{Value_T}\t{Length}\t-999\t999\t0\t0\t{End}\t{Value_F}\t{Length}\t-999\t999\t0\t0\t{End}\t{Jump}\t\n'

#Temperaturprogramm erstellen
temp_step = 25.0 - prog[0][4] #Starttemperatur
No = 0 #Erste Stufe
with open('test2.prg', 'w', encoding="iso-8859-1") as file:
    #Header schreiben
    for i in header:
            file.write(i)
    #Erste Zeile schreiben
    row_first = row.format(No=No,Value_T='25.0', Length='00:10', End='98', Value_F='50.0',Jump='Jump')
    file.write(row_first)
    #Temperaturprogramm schreiben
    for i in prog:
        instance_step_current = 0 #Mithilfe instance_step_current kann ermittelt werden, ob alle Stufen einer Instanz berücksihtig wurden
        while instance_step_current < i[3]: #Jeder Instanz wurde eine absolute Anzahl an Stufen zugeschrieben, solange instance_step_current dieser Zahl nicht entspricht wurden noch nicht alle Stufen der Instanz berücksichtigt
            instance_step_current += 1
            temp_step += i[4]
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

print(prog)

diagram('test2.prg')
