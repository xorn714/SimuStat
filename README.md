# SimuStat 📊⚙️

**SimuStat** es una plataforma interactiva web diseñada para la generación y validación estadística de números pseudoaleatorios. El proyecto implementa algoritmos de generación de variables uniformes, aplica pruebas formales de validación estadística para certificar la calidad de las secuencias generadas y permite transformar dichas secuencias en variables aleatorias **continuas** (Uniforme, Exponencial, Normal y Weibull) o **discretas** (Bernoulli, Binomial, Poisson, Geométrica, Binomial Negativa, Hipergeométrica y Uniforme Discreta), facilitando la comprensión y el análisis de sistemas de simulación.

---

## 🚀 Arquitectura del Proyecto

El sistema está dividido en una arquitectura desacoplada de Cliente-Servidor (Frontend y Backend) que se comunican mediante una API REST:

*   **Backend**: Desarrollado en **Python** utilizando **FastAPI**. Sigue una arquitectura hexagonal/por capas (dominio, servicios y adaptadores) que mantiene la lógica de negocio desacoplada de los detalles de infraestructura. Ofrece una API rápida, validación automática de datos con **Pydantic** y documentación interactiva integrada mediante **Swagger UI**. Incluye una suite de pruebas con **pytest** (unitarias e integración).
*   **Frontend**: Desarrollado en **React** con **TypeScript** utilizando **Vite** para un desarrollo ultrarrápido y **TailwindCSS v4** para un diseño moderno, interactivo y premium. Las visualizaciones utilizan **Recharts** y **Lucide Icons**. El linting se realiza con **oxlint**.

### 🗂️ Capas del Backend

*   **`domain/`**: Contiene los algoritmos de generación, las pruebas estadísticas y el cálculo de estadísticos continuos y discretos (lógica de negocio pura).
*   **`services/`**: Orquesta el flujo completo de la simulación (`SimulationService`).
*   **`adapter/`**: Define los esquemas Pydantic, las rutas API y el enrutador v1.

---

## 🧠 Modelos Matemáticos y Algoritmos

### 1. Generadores de Números Pseudoaleatorios (Distribución Uniforme)
El proyecto genera secuencias de números pseudoaleatorios en el intervalo $[0, 1)$ mediante tres metodologías:

*   **Método Congruencial**:
    *   *Lineal (LCG)*: Define la relación recursiva:
        $$x_{i+1} = (a \cdot x_i + c) \pmod m$$
    *   *Multiplicativo (MCG)*: Simplifica la relación omitiendo la constante aditiva $c$:
        $$x_{i+1} = (a \cdot x_i) \pmod m$$
    *   Para ambos, el número pseudoaleatorio normalizado es $r_i = \frac{x_i}{m-1}$.
*   **Método de Cuadrados Medios (Mid-Square)**:
    *   A partir de una semilla $x_0$ de $d$ dígitos (donde $d$ es par), se eleva al cuadrado $x_0^2$.
    *   Se extraen los $d$ dígitos centrales de $x_0^2$ para obtener el siguiente valor de la secuencia $x_1$.
    *   Se normaliza como $r_1 = \frac{x_1}{10^d}$. Se repite recursivamente.

### 2. Generación de Variables Aleatorias Continuas

Partiendo de la secuencia base $U(0,1)$, la plataforma permite transformarla (método de la transformada inversa y Box-Muller) en las siguientes distribuciones continuas:

*   **Uniforme Continua** $U(a, b)$: $X = a + (b - a) \cdot U$
*   **Exponencial** $\text{Exp}(\beta)$: $X = -\beta \ln(1 - U)$ (parametrizada por su tiempo medio/escala $\beta$)
*   **Normal** $N(\mu, \sigma^2)$: mediante la transformación de **Box-Muller**.
*   **Weibull** $\text{Weibull}(\alpha, \beta)$: $X = \alpha \cdot (-\ln(1 - U))^{1/\beta}$

Para cada distribución se calculan los estadísticos empíricos vs teóricos (media y varianza) y se genera un histograma de frecuencias con la curva de densidad teórica superpuesta.

### 3. Generación de Variables Aleatorias Discretas

Partiendo de la misma secuencia base $U(0,1)$, la plataforma permite generar variables aleatorias discretas mediante el **método de la transformada inversa** sobre la función de masa de probabilidad $P(X = k)$:

