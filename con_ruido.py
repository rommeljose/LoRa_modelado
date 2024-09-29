# Preparado por: Rommel Contreras / Cumaná - Venezuela
# Fecha de creación: 2021-09-25
# Fecha de actualización: 2021-09-25
# Objetivo: Simulación de la modulación chirp con ruido

# Importar librerías
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Define características de la modulación
BW = 1000
Fs = 1000

# Define el símbolo inicial que se va a transmitir
s = 189

# Relación señal ruido
SNR = -10

# Período de muestreo y duración de cada símbolo
T = 1 / BW

# Función para generar símbolos
def generar_symb(Ts, Fs, s, SF):
    t = np.linspace(0, Ts, int(Ts * Fs))
    chirp = np.exp(1j * 2 * np.pi * (s * BW / (2 ** SF) * t + (BW / (2 * Ts)) * t**2))
    return t, chirp

# Función para añadir ruido a la señal
def add_noise(signal, SNR):
    signal_power = np.mean(np.abs(signal) ** 2)
    noise_power = signal_power / (10 ** (SNR / 10))
    noise = np.sqrt(noise_power / 2) * (np.random.randn(len(signal)) + 1j * np.random.randn(len(signal)))
    return signal + noise

# Función para actualizar los gráficos
def update(val):
    s = int(slider_s.val)
    SF = int(slider_sf.val)
    Ts = (2 ** SF) * T
    num_samples = int(Ts * Fs)
    
    symb_t, symb_f = generar_symb(Ts, Fs, s, SF)
    symb_f_noisy = add_noise(symb_f, SNR)
    symb_t_elongated = np.linspace(0, 0.3, int(0.3 * Fs))
    symb_f_elongated = np.exp(1j * 2 * np.pi * (s * BW / (2 ** SF) * symb_t_elongated + (BW / (2 * Ts)) * symb_t_elongated**2))
    instantaneous_phase = np.unwrap(np.angle(symb_f_elongated))
    instantaneous_frequency = np.diff(instantaneous_phase) / (2.0 * np.pi) * Fs
    
    base_down_chirp = np.zeros(num_samples, dtype=complex)
    k = 0
    for n in range(num_samples):
        if k >= (2 ** SF):
            k = k - (2 ** SF)
        k = k + 1
        base_down_chirp[n] = (1 / np.sqrt(2 ** SF)) * np.exp(-1j * 2 * np.pi * k * (k / (2 ** SF * 2)))
    
    dechirped = symb_f_noisy * base_down_chirp
    dechirped_fft = np.fft.fft(dechirped)
    power = np.abs(dechirped_fft) ** 2

    ax1.clear()
    ax1.plot(symb_t_elongated[:-1], instantaneous_frequency)
    ax1.set_title(f'Variación de la Frecuencia para el símbolo s={s} y SF={SF}')
    ax1.set_xlabel('Tiempo (s)')
    ax1.set_ylabel('Frecuencia (Hz)')
    ax1.grid()

    ax2.clear()
    ax2.plot(symb_t, np.real(symb_f_noisy))
    ax2.set_title(f'Chirp con el símbolo {s} modulado con factor de dispersión {SF}')
    ax2.set_xlabel('Tiempo (s)')
    ax2.set_ylabel('Amplitud')
    ax2.grid()

    ax3.clear()
    ax3.plot(symb_t, np.real(base_down_chirp))
    ax3.set_title(f'Chirp utilizado para demodular con valor de dispersión {SF}')
    ax3.set_xlabel('Tiempo (s)')
    ax3.set_ylabel('Amplitud')
    ax3.grid()

    ax4.clear()
    ax4.plot(symb_t, np.real(dechirped))
    ax4.set_title(f'Chirp demodulado que incluye el símbolo {s}, con ruido')
    ax4.set_xlabel('Tiempo (s)')
    ax4.set_ylabel('Amplitud')
    ax4.grid()

    ax5.clear()
    ax5.plot(f_sym, power)
    ax5.set_title(f'Espectro de Potencia del Símbolo Demodulado {s}, con ruido')
    ax5.set_xlabel('Frecuencia (Hz)')
    ax5.set_ylabel('Potencia')
    ax5.grid()

    fig.canvas.draw_idle()

