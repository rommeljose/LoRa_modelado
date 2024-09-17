import numpy as np
import matplotlib.pyplot as plt

# Define características de la modulación
SF = 8
BW = 1000
Fs = 1000

# Define el símbolo que se va a transmitir
s = 189

# Relación señal ruido
SNR = -10

# Período de muestreo y duración de cada símbolo
T = 1 / BW
Ts = (2 ** SF) * T
num_samples = int(Ts * Fs)

n_sy = 1  # Número de símbolos

# Función para generar símbolos
def generar_symb(Ts, Fs, s, SF):
    t = np.linspace(0, Ts, int(Ts * Fs))
    chirp = np.exp(1j * 2 * np.pi * (s * BW / (2 ** SF) * t + (BW / (2 * Ts)) * t**2))
    return t, chirp

# Calcula los símbolos para enviar un payload
symb_t, symb_f = generar_symb(Ts, Fs, s, SF)

# Vector de tiempo para n_sy símbolos
x = np.linspace(0, n_sy * Ts, n_sy * (2 ** SF))

# Ajustar el vector de tiempo para cubrir 300 ms
symb_t_elongated = np.linspace(0, 0.3, int(0.3 * Fs))

# Generar el chirp con la base temporal elongada
symb_f_elongated = np.exp(1j * 2 * np.pi * (s * BW / (2 ** SF) * symb_t_elongated + (BW / (2 * Ts)) * symb_t_elongated**2))

# Calcular la frecuencia instantánea
instantaneous_phase = np.unwrap(np.angle(symb_f_elongated))
instantaneous_frequency = np.diff(instantaneous_phase) / (2.0 * np.pi) * Fs

# Transmite
base_down_chirp = np.zeros(num_samples, dtype=complex)

k = 0

for n in range(num_samples):
    if k >= (2 ** SF):
        k = k - (2 ** SF)
    k = k + 1
    base_down_chirp[n] = (1 / np.sqrt(2 ** SF)) * np.exp(-1j * 2 * np.pi * k * (k / (2 ** SF * 2)))

dechirped = symb_f * base_down_chirp
dechirped_fft = np.fft.fft(dechirped)

n = len(dechirped_fft)  # número de muestras
f = (np.arange(n)) * (Fs / n)  # Rango de frecuencias
f_sym = (f * 2 ** SF) / BW
power = np.abs(dechirped_fft) ** 2  # potencia de la señal

# Ajustar el tamaño de las fuentes
plt.rcParams.update({'font.size': 8})

# Crear una figura con subplots
plt.figure(figsize=(12, 10))

# Grafica de la variación de la frecuencia para símbolo 189 con factor de dispersión 8
plt.subplot(5, 1, 1)
plt.plot(symb_t_elongated[:-1], instantaneous_frequency)
plt.title('Variación de la Frecuencia para el símbolo s=189')
plt.xlabel('Tiempo (s)')
plt.ylabel('Frecuencia (Hz)')
plt.grid()

# Grafica Amplitud Vs. tiempo del Chrirp con el simbolo 189 modulado con factor de dispersión 8
plt.subplot(5, 1, 2)
plt.plot(symb_t, np.real(symb_f))
plt.title('Chirp con el símbolo 189 modulado con factor de dispersión 8')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()



# Gráfica del Chirp utilizado para demodular con valor de dispersión 8
plt.subplot(5, 1, 3)
plt.plot(symb_t, np.real(base_down_chirp))
plt.title('Chirp utilizado para demodular con valor de dispersión 8')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()

# Gráfica Amplitud vs. tiempo del chirp demodulado que incluye el símbolo 189
plt.subplot(5, 1, 4)
plt.plot(symb_t, np.real(dechirped))
plt.title('Chirp demodulado que incluye el símbolo 189')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()

# Graficar el espectro de potencia
plt.subplot(5, 1, 5)
plt.plot(f_sym, power)
plt.title('Espectro de Potencia del Símbolo Demodulado')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Potencia')
plt.grid()

# Ajustar el layout para que no se solapen los subplots
plt.tight_layout()
plt.show()