# SimuStat 📊⚙️

**SimuStat** es una plataforma interactiva web diseñada para la generación y validación estadística de números pseudoaleatorios. El proyecto implementa algoritmos de generación de variables uniformes y aplica pruebas formales de validación estadística para certificar la calidad de las secuencias generadas, facilitando la comprensión y el análisis de sistemas de simulación.

---

## 🚀 Arquitectura del Proyecto

El sistema está dividido en una arquitectura desacoplada de Cliente-Servidor (Frontend y Backend) que se comunican mediante una API REST:

*   **Backend**: Desarrollado en **Python** utilizando **FastAPI**. Ofrece una API rápida, validación automática de datos con Pydantic y documentación interactiva integrada mediante **Swagger UI**.
*   **Frontend**: Desarrollado en **React** con **TypeScript** utilizando **Vite** para un desarrollo ultrarrápido y **TailwindCSS v4** para un diseño moderno, interactivo y premium. Las visualizaciones utilizan **Recharts** y **Lucide Icons**.

---

## 🧠 Modelos Matemáticos y Algoritmos

### 1. Generadores de Números Pseudoaleatorios (Distribución Uniforme)
El proyecto genera secuencias de números pseudoaleatorios en el intervalo $[0, 1)$ mediante dos metodologías:

*   **Método Congruencial**:
    *   *Lineal*: Define la relación recursiva:
        $$x_{i+1} = (a \cdot x_i + c) \pmod m$$
    *   *Multiplicativo*: Simplifica la relación omitiendo la constante aditiva $c$:
        $$x_{i+1} = (a \cdot x_i) \pmod m$$
    *   Para ambos, el número pseudoaleatorio normalizado es $r_i = \frac{x_i}{m}$ (o $\frac{x_i}{m-1}$).
*   **Método de Cuadrados Medios (Mid-Square)**:
    *   A partir de una semilla $x_0$ de $d$ dígitos (donde $d$ es par), se eleva al cuadrado $x_0^2$.
    *   Se extraen los $d$ dígitos centrales de $x_0^2$ para obtener el siguiente valor de la secuencia $x_1$.
    *   Se normaliza como $r_1 = \frac{x_1}{10^d}$. Se repite recursivamente.

---

### 2. Pruebas Estadísticas de Validación Obligatorias
Para certificar que una secuencia generada $R = \{r_1, r_2, \dots, r_n\}$ se comporta efectivamente como una distribución uniforme $U(0, 1)$, se aplican tres pruebas fundamentales:

#### A. Prueba de Media (Validación del Valor Esperado)
Valida si el valor promedio de la muestra es estadísticamente igual a $0.5$ con un nivel de significancia $\alpha$.
*   **Hipótesis**:
    $$H_0: \mu = 0.5$$
    $$H_1: \mu \neq 0.5$$
*   **Estadístico de prueba (Media Muestral)**:
    $$\bar{x} = \frac{1}{n} \sum_{i=1}^n r_i$$
*   **Límites de Aceptación**:
    $$LI = 0.5 - Z_{\alpha/2} \cdot \frac{1}{\sqrt{12n}}$$
    $$LS = 0.5 + Z_{\alpha/2} \cdot \frac{1}{\sqrt{12n}}$$
    *(Donde $Z_{\alpha/2}$ es el valor de la distribución normal estándar para la significancia seleccionada).*
*   **Criterio**: Si $LI \leq \bar{x} \leq LS$, el conjunto de números **pasa** la prueba de media.

#### B. Prueba de Varianza (Validación de Dispersión)
Comprueba si la variabilidad de la muestra es estadísticamente equivalente a la varianza teórica de una uniforme estándar, la cual es $\sigma^2 = \frac{1}{12} \approx 0.08333$.
*   **Hipótesis**:
    $$H_0: \sigma^2 = \frac{1}{12}$$
    $$H_1: \sigma^2 \neq \frac{1}{12}$$
