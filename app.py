# ==================================================
# IMPORTAR LIBRERÍAS
# ==================================================

# Flask permite crear la aplicación web
# render_template muestra páginas HTML
# request recibe datos de formularios
# redirect redirige a otra ruta
# session guarda información del usuario logueado
from flask import Flask, render_template, request, redirect, session

# ==================================================
# CONFIGURACIÓN DE LA APP
# ==================================================

# Creamos la aplicación Flask
app = Flask(__name__)

# Clave secreta para manejar sesiones
app.secret_key = "clave_secreta"

# ==================================================
# BASE DE DATOS TEMPORAL
# ==================================================

# Diccionario de usuarios
# Aquí se guardan los usuarios registrados
usuarios = {
    "admin@gmail.com": {
        "usuario": "Administrador",
        "nombres": "Admin",
        "apellidos": "Sistema",
        "correo": "admin@gmail.com",
        "edad": 30,
        "password": "1234",
        "rol": "admin"
    }
}

# Lista de pedidos
pedidos = []

# Lista de facturas
facturas = []

# Catálogo de flores con sus precios
flores = {
    "Rosa": 2,
    "Tulipan": 3,
    "Girasol": 4
}

# ==================================================
# FUNCIONES AUXILIARES
# ==================================================

def usuario_logueado():
    """
    Verifica si existe un usuario logueado en la sesión
    y si su correo sigue existiendo en el diccionario usuarios.
    """
    if "usuario" not in session or "correo" not in session:
        return False

    correo = session.get("correo")

    if correo not in usuarios:
        return False

    return True


def es_admin():
    """
    Verifica si el usuario actual es administrador.
    """
    if not usuario_logueado():
        return False

    correo = session.get("correo")
    return usuarios[correo]["rol"] == "admin"

# ==================================================
# RUTA PRINCIPAL
# ==================================================

@app.route("/")
def index():
    # Si no hay sesión, redirige al login
    if not usuario_logueado():
        return redirect("/login")

    # Si hay sesión, muestra el panel principal
    return render_template("index.html")

# ==================================================
# ACERCA DE
# ==================================================

@app.route("/about")
def about():
    # Protege la ruta
    if not usuario_logueado():
        return redirect("/login")

    return render_template("about.html")

# ==================================================
# LOGIN
# ==================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    # Variable para mostrar mensajes de error en el formulario
    error = None

    # Si el formulario fue enviado
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]

        # Verifica si el usuario existe y la contraseña coincide
        if correo in usuarios and usuarios[correo]["password"] == password:
            session["usuario"] = usuarios[correo]["usuario"]
            session["correo"] = usuarios[correo]["correo"]
            session["rol"] = usuarios[correo]["rol"]

            return redirect("/")

        # Si falla, no lo saca del login; solo muestra error
        error = "Credenciales incorrectas"

    return render_template("login.html", error=error)

# ==================================================
# REGISTRO
# ==================================================

@app.route("/registro", methods=["GET", "POST"])
def registro():
    # Variable para mostrar mensajes de error
    error = None

    # Si el formulario fue enviado
    if request.method == "POST":
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        correo = request.form["correo"]
        password = request.form["password"]

        # Verifica si el correo ya existe
        if correo in usuarios:
            error = "Usuario ya registrado"

        else:
            # Si no existe, crea el nuevo usuario como cliente
            usuarios[correo] = {
                "usuario": nombres,
                "nombres": nombres,
                "apellidos": apellidos,
                "correo": correo,
                "edad": 20,
                "password": password,
                "rol": "cliente"
            }

            # Después del registro, redirige al login
            return redirect("/login")

    return render_template("registro.html", error=error)

# ==================================================
# CERRAR SESIÓN
# ==================================================

@app.route("/logout")
def logout():
    # Borra toda la sesión actual
    session.clear()

    # Regresa al login
    return redirect("/login")

# ==================================================
# CLIENTES
# ==================================================

