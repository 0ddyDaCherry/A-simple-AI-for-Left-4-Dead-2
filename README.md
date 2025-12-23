# L4D2 AI

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![YOLOv8](https://img.shields.io/badge/AI-YOLOv8-green)
![Status](https://img.shields.io/badge/Status-Active-success)

Un bot de asistencia avanzado para **Left 4 Dead 2**, diseñado específicamente para detectar y neutralizar **Hunters**. Utiliza visión artificial (YOLOv8) combinada con filtros de color HSV y automatización de mouse a bajo nivel (Win32API) para una respuesta instantánea.

Incluye una **Interfaz Gráfica (GUI)** para configurar sensibilidades, teclas y rendimiento sin tocar el código.

---

## Características Principales

* **Detección por IA:** Utiliza un modelo YOLOv8 entrenado (`best.pt`) para identificar Hunters en tiempo real.
* **Auto-Deadstop (Defensa):** Detecta si un Hunter está demasiado cerca (pantalla roja) y realiza un empujón (Click Derecho) automático instantáneo.
* **Color Lock:** Sistema híbrido que valida la detección de la IA con un filtro de color rojo para evitar disparar a compañeros o paredes (Falsos Positivos).
* **GUI Moderna:** Panel de control estilo "Dashboard" creado con `customtkinter` (Modo Oscuro/Claro, Sliders, Pestañas).
* **Rendimiento Ajustable:** Slider de resolución dinámica para balancear entre precisión (640px) y máximos FPS (320px).
* **Memoria de Predicción:** Si el Hunter se mueve rápido y la IA lo pierde, el bot predice su trayectoria por unos milisegundos.
* **Movimiento Suave:** Uso de `win32api` para mover el mouse, evitando latigazos bruscos y simulando movimiento humano (o agresivo según configuración).

---

## Requisitos Previos

* **Sistema Operativo:** Windows 10/11.
* **Python:** 3.10 o superior.
* **GPU:** Tarjeta gráfica NVIDIA para acelerar la IA con CUDA (Opcional pero recomendado) o Tarjeta gráfica AMD.
* **Juego:** Left 4 Dead 2 (Configurado en modo Ventana o Pantalla completa sin bordes para mejor captura).

---

## Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/0ddyDaCherry/A-simple-AI-for-Left-4-Dead-2.git
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **(Recomendado para NVIDIA) Instalar PyTorch con soporte CUDA:**
    Si tienes una tarjeta NVIDIA, ejecuta esto para que el bot sea rápido:
    ```bash
    pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu118](https://download.pytorch.org/whl/cu118)
    ```

4.  **Colocar el Modelo:**
    Asegúrate de tener tu archivo de modelo entrenado `best.pt` en la carpeta raíz del proyecto (ya tenemos uno por defecto).

---

## Uso

1.  Ejecuta el lanzador (No abras `bot.py` directamente):
    ```bash
    python launcher.py
    ```
2.  Configura tus teclas y sensibilidad en la interfaz.
3.  Presiona **"GUARDAR E INICIAR"**.
4.  En el juego:
    * **`T`** (por defecto): Activar/Pausar el bot.
    * **`Z`** (por defecto): Mantener presionado para apuntar y disparar.
    * **`Q`** (por defecto): Cerrar el programa completamente.

---

## Configuración de la GUI

| Pestaña | Opción | Descripción |
| :--- | :--- | :--- |
| **Standard** | Teclas | Configura las teclas de activación, disparo y salida. |
| **Standard** | Umbral Deadstop | Sensibilidad del empujón automático (0.1 = sensible, 0.5 = necesita mucho rojo). |
| **Aimbot** | Divisores X/Y | Controlan la velocidad. Valor más alto = Movimiento más lento/suave. |
| **Aimbot** | Offset Cabeza | Ajuste vertical para apuntar al cuello/cabeza (ej. -5 píxeles). |
| **Aimbot** | Memoria | Cuántos frames sigue rastreando si pierde visión del objetivo. |
| **Visuals** | Resolución | Ajusta el tamaño de visión de la IA. Menos píxeles = Más FPS. |
| **Visuals** | Mostrar Ventana | Actívalo para ver qué ve el bot. Desactívalo para máximo rendimiento. |

---

## Aviso Legal (Disclaimer)

Este software ha sido desarrollado con fines **educativos** y de aprendizaje sobre visión artificial y automatización.

* El autor no se hace responsable del mal uso de esta herramienta.
* **Úsalo bajo tu propio riesgo** (se recomienda usarlo solo en servidores locales, modo `insecure` o partidas privadas con amigos).

---

## Créditos


Desarrollado por Oddy Da Cherry.

