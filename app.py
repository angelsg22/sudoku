# =============================================================================
# app.py — Servidor web con Flask
# =============================================================================
#
# Flask es un "micro-framework" web para Python. Hace dos cosas principales:
#   1. Sirve páginas web (como el index.html)
#   2. Crea una API: responde a peticiones del navegador con datos JSON
#
# ¿Qué es una API? Es como un "menú de restaurante":
#   - El navegador (cliente) hace un pedido: "dame un tablero nuevo"
#   - Flask (servidor) lo procesa y devuelve los datos
#   - El navegador los usa para pintar la pantalla
#
# Rutas disponibles:
#   GET  /                  → sirve la página HTML principal
#   POST /api/nuevo-juego   → genera y devuelve un tablero nuevo
#   POST /api/comprobar     → valida la respuesta del usuario
#   POST /api/pista         → devuelve una celda resuelta como ayuda
#   GET  /api/solucion      → devuelve el tablero completo resuelto
# =============================================================================

from flask import Flask, render_template, request, jsonify, session
import sudoku  # Importamos nuestro archivo sudoku.py con toda la lógica
import os      # Para generar una clave secreta de seguridad

# =============================================================================
# Creamos la aplicación Flask
# =============================================================================
# __name__ le dice a Flask en qué archivo estamos.
# Flask lo usa para encontrar la carpeta "templates" donde está el HTML.
app = Flask(__name__)

# La clave secreta es necesaria para usar "session" (memoria entre peticiones)
# os.urandom(24) genera 24 bytes aleatorios → muy difícil de adivinar
app.secret_key = os.urandom(24)


# =============================================================================
# RUTA: / (página principal)
# =============================================================================
# Cuando el usuario abre http://localhost:5000, Flask devuelve el HTML.
# render_template busca el archivo en la carpeta "templates/".
# =============================================================================
@app.route("/")
def pagina_principal():
    return render_template("index.html")


# =============================================================================
# RUTA: /api/nuevo-juego
# =============================================================================
# El navegador envía: {"dificultad": "facil" | "medio" | "dificil"}
# Flask responde con: {"puzzle": [[...]], "dificultad": "medio"}
#
# ¿Por qué POST y no GET?
# GET es para pedir información (como cargar una página).
# POST es para enviar datos al servidor (como enviar un formulario).
# Aquí enviamos la dificultad elegida → usamos POST.
# =============================================================================
@app.route("/api/nuevo-juego", methods=["POST"])
def nuevo_juego():
    # request.json contiene los datos que envió el navegador en formato JSON
    datos = request.json
    dificultad = datos.get("dificultad", "medio")  # Si no viene, usamos "medio"

    # Generamos el puzzle usando nuestra lógica de sudoku.py
    resultado = sudoku.generar_puzzle(dificultad)

    # Guardamos la solución en la "session" (memoria del servidor para este usuario)
    # IMPORTANTE: La sesión de Flask guarda datos entre peticiones del mismo usuario.
    # Así no tenemos que reenviar la solución al navegador (el usuario no la vería).
    session["solucion"] = resultado["solucion"]

    # Respondemos al navegador con el puzzle (sin la solución)
    # jsonify convierte un diccionario Python en formato JSON
    return jsonify({
        "puzzle": resultado["puzzle"],
        "dificultad": dificultad
    })


# =============================================================================
# RUTA: /api/comprobar
# =============================================================================
# El navegador envía: {"respuesta": [[...matriz 9x9 con los números del usuario...]]}
# Flask responde con: {"correcto": true/false, "errores": [[fila,col],...], "completo": true/false}
# =============================================================================
@app.route("/api/comprobar", methods=["POST"])
def comprobar():
    # Recuperamos la solución guardada en la sesión
    solucion = session.get("solucion")

    # Si no hay sesión activa (por ejemplo, recargó la página sin jugar)
    if solucion is None:
        return jsonify({"error": "No hay ningún juego activo"}), 400

    # Obtenemos la respuesta del usuario
    datos = request.json
    respuesta_usuario = datos.get("respuesta")

    # Validamos usando nuestra función de sudoku.py
    resultado = sudoku.validar_solucion(respuesta_usuario, solucion)

    return jsonify(resultado)


# =============================================================================
# RUTA: /api/pista
# =============================================================================
# El navegador envía: {"respuesta": [[...estado actual del tablero del usuario...]]}
# Flask responde con: {"fila": 3, "col": 5, "valor": 7}
# =============================================================================
@app.route("/api/pista", methods=["POST"])
def pista():
    solucion = session.get("solucion")

    if solucion is None:
        return jsonify({"error": "No hay ningún juego activo"}), 400

    datos = request.json
    respuesta_usuario = datos.get("respuesta")

    # Pedimos una pista a nuestra función de sudoku.py
    pista_data = sudoku.obtener_pista(respuesta_usuario, solucion)

    if pista_data is None:
        return jsonify({"mensaje": "¡El tablero ya está resuelto!"})

    return jsonify(pista_data)


# =============================================================================
# RUTA: /api/solucion
# =============================================================================
# El usuario pulsa "Revelar solución" y el navegador pide la solución completa.
# Flask la devuelve desde la sesión.
# =============================================================================
@app.route("/api/solucion", methods=["GET"])
def ver_solucion():
    solucion = session.get("solucion")

    if solucion is None:
        return jsonify({"error": "No hay ningún juego activo"}), 400

    return jsonify({"solucion": solucion})


# =============================================================================
# RUTA: /api/candidatos
# =============================================================================
# El modo apunte del frontend llama a esta ruta para saber qué números son
# posibles en cada celda vacía según el estado actual del tablero.
#
# El navegador envía: {"tablero": [[...matriz 9x9 con estado actual...]]}
# Flask responde con: {"candidatos": {"fila-col": [numeros], ...}}
# =============================================================================
@app.route("/api/candidatos", methods=["POST"])
def candidatos():
    datos = request.json
    tablero = datos.get("tablero")

    # Calculamos los candidatos usando la lógica de sudoku.py
    resultado = sudoku.calcular_candidatos(tablero)

    return jsonify({"candidatos": resultado})


# =============================================================================
# Punto de entrada del programa
# =============================================================================
# Este bloque se ejecuta cuando corres: python app.py
# debug=True significa que Flask se recarga automáticamente si cambias el código
# (muy útil mientras desarrollas, ¡desactívalo en producción!)
# =============================================================================
if __name__ == "__main__":
    print("🎮 Servidor Sudoku iniciado en http://localhost:5000")
    app.run(debug=True)
