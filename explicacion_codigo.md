# Modulación y Demodulación LoRa

## Introducción
LoRa (Long Range) es una tecnología de modulación de radiofrecuencia utilizada en redes de área amplia de baja potencia (LPWAN). Permite la comunicación a largas distancias con un consumo de energía muy bajo.

## Modulación LoRa
La modulación LoRa se basa en la técnica de modulación por espectro ensanchado de chirp (CSS). Los chirps son señales cuya frecuencia aumenta o disminuye linealmente con el tiempo.

### Características de la Modulación LoRa
- **Ancho de Banda (BW):** El rango de frecuencias utilizado para la transmisión.
- **Factor de Expansión (SF):** Determina la duración del chirp y la tasa de datos.
- **Frecuencia Central (Fc):** La frecuencia central de la señal transmitida.

### Proceso de Modulación
1. **Generación de Chirps:** Se generan chirps ascendentes y descendentes.
2. **Codificación de Datos:** Los datos se codifican en la fase de los chirps.
3. **Transmisión:** La señal modulada se transmite a través del canal de comunicación.

## Demodulación LoRa
La demodulación LoRa es el proceso inverso a la modulación, donde se recuperan los datos originales a partir de la señal modulada recibida.

### Proceso de Demodulación
1. **Recepción de la Señal:** La señal modulada se recibe a través de la antena.
2. **Sincronización:** Se sincroniza la señal recibida con un chirp de referencia.
3. **Decodificación de Datos:** Se extraen los datos a partir de la fase de los chirps recibidos.

## Ventajas de LoRa
- **Larga Distancia:** Permite la comunicación a varios kilómetros de distancia.
- **Bajo Consumo de Energía:** Ideal para dispositivos IoT con baterías de larga duración.
- **Robustez:** Resistente a interferencias y ruido.

## Aplicaciones de LoRa
- **Monitoreo Remoto:** Sensores ambientales, medidores inteligentes.
- **Agricultura:** Monitoreo de cultivos y ganado.
- **Ciudades Inteligentes:** Gestión de recursos y servicios urbanos.

## Aspectos Físico-Matemáticos del Código

El código proporcionado implementa la modulación y demodulación LoRa utilizando varios conceptos físico-matemáticos clave. A continuación, se describen estos aspectos:

### Parámetros de Modulación
- **Factor de Expansión (SF):** Determina la duración del chirp y la tasa de datos. En el código, se define como `SF = 8`.
- **Ancho de Banda (BW):** El rango de frecuencias utilizado para la transmisión. En el código, se define como `BW = 1000` Hz.
- **Frecuencia de Muestreo (Fs):** La frecuencia a la que se muestrea la señal. En el código, se define como `Fs = 1000` Hz.

### Generación de Chirps
La función `generar_symb` genera los chirps necesarios para la modulación. Utiliza la siguiente fórmula matemática para crear un chirp ascendente:

chirp(t) = exp(i * 2 * pi * ((s * BW / 2^SF) * t + (BW / 2 * T_s) * t^2))


donde \( s \) es el símbolo a transmitir, \( BW \) es el ancho de banda, \( SF \) es el factor de expansión, y \( T_s \) es la duración del símbolo.

### Frecuencia Instantánea
La frecuencia instantánea del chirp se calcula utilizando la fase instantánea de la señal:

frecuencia_instantánea = d(fase_instantánea) / (2 * pi * dt)

Esto se implementa en el código utilizando la función `np.unwrap` para obtener la fase y `np.diff` para calcular la derivada.

### Demodulación
Para la demodulación, se utiliza un chirp descendente de referencia (`base_down_chirp`). La señal recibida se multiplica por este chirp para obtener la señal demodulada (`dechirped`). Luego, se aplica una Transformada Rápida de Fourier (FFT) para obtener el espectro de potencia de la señal demodulada:

dechirped_fft = FFT(dechirped)


El espectro de potencia se calcula como:

potencia = |dechirped_fft|^2



### Visualización
El código utiliza `matplotlib` para visualizar diferentes aspectos de la señal modulada y demodulada, incluyendo la variación de frecuencia, la amplitud en función del tiempo, y el espectro de potencia.

Estas visualizaciones ayudan a entender mejor el comportamiento de la señal LoRa durante el proceso de modulación y demodulación.

## Conclusión
La tecnología LoRa ofrece una solución eficiente para la comunicación de larga distancia con bajo consumo de energía, siendo ideal para aplicaciones IoT y redes de sensores.


### Referencias:
- [1] Frequency Shift Chirp Modulation: The LoRa Modulation. Lorenzo Vangelista. IEEE Signal Procesing Letters, Vol. 24, No. 12, 2017. [enlace al documento](https://drive.google.com/file/d/1pGHh7WLAYIRgUsoMKCYRLLRIZi5ozapL/view?usp=sharing)
- [2] How LoRa Modulation really works - long range communication using chirps; [enlace al youtube](https://www.youtube.com/watch?v=jHWepP1ZWTk)