*   **Varianza Muestral ($s^2$)**:
    $$s^2 = \frac{1}{n-1} \sum_{i=1}^n (r_i - \bar{x})^2$$
*   **Límites de Aceptación**:
    $$LI = \frac{\chi^2_{1-\alpha/2, \ n-1}}{12(n-1)}$$
    $$LS = \frac{\chi^2_{\alpha/2, \ n-1}}{12(n-1)}$$
    *(Donde $\chi^2$ representa los valores críticos de la distribución Chi-cuadrada con $n-1$ grados de libertad).*
*   **Criterio**: Si $LI \leq s^2 \leq LS$, el conjunto de números **pasa** la prueba de varianza.

#### C. Prueba de Bondad de Ajuste Kolmogorov-Smirnov (KS)
Determina si la distribución de la muestra empírica difiere significativamente de la función de distribución acumulada uniforme teórica $F(x) = x$.
*   **Algoritmo**:
    1.  Ordenar la muestra de menor a mayor: $r_{(1)} \leq r_{(2)} \leq \dots \leq r_{(n)}$.
    2.  Calcular las diferencias máxima superior e inferior:
        $$D^+ = \max_{1 \leq i \leq n} \left( \frac{i}{n} - r_{(i)} \right)$$
        $$D^- = \max_{1 \leq i \leq n} \left( r_{(i)} - \frac{i-1}{n} \right)$$
    3.  Calcular el estadístico de contraste: $D = \max(D^+, D^-)$.
*   **Criterio**: Si $D < d_{\alpha, n}$ (valor crítico de la tabla KS para un tamaño de muestra $n$ y nivel de significancia $\alpha$), se concluye que los números siguen una **distribución uniforme**.

---

## 🛠️ Requisitos de Instalación y Ejecución en Local

Sigue los pasos a continuación para iniciar el backend y el frontend en tu máquina local.

### 🐍 Backend (Python + FastAPI)

1.  **Navega al directorio del backend**:
    ```bash
    cd backend
    ```
2.  **Crea el entorno virtual** (si no está creado):
    ```bash
    py -m venv venv
    ```
3.  **Activa el entorno virtual**:
    *   **En Windows (PowerShell)**:
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    *   **En Windows (CMD)**:
        ```cmd
        .\venv\Scripts\activate.bat
        ```
    *   **En macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```
4.  **Instala las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Inicia el servidor uvicorn en modo desarrollo**:
    ```bash
    uvicorn main:app --reload
    ```
    *Nota: El servidor correrá por defecto en `http://127.0.0.1:8000`. Puedes ingresar a `http://127.0.0.1:8000/docs` para ver y probar la API interactiva en **Swagger UI**.*

---

### ⚡ Frontend (Vite + React TS + Tailwind v4)

1.  **Navega al directorio del frontend**:
    ```bash
    cd frontend
    ```
2.  **Instala las dependencias de node**:
    ```bash
    npm install
    ```
3.  **Inicia el servidor de desarrollo Vite**:
    ```bash
    npm run dev
    ```
    *Nota: La aplicación web se levantará en el puerto indicado por Vite (típicamente `http://localhost:5173`). Abre ese enlace en tu navegador para ver la interfaz interactiva.*

---

## 📂 Estructura del Workspace

```text
SimuStat/
├── backend/            # Lógica en Python (FastAPI)
│   ├── venv/           # Entorno virtual de Python
│   └── requirements.txt# Dependencias de Python
├── frontend/           # Interfaz de usuario (React + TypeScript)
│   ├── src/
│   │   ├── App.tsx     # Componente principal con Dashboard de SimuStat
│   │   ├── index.css   # Estilos globales y Tailwind CSS v4
│   │   └── main.tsx    # Entrada de React
│   ├── package.json    # Dependencias de Node.js
│   └── vite.config.ts  # Configuración de Vite con TailwindCSS v4
└── README.md           # Información general del proyecto (este archivo)
```
