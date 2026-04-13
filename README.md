# 🎯 Sudoku Web App

Una aplicación web de Sudoku hecha con Python (Flask) y HTML/CSS/JavaScript.

---

## ¿Qué hay en cada archivo?

```
sudoku-app/
├── app.py              → Servidor web (Flask): gestiona las peticiones del navegador
├── sudoku.py           → Lógica del juego: generar, resolver y validar tableros
├── requirements.txt    → Lista de librerías Python necesarias
├── README.md           → Este archivo
└── templates/
    └── index.html      → La página web completa (HTML + CSS + JavaScript)
```

---

## Instalación paso a paso

### 1. Requisitos previos

Necesitas tener **Python 3.8 o superior** instalado.

Compruébalo en la terminal:
```bash
python --version
```

Si no lo tienes, descárgalo en: https://www.python.org/downloads/

---

### 2. Descarga o crea la carpeta del proyecto

Si clonaste el repositorio:
```bash
cd sudoku-app
```

Si creaste los archivos manualmente, entra a la carpeta donde están.

---

### 3. Crea un entorno virtual (recomendado)

Un entorno virtual es una "caja" donde instalas las librerías sin mezclarlas
con otras que tengas en el ordenador.

```bash
# Crea el entorno virtual (solo la primera vez)
python -m venv venv

# Actívalo en Windows
venv\Scripts\activate

# Actívalo en Mac/Linux
source venv/bin/activate
```

Sabrás que está activo porque el nombre `(venv)` aparecerá al principio del prompt.

---

### 4. Instala las dependencias

```bash
pip install -r requirements.txt
```

Esto instalará Flask automáticamente.

---

### 5. Ejecuta el servidor

```bash
python app.py
```

Deberías ver algo como:
```
🎮 Servidor Sudoku iniciado en http://localhost:5000
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

### 6. Abre el juego en el navegador

Abre tu navegador (Chrome, Firefox, Edge...) y ve a:

```
http://localhost:5000
```

¡Ya puedes jugar!

---

## Cómo jugar

1. **Elige la dificultad** en el selector (Fácil / Medio / Difícil)
2. **Pulsa "Nuevo juego"** para generar un tablero
3. **Haz clic en una celda vacía** para seleccionarla
4. **Escribe un número** (teclado físico o teclado en pantalla)
5. **Pulsa "Comprobar"** para ver si tu solución es correcta
6. Si te atascas, usa **"Pedir pista"** (tienes 3 por partida)
7. Como último recurso, **"Revelar solución"** muestra la respuesta completa

---

## Funcionalidades

| Función | Descripción |
|---|---|
| Nuevo juego | Genera un tablero único cada vez |
| 3 dificultades | Fácil (35 vacías), Medio (45), Difícil (55) |
| Validación | Marca en rojo las celdas incorrectas |
| Pistas | Hasta 3 por partida |
| Revelar solución | Muestra el tablero completo |
| Temporizador | Cronómetro visible mientras juegas |
| Mejor tiempo | Guardado en el navegador por dificultad |
| Teclado numérico | Funciona en pantalla y con el teclado físico |
| Responsive | Se adapta a móvil y escritorio |

---

## Para parar el servidor

En la terminal donde está corriendo Flask, pulsa:
```
Ctrl + C
```

---

## Solución de problemas

**El navegador muestra "Error al conectar con el servidor"**
→ Comprueba que Flask está ejecutándose (`python app.py`) y no hubo errores.

**`pip` no se reconoce como comando**
→ Prueba con `pip3` en lugar de `pip`.

**La página no carga en http://localhost:5000**
→ Prueba con http://127.0.0.1:5000 (son equivalentes).

**`ModuleNotFoundError: No module named 'flask'`**
→ Asegúrate de haber activado el entorno virtual y haber ejecutado `pip install -r requirements.txt`.
