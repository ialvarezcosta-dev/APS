#%% ------------------------- CONSIGNA -------------------------

"""
Estudiante: Iara Alvarez Costa
Fecha: 30/08/2026

---------------------------------

Utilizando siempre N = 1000 muestras. Se pide:

Sintetizar:

Señal sinusoidal de 2 KHz que tenga al menos 10 puntos por período.
Misma señal con 2 W de potencia media y desfasada en π/2.
Una secuencia aleatoria de ruido normalmente distribuido con DC (valor medio) 0V y varianza 0.1 W.
Una secuencia aleatoria de ruido uniformemente distribuido con DC (valor medio) 0V y varianza 0.1 W. 

FALTA
Un pulso rectangular de la misma frecuencia, 1 W de potencia y ciclo de actividad del 50% (Ver scipy.signal apartado Waveforms).
Para cada señal visualice el módulo de la transformada de Fourier.

"""

#%% ------------------ IMPORTACION DE MODULOS -------------------

import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy

#%% ---------------------- DEFINICION CTES ----------------------

"Ctes. señal senoidal"
fs = 20000 #Frecuencia muestreo [Hz] 
N = 1000 #Cant. muestras
vmax = 2 #Amp max senoidal
dc = 0 #Offset senoidal
ff = 2000 #Frecuencia sinusoidal [Hz]
ph = np.pi/2 #Fase sinusoidal [rad]

"Ctes. señal cuadrada"
fs_sq = fs
vmax_sq = 1 #La amplitud maxima debe ser = 1 para que la potencia sea 1 watt
dc_sq = dc
ph_sq = ph
duty = 0.5 #Ciclo de actividad 

"Ctes. secuencias ruido"
SNR = 13 #Relación potencia señal/ruido [dB]
Psen = 2 #Potencia media senoide [Watt]
ur = 0 #Media del ruido 


#%% ------------------------- FUNCIONES -------------------------

"Señales"
# Generador de señal senoidal
def gen_sin (vmax = 1, dc = 0, ff = 1, ph=0, nn = N, fs = fs):

    #genero un vector de valores de 0 a N/fs segundos a intervalos de 1/fs
    tt = np.arange(0, stop=nn/fs, step=1/fs)
    #genero un vector con los valores de 'dc + vmax.Sen(2pi.ff.tt + ph)' para cada valor de tt
    xx = dc + vmax * np.sin (2 * np.pi * ff * tt + ph)
    
    return tt, xx 


# Generador de señal cuadrada
def gen_square (vmax = 1, dc = 0, ff = 1, ph = 0, nn = N, fs = fs, duty = 0.5):

    #genero un vector de valores de 0 a N/fs segundos a intervalos de 1/fs
    tt = np.arange(0, stop=nn/fs, step=1/fs)
    #genero un vector con los valores de 'dc + vmax.Sen(2pi.ff.tt + ph)' para cada valor de tt
    xx = dc + vmax * scipy.signal.square(2*np.pi*ff*tt, duty)
    
    return tt, xx 

"Secuencias de ruido"
# Generador de ruido normal
def gen_noise_norm (SNR = SNR, Px = 1, ur = ur, nn = N):

    #despejo la potencia del ruido en función de SNR y Psen    
    Pr = Px / (10**(SNR/10))
     
    #calculo la desviación estandar del ruido en base a Pr (Pr = σr^2)
    desv_est_r = np.sqrt(Pr)
    
    #genero un vector de nros aleatorios de distribucion normal
    ruido = np.random.normal(ur, desv_est_r, nn)
    
    return ruido


# Generador de ruido uniforme
def gen_noise_unif (SNR = SNR, Px = 1, nn = N):

    #despejo la potencia del ruido en función de SNR y Psen    
    Pr = Px / (10**(SNR/10))
     
    #calculo el parametro b
    b = np.sqrt(3 * Pr)
    
    #genero un vector de nros aleatorios de distribucion uniforme
    ruido = np.random.uniform(-b, b, nn)
    
    return ruido


#%% ------------------------ MAIN SCRIPT ------------------------

#Señales
tt, xsen = gen_sin ( vmax, dc, ff, ph, N, fs) 
tt_sq, xsquare = gen_square (vmax_sq, dc_sq, ff, ph_sq, N, fs_sq, duty) 

#Secuencias de ruido
ruido_norm = gen_noise_norm (SNR, Psen, ur, N)
ruido_unif = gen_noise_unif (SNR, Psen, N)

#Señales ruidosas
noisy_xsen_norm = xsen + ruido_norm
noisy_xsen_unif = xsen + ruido_unif
noisy_xsquare_norm = xsquare + ruido_norm
noisy_xsquare_unif = xsquare + ruido_unif

#Calculo fft de las 4 señales ruidosas que armé
xsen_norm_fft = np.fft.fft(noisy_xsen_norm) 
xsen_unif_fft = np.fft.fft(noisy_xsen_unif)
xsq_norm_fft = np.fft.fft(noisy_xsquare_norm)
xsq_unif_fft = np.fft.fft(noisy_xsquare_unif)

#Selecciono las muestras de las señales transformadas hasta la frec de Nyquist (N/2)

A = xsen_norm_fft[:N//2]
AdB = 20*np.log10(np.abs(A)) #Expreso el espectro en decibeles para mejor visualizacion

B = xsen_unif_fft[:N//2]
BdB = 20*np.log10(np.abs(B))

C = xsq_norm_fft[:N//2]
CdB = 20*np.log10(np.abs(C))

D = xsq_unif_fft[:N//2]
DdB = 20*np.log10(np.abs(D))

#Armo vector de frecuencias
frec = np.arange(N//2) * fs/N

fig, axs = plt.subplots(2, 2, figsize=(10, 8))

axs[0, 0].plot(frec, AdB, color='blue')
axs[0, 0].set_title('FFT senoidal con nq normal')

axs[1, 0].plot(frec, BdB, color='green')
axs[1, 0].set_title('FFT senoidal con nq uniforme')

axs[0, 1].plot(frec, CdB, color='orange')
axs[0, 1].set_title('FFT cuadrada con nq normal')

axs[1, 1].plot(frec, DdB, color='red')
axs[1, 1].set_title('FFT cuadrada con nq uniforme')

for ax in axs.flat:
    ax.set_xlabel("Frecuencia [Hz]")
    ax.set_ylabel("Módulo (dB)")
    ax.grid()

plt.tight_layout(w_pad=3, h_pad=3)
plt.show()