# Ajustar el vector de tiempo para cubrir 300 ms
symb_t_elongated = np.linspace(0, 0.3, int(0.3 * Fs))

# Generar el chirp con la base temporal elongada
SF = 8
Ts = (2 ** SF) * T
symb_f_elongated = np.exp(1j * 2 * np.pi * (s * BW / (2 ** SF) * symb_t_elongated + (BW / (2 * Ts)) * symb_t_elongated**2))

# Calcular la frecuencia instantánea
instantaneous_phase = np.unwrap(np.angle(symb_f_elongated))
instantaneous_frequency = np.diff(instantaneous_phase) / (2.0 * np.pi) * Fs

# Transmite
num_samples = int(Ts * Fs)
base_down_chirp = np.zeros(num_samples, dtype=complex)

k = 0

for n in range(num_samples):
    if k >= (2 ** SF):
        k = k - (2 ** SF)
    k = k + 1
    base_down_chirp[n] = (1 / np.sqrt(2 ** SF)) * np.exp(-1j * 2 * np.pi * k * (k / (2 ** SF * 2)))

symb_t, symb_f = generar_symb(Ts, Fs, s, SF)
symb_f_noisy = add_noise(symb_f, SNR)
dechirped = symb_f_noisy * base_down_chirp
dechirped_fft = np.fft.fft(dechirped)

n = len(dechirped_fft)  # número de muestras
f = (np.arange(n)) * (Fs / n)  # Rango de frecuencias
f_sym = (f * 2 ** SF) / BW
power = np.abs(dechirped_fft) ** 2  # potencia de la señal

# Ajustar el tamaño de las fuentes
plt.rcParams.update({'font.size': 8})

# Crear una figura con subplots, reduciendo el tamaño a la mitad
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(6, 5))

# Grafica de la variación de la frecuencia para símbolo 189 con factor de dispersión 8
ax1.plot(symb_t_elongated[:-1], instantaneous_frequency)
ax1.set_title(f'Variación de la Frecuencia para el símbolo s={s} y SF={SF}')
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Frecuencia (Hz)')
ax1.grid()

# Grafica Amplitud Vs. tiempo del Chrirp con el simbolo 189 modulado con factor de dispersión 8
ax2.plot(symb_t, np.real(symb_f_noisy))
ax2.set_title(f'Chirp con el símbolo {s} modulado con factor de dispersión {SF}')
ax2.set_xlabel('Tiempo (s)')
ax2.set_ylabel('Amplitud')
ax2.grid()

# Gráfica del Chirp utilizado para demodular con valor de dispersión 8
ax3.plot(symb_t, np.real(base_down_chirp))
ax3.set_title(f'Chirp utilizado para demodular con valor de dispersión {SF}')
ax3.set_xlabel('Tiempo (s)')
ax3.set_ylabel('Amplitud')
ax3.grid()

# Gráfica Amplitud vs. tiempo del chirp demodulado que incluye el símbolo 189
ax4.plot(symb_t, np.real(dechirped))
ax4.set_title(f'Chirp demodulado que incluye el símbolo {s} con ruido')
ax4.set_xlabel('Tiempo (s)')
ax4.set_ylabel('Amplitud')
ax4.grid()

# Graficar el espectro de potencia
ax5.plot(f_sym, power)
ax5.set_title(f'Espectro de Potencia del Símbolo Demodulado {s} con ruido')
ax5.set_xlabel('Frecuencia (Hz)')
ax5.set_ylabel('Potencia')
ax5.grid()

# Ajustar el layout para que no se solapen los subplots
plt.tight_layout()

# # Crear la barra deslizante para el símbolo
# ax_slider_s = plt.axes([0.2, 0.03, 0.65, 0.03], facecolor='lightgoldenrodyellow')
# slider_s = Slider(ax_slider_s, 'Símbolo', 0, 255, valinit=s, valstep=1)
# slider_s.on_changed(update)

# # Crear la barra deslizante para el factor de dispersión
# ax_slider_sf = plt.axes([0.2, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')
# slider_sf = Slider(ax_slider_sf, 'SF', 7, 12, valinit=SF, valstep=1)
# slider_sf.on_changed(update)

plt.show()