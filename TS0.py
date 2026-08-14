# -*- coding: utf-8 -*-
"""
Estudiante: Iara Alvarez Costa
Fecha: 12/08/2026

---------------------------------

La tarea consiste en programar una función que genere señales senoidales y que permita parametrizar:

la amplitud máxima de la senoidal (volts)
su valor medio (volts)
la frecuencia (Hz)
la fase (radianes)
la cantidad de muestras digitalizada por el ADC (# muestras)
la frecuencia de muestreo del ADC.


¿A partir de que ff el gráfico deja de parecer una sinusoidal? 
Resp: A partir de N/2

"""
#%% Importación de módulos

import numpy as np
import matplotlib.pyplot as plt


#%% Definicion ctes experimentales

fs = 1000 #Frecuencia muestreo (Hz) 
N = 1000 #muestras
vmax = 1.5 #amp max
dc = 0 #offset
ff = 10 #Frecuencia sinusoidal (Hz)
ph = 0 #rad


#%% Funciones

def gen_sin (vmax = 1, dc = 0, ff = 1, ph=0, nn = N, fs = fs):

    tt = np.arange(0, stop=N/fs, step=1/fs)#genero un vector de valores de 0 a N/fs segundos a intervalos de 1/fs
    xx = dc + vmax * np.sin (2 * np.pi * ff * tt + ph)
    
    return tt, xx


#%% Main Script

#Invoco la función
tt, xx = gen_sin( vmax, dc, ff, ph, N, fs) 


#Grafico
plt.plot(tt,xx)
plt.xlabel("Tiempo (s)")
plt.title("Frec: " + str(ff) + "Hz | Sample frec: " + str(fs) + "Hz | Phase: " + str(ph) + "rad")
plt.grid()
plt.show()

"""1) Acceder a cuenta de GitHub internet
   2) Create repository (APS)
   3) -> Projects -> Create project (TS0) -> Untitle project, cambiar nombre TS0, revisar que esté en depository
   4) Poner todo public
   5) Upload existing file
   6) Acceder al archivo subido para verificar que se vea el código
   
   Pra generar archivo Jupyter
   1) Entrar al Spyder
   2) Buscar opción '"""