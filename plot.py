import matplotlib.pyplot as plt

X = [10, 20, 30, 50, 100]
#Skutecznosc_pocz[(35%)(25%)]
Y_def = [64, 150,207,341 ,692]
Y_opt = [1.79, 3.58, 5.27, 8.74, 15.26]
plt.yscale('log')
plt.plot(X,Y_def, 'bs',label='początkowy')
plt.plot(X,Y_opt, 'ro', label='końcowy')
plt.legend(loc="upper left")
plt.xlabel('liczba listów na elfa')
plt.ylabel('sekundy')
plt.grid()
plt.show()


X = ['Początkowy', 'Serializacja', 'Read committed']
Y = [0.86, 17.5, 130.7]
plt.plot(X,Y, 'bs')
plt.ylabel('transakcje na sekundę')
plt.grid()
plt.show()

X = ['Początkowy', 'Serializacja', 'Read committed']
Y = [1400, 8560, 17]
plt.plot(X,Y, 'bs')
plt.ylabel('nieudane transakcje na 2000 listów')
plt.grid()
plt.show()