*   **Bernoulli** $\text{Bernoulli}(p)$: $X = 1$ si $U < p$, en caso contrario $X = 0$.
*   **Binomial** $\text{Binomial}(n, p)$: suma de $n$ variables Bernoulli independientes (consume $n$ números uniformes por observación).
*   **Poisson** $\text{Poisson}(\lambda)$: transformada inversa usando la relación recursiva $P(X = k) = P(X = k-1) \cdot \frac{\lambda}{k}$.
*   **Geométrica** $\text{Geo}(p)$: $X = \left\lfloor \frac{\ln(1 - U)}{\ln(1 - p)} \right\rfloor$ (rango $\{0, 1, 2, \dots\}$ representando el número de fracasos antes del primer éxito).
*   **Binomial Negativa** $\text{NB}(r, p)$: suma de $r$ variables geométricas independientes.
*   **Hipergeométrica** $\text{HG}(N, K, n)$: muestreo secuencial sin reemplazo.
*   **Uniforme Discreta** $\text{UD}(i, j)$: $X = i + \lfloor U \cdot (j - i + 1) \rfloor$ (rango $\{i, \dots, j\}$).

Para cada distribución se calculan los estadísticos empíricos vs teóricos (media y varianza), la tabla de frecuencias y un histograma de barras comparando la frecuencia relativa empírica con la PMF teórica.

---

### 4. Pruebas Estadísticas de Validación
Para certificar que una secuencia generada $R = \{r_1, r_2, \dots, r_n\}$ se comporta efectivamente como una distribución uniforme $U(0, 1)$, se aplican cuatro pruebas fundamentales:

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

#### D. Prueba de Rachas (Runs Test) — Independencia
Verifica la independencia de la secuencia analizando el número de rachas (corridas) de valores por encima y por debajo de la media teórica $0.5$.
*   **Estadístico de prueba (Z)**:
    $$\mu_R = \frac{2 n_1 n_2}{n} + 1, \qquad \sigma_R^2 = \frac{2 n_1 n_2 (2 n_1 n_2 - n)}{n^2 (n - 1)}$$
    $$Z = \frac{R - \mu_R}{\sigma_R}$$
    *(Donde $n_1$ y $n_2$ son la cantidad de valores $\geq 0.5$ y $< 0.5$ respectivamente, y $R$ el número de rachas observado).*
*   **Límites de Aceptación**: $LI = -Z_{\alpha/2}$ y $LS = Z_{\alpha/2}$.
*   **Criterio**: Si $LI \leq Z \leq LS$, el conjunto de números **pasa** la prueba de rachas (independencia).

---

## 🛠️ Requisitos Previos

*   **Python** 3.10 o superior (recomendado 3.12).
*   **Node.js** 18 o superior y **npm**.
*   **Git** (opcional).

---

## ⚙️ Instalación y Ejecución en Local

> **Nota:** Todos los pasos deben ejecutarse desde la raíz del repositorio `SimuStat/`. Primero se levanta el backend y luego el frontend.

### 🐧 Instalación en Linux / macOS

#### 🐍 Backend (Python + FastAPI)

1.  **Navega al directorio del backend**:
    ```bash
    cd backend
    ```
2.  **Crea el entorno virtual** (si no está creado):
    ```bash
    python3 -m venv venv
    ```
3.  **Activa el entorno virtual**:
    ```bash
    source venv/bin/activate
    ```
4.  **Instala las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Inicia el servidor uvicorn en modo desarrollo**:
    ```bash
    uvicorn app.main:app --reload
    ```
    *Nota: El servidor correrá por defecto en `http://127.0.0.1:8000`. Puedes ingresar a `http://127.0.0.1:8000/docs` para ver y probar la API interactiva en **Swagger UI**.*

#### ⚡ Frontend (Vite + React TS + Tailwind v4)

1.  **Abre una nueva terminal y navega al directorio del frontend**:
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

### 🪟 Instalación en Windows

#### 🐍 Backend (Python + FastAPI)

1.  **Navega al directorio del backend**:
    ```powershell
    cd backend
    ```
2.  **Crea el entorno virtual** (si no está creado):
    ```powershell
    python -m venv venv
    ```
