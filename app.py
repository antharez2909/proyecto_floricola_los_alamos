from flask import Flask

app = Flask(__name__)

# =========================
# RUTA PRINCIPAL
# =========================
@app.route("/")
def home():
    return "Bienvenido a Florícola Los Álamos – Sistema Empresarial de Gestión"

# =========================
# VENTA NACIONAL (CLIENTES, FLORES, PEDIDOS)
# =========================
@app.route("/cliente/<nombre>")
def cliente(nombre):
    return f"Bienvenido {nombre}, tu pedido en Florícola Los Álamos está en proceso."

@app.route("/clientes")
def clientes():
    return "Listado de clientes registrados en Florícola Los Álamos."

@app.route("/flor/<nombre>")
def flor(nombre):
    return f"Flor: {nombre} – disponible para despacho."

@app.route("/flores")
def flores():
    return "Catálogo general de flores de Florícola Los Álamos."

@app.route("/pedido/<codigo>")
def pedido(codigo):
    return f"Pedido #{codigo} – en preparación para envío."

@app.route("/pedidos")
def pedidos():
    return "Listado de pedidos activos."

# =========================
# INVENTARIO Y LOGÍSTICA
# =========================
@app.route("/item/<codigo>")
def item(codigo):
    return f"Ítem {codigo} – stock disponible."

@app.route("/inventario")
def inventario():
    return "Inventario general de Florícola Los Álamos."

@app.route("/envio/<codigo>")
def envio(codigo):
    return f"Envío {codigo} – en ruta para entrega."

@app.route("/envios")
def envios():
    return "Historial de envíos realizados."

@app.route("/ruta/<codigo>")
def ruta(codigo):
    return f"Ruta logística {codigo}."

@app.route("/flota")
def flota():
    return "Flota de transporte."

@app.route("/transportistas")
def transportistas():
    return "Listado de transportistas."

# =========================
# PRODUCCIÓN
# =========================
@app.route("/lote/<codigo>")
def lote(codigo):
    return f"Lote {codigo} – en producción."

@app.route("/siembra/nueva")
def siembra():
    return "Registro de nueva siembra."

@app.route("/cosecha/<fecha>")
def cosecha(fecha):
    return f"Cosecha del día {fecha}."

@app.route("/produccion/diaria")
def produccion():
    return "Resumen diario de producción."

# =========================
# TALENTO HUMANO
# =========================
@app.route("/empleado/<id>")
def empleado(id):
    return f"Empleado #{id} – ficha laboral."

@app.route("/empleados")
def empleados():
    return "Listado de empleados."

@app.route("/nomina")
def nomina():
    return "Gestión de nómina."

@app.route("/turnos")
def turnos():
    return "Turnos de trabajo."

# =========================
# FINANZAS
# =========================
@app.route("/factura/<numero>")
def factura(numero):
    return f"Factura #{numero} – emitida correctamente."

@app.route("/facturas")
def facturas():
    return "Listado de facturas."

@app.route("/costos")
def costos():
    return "Costos de producción."

@app.route("/utilidades")
def utilidades():
    return "Reporte de utilidades."

@app.route("/proveedores")
def proveedores():
    return "Listado de proveedores."

@app.route("/pagos")
def pagos():
    return "Registro de pagos."

# =========================
# ADMINISTRACIÓN
# =========================
@app.route("/admin")
def admin():
    return "Panel de administración – Florícola Los Álamos."

@app.route("/admin/reportes")
def reportes():
    return "Reportes de ventas y producción."

# =========================
# INFORMACIÓN
# =========================
@app.route("/contacto")
def contacto():
    return "Contacto: floricola.losalamos@email.com"

@app.route("/sobre-nosotros")
def nosotros():
    return "Floricola Los Álamos – Calidad en flores desde Ecuador."

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    app.run(debug=True)

