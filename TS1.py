#%% ------------------------- CONSIGNA -------------------------

"""
Estudiante: Iara Alvarez Costa
Fecha: 20/08/2026

---------------------------------

Se pide simular una señal senoidal ruidosa de 1 watt de potencia,...
...cuyo ruido acompañante se pueda programar a través de la relación...
...SNR entre potencias. 

"""

#%% ------------------ IMPORTACION DE MODULOS -------------------

import numpy as np
import matplotlib.pyplot as plt

#%% ---------------------- DEFINICION CTES ----------------------

fs = 1000 #Frecuencia muestreo (Hz) 
N = 1000 #Cant. muestras
vmax = np.sqrt(2) #amp max
dc = 0 #offset
ff = 3 #Frecuencia sinusoidal (Hz)
ph = 0 #rad
SNR = 10 #dB
Psen = 1 #Potencia media senoide [Watt]
ur = 0 #Media del ruido


#%% ------------------------- FUNCIONES -------------------------

# Generador de señal senoidal
def gen_sin (vmax = 1, dc = 0, ff = 1, ph=0, nn = N, fs = fs):

    #genero un vector de valores de 0 a N/fs segundos a intervalos de 1/fs
    tt = np.arange(0, stop=N/fs, step=1/fs)
    #genero un vector con los valores de 'dc + vmax.Sen(2pi.ff.tt + ph)' para cada valor de tt
    xx = dc + vmax * np.sin (2 * np.pi * ff * tt + ph)
    
    return tt, xx 


# Generador de ruido
def gen_noise (SNR = SNR, Psen = Psen, ur = ur, nn = N):

    #despejo la potencia del ruido en función de SNR y Psen    
    Pr = Psen / (10**(SNR/10))
     
    #calculo la desviación estandar del ruido en base a Pr (Pr = σr^2)
    desv_est_r = np.sqrt(Pr)
    
    #genero un vector de nros aleatorios de distribucion normal
    ruido = np.random.normal(ur, desv_est_r, nn)
    
    return ruido


#%% ------------------------ MAIN SCRIPT ------------------------

#Invoco la función generadora de senoides
tt, xx = gen_sin( vmax, dc, ff, ph, N, fs) 

#Invoco la función generadora de ruido
ruido = gen_noise (SNR, Psen, ur, N)

#Armo manualmente la señal ruidosa
noisy_xx = xx + ruido



#Grafico señal ruidosa
plt.plot(tt,ruido)
plt.plot(tt,noisy_xx)
plt.plot(tt,xx)
plt.grid()
plt.show()