3.  **Activa el entorno virtual** (elige según tu terminal):
    *   **PowerShell**:
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
        *(Si PowerShell bloquea la ejecución de scripts, ejecuta primero: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*
    *   **CMD (Símbolo del sistema)**:
        ```cmd
        .\venv\Scripts\activate.bat
        ```
4.  **Instala las dependencias**:
    ```powershell
    pip install -r requirements.txt
    ```
5.  **Inicia el servidor uvicorn en modo desarrollo**:
    ```powershell
    uvicorn app.main:app --reload
    ```
    *Nota: El servidor correrá por defecto en `http://127.0.0.1:8000`. Puedes ingresar a `http://127.0.0.1:8000/docs` para ver y probar la API interactiva en **Swagger UI**.*

#### ⚡ Frontend (Vite + React TS + Tailwind v4)

1.  **Abre una nueva terminal y navega al directorio del frontend**:
    ```powershell
    cd frontend
    ```
2.  **Instala las dependencias de node**:
    ```powershell
    npm install
    ```
3.  **Inicia el servidor de desarrollo Vite**:
    ```powershell
    npm run dev
    ```
    *Nota: La aplicación web se levantará en el puerto indicado por Vite (típicamente `http://localhost:5173`). Abre ese enlace en tu navegador para ver la interfaz interactiva.*

---

## 🧪 Pruebas

### Backend (pytest)

```bash
cd backend
source venv/bin/activate   # Windows: .\venv\Scripts\Activate.ps1
pytest
```

### Frontend (oxlint)

```bash
cd frontend
npm run lint
```

---

## ☁️ Despliegue en Producción (Vercel)

El proyecto incluye un archivo `vercel.json` que define dos servicios:

*   **Frontend**: construido con Vite (raíz `frontend/`).
*   **Backend**: FastAPI con entrypoint en `backend/api/index.py`.

Las peticiones a `/api/*` se enrutan automáticamente al backend y el resto a la aplicación web. En producción, el frontend utiliza rutas relativas (`/api/v1`) por lo que no requiere configuración adicional de CORS.

---

## 📂 Estructura del Workspace

```text
SimuStat/
├── vercel.json              # Configuración de despliegue en Vercel
├── backend/                 # Lógica en Python (FastAPI)
│   ├── api/
│   │   └── index.py         # Entrypoint para Vercel
│   ├── app/
│   │   ├── main.py          # Instancia de FastAPI, CORS y router principal
│   │   ├── domain/          # Lógica de negocio pura
│   │   │   ├── exceptions.py           # Jerarquía de excepciones del dominio
│   │   │   ├── generators/             # Generadores de números pseudoaleatorios
│   │   │   │   ├── base.py             # Clase abstracta Generator y validaciones
│   │   │   │   ├── congruential.py     # LCG, MCG y Mid-Square
│   │   │   │   ├── continuous.py       # Distribuciones continuas (Uniforme, Exp, Normal, Weibull)
│   │   │   │   └── discrete.py         # Distribuciones discretas (Bernoulli, Binomial, Poisson, etc.)
│   │   │   ├── validators/             # Pruebas estadísticas (media, varianza, KS y rachas)
│   │   │   └── stats/
│   │   │       ├── continuous_stats.py # Estadísticos empíricos/teóricos e histograma continuo
│   │   │       └── discret_stats.py    # Estadísticos empíricos/teóricos e histograma discreto
│   │   ├── services/
│   │   │   └── simulation_service.py  # Orquestación de la simulación
│   │   └── adapter/
│   │       ├── api/
│   │       │   ├── schema.py   # Esquemas Pydantic (request/response)
│   │       │   └── v1/
│   │       │       ├── router.py
│   │       │       └── endpoint/sim_routes.py  # POST /generate-sequence
│   ├── tests/                # Pruebas con pytest
│   │   ├── unit/             # Pruebas unitarias de dominio y servicio
│   │   └── integration/      # Pruebas de integración de la API
│   ├── venv/                 # Entorno virtual de Python
│   └── requirements.txt      # Dependencias de Python
├── frontend/                 # Interfaz de usuario (React + TypeScript)
│   ├── src/
│   │   ├── App.tsx           # Componente principal con Dashboard de SimuStat
│   │   ├── index.css         # Estilos globales y Tailwind CSS v4
│   │   └── main.tsx          # Entrada de React
│   │   ├── components/
│   │   │   └── layout/       # Navbar y Sidebar (configuración del generador)
│   │   ├── features/
│   │   │   ├── dashboard/    # Dashboard, gráficas y tarjetas de pruebas
│   │   │   │   ├── components/  # Tablas, histogramas y estadísticos de variables continuas y discretas
│   │   │   │   ├── Grafica.tsx, DistribucionUniforme.tsx
│   │   │   │   ├── TestMedia.tsx, TestVarianza.tsx, TestKS.tsx, TestRacha.tsx
│   │   │   │   ├── discretePmf.ts, formatTestStatistic.ts
│   │   │   │   └── types.ts
│   │   │   ├── generators/   # Lógica de generadores (frontend)
│   │   │   └── validation/   # Lógica de validación (frontend)
│   │   └── services/
│   │       └── api.ts        # Cliente HTTP para consumir el backend
│   ├── package.json          # Dependencias de Node.js
│   └── vite.config.ts        # Configuración de Vite con TailwindCSS v4
└── README.md                 # Información general del proyecto (este archivo)
```

---

## 🧩 Endpoints de la API

| Método | Ruta                    | Descripción                                                                 |
|--------|-------------------------|-----------------------------------------------------------------------------|
| `GET`  | `/`                     | Mensaje de bienvenida.                                                      |
| `GET`  | `/docs`                 | Documentación interactiva (Swagger UI).                                     |
| `POST` | `/api/v1/generate-sequence` | Genera una secuencia (LCG, MCG o Mid-Square), aplica las 4 pruebas estadísticas y opcionalmente genera una variable aleatoria (continua o discreta) con sus estadísticos e histograma. |
