import matplotlib.pyplot as plt
import numpy as np

#Temperaturprogramm plotten
def diagram(prg_file):
    data = open(str(prg_file), 'r', encoding="iso-8859-1")

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