@app.route("/clientes")
def clientes():
    # Si no hay sesión, manda al login
    if not usuario_logueado():
        session.clear()
        return redirect("/login")

    # Si es admin, ve todos los clientes
    if es_admin():
        return render_template("clientes_admin.html", usuarios=usuarios.values())

    # Si es cliente, ve solo sus propios datos
    correo = session.get("correo")
    cliente = usuarios.get(correo)

    # Si por alguna razón no existe, limpiar sesión
    if not cliente:
        session.clear()
        return redirect("/login")

    return render_template("clientes.html", cliente=cliente)

# ==================================================
# VENTA / COMPRA
# ==================================================

@app.route("/venta", methods=["GET", "POST"])
def venta():
    # Si no hay sesión, manda al login
    if not usuario_logueado():
        return redirect("/login")

    # El administrador no puede comprar
    if es_admin():
        return redirect("/admin")

    # Si el cliente envía el formulario
    if request.method == "POST":
        flor = request.form["flor"]
        cantidad = int(request.form["cantidad"])

        # Validación básica
        if flor not in flores or cantidad <= 0:
            return "Datos inválidos"

        # Precio de la flor seleccionada
        precio = flores[flor]

        # Cálculo del subtotal
        subtotal = precio * cantidad

        # Crear pedido
        pedido = {
            "codigo": len(pedidos) + 1,
            "correo": session["correo"],
            "flor": flor,
            "cantidad": cantidad,
            "precio": precio,
            "subtotal": subtotal,
            "total": subtotal
        }

        # Guardar pedido
        pedidos.append(pedido)

        # Crear factura
        factura = {
            "codigo": len(facturas) + 1,
            "correo": session["correo"],
            "flor": flor,
            "cantidad": cantidad,
            "precio": precio,
            "subtotal": subtotal,
            "total": subtotal
        }

        # Guardar factura
        facturas.append(factura)

        # Después de comprar, manda a facturas
        return redirect("/mis-facturas")

    return render_template("venta.html", flores=flores)

# ==================================================
# MIS COMPRAS
# ==================================================

@app.route("/mis-compras")
def mis_compras():
    # Si no hay sesión, manda al login
    if not usuario_logueado():
        return redirect("/login")

    # El admin no entra aquí
    if es_admin():
        return redirect("/admin")

    # Filtra solo las compras del usuario actual
    correo = session["correo"]
    compras = [p for p in pedidos if p["correo"] == correo]

    return render_template("mis_compras.html", compras=compras)

# ==================================================
# MIS PEDIDOS
# ==================================================

@app.route("/mis-pedidos")
def mis_pedidos():
    # Si no hay sesión, manda al login
    if not usuario_logueado():
        return redirect("/login")

    # Si es admin, ve todos los pedidos
    if es_admin():
        return render_template("pedidos_admin.html", pedidos=pedidos)

    # Si es cliente, ve solo sus pedidos
    correo = session["correo"]
    mis = [p for p in pedidos if p["correo"] == correo]

    return render_template("mis_pedidos.html", pedidos=mis)

# ==================================================
# MIS FACTURAS
# ==================================================

@app.route("/mis-facturas")
def mis_facturas():
    # Si no hay sesión, manda al login
    if not usuario_logueado():
        return redirect("/login")

    # Si es admin, ve todas las facturas
    if es_admin():
        return render_template("facturas_admin.html", facturas=facturas)

    # Si es cliente, ve solo sus facturas
    correo = session["correo"]
    mis = [f for f in facturas if f["correo"] == correo]

    return render_template("mis_facturas.html", facturas=mis)

# ==================================================
# PANEL ADMIN
# ==================================================

@app.route("/admin")
def admin():
    # Si no hay sesión, manda al login
    if not usuario_logueado():
        return redirect("/login")

    # Solo el admin puede entrar
    if not es_admin():
        return "Acceso denegado"

    return render_template(
        "admin.html",
        usuarios=usuarios.values(),
        pedidos=pedidos,
        facturas=facturas
    )

# ==================================================
# EJECUTAR SERVIDOR
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)