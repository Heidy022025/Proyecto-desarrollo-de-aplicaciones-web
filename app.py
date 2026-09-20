from flask import Flask, render_template, redirect, url_for, flash
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm

from models import Usuario

import mysql.connector
from decimal import Decimal


app = Flask(__name__)

# =========================================================
# CONFIGURACIÓN DE FLASK-WTF Y FLASK-LOGIN
# =========================================================

app.config["SECRET_KEY"] = "smartventas-clave-secreta-2026"

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Debe iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"


# =========================================================
# CONFIGURACIÓN DE MYSQL
# =========================================================

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "heidy_2006",
    "database": "smartventas"
}

def conectar_bd():
    return mysql.connector.connect(**DB_CONFIG)


# =========================================================
# CARGAR USUARIO PARA FLASK-LOGIN
# =========================================================

@login_manager.user_loader
def load_user(user_id):

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, usuario, password
        FROM usuarios
        WHERE id = %s
    """, (user_id,))

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        return Usuario(
            usuario["id"],
            usuario["usuario"],
            usuario["password"]
        )

    return None

# =========================================================
# REGISTRO DE USUARIOS
# =========================================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)

        # Comprobar si el usuario ya existe
        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario_existente = cursor.fetchone()

        if usuario_existente:
            cursor.close()
            conn.close()

            flash("El nombre de usuario ya está registrado.", "danger")

            return render_template(
                "registro.html",
                form=form
            )

        # Proteger la contraseña mediante hash
        password_hash = generate_password_hash(
            form.password.data
        )

        # Insertar usuario
        cursor.execute("""
            INSERT INTO usuarios
            (usuario, password)
            VALUES (%s, %s)
        """, (
            form.usuario.data,
            password_hash
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Usuario registrado correctamente. Ahora puede iniciar sesión.", "success")

        return redirect(url_for("login"))

    return render_template(
        "registro.html",
        form=form
    )
    
# =========================================================
# INICIO DE SESIÓN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario and check_password_hash(
            usuario["password"],
            form.password.data
        ):

            usuario_obj = Usuario(
                usuario["id"],
                usuario["usuario"],
                usuario["password"]
            )

            login_user(usuario_obj)

            flash(
                f"Bienvenido/a, {usuario['usuario']}.",
                "success"
            )

            return redirect(url_for("dashboard"))

        flash(
            "Usuario o contraseña incorrectos.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form
    )


# =========================================================
# CERRAR SESIÓN
# =========================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(url_for("login"))

# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        usuario=current_user.usuario
    )
    
    
# =========================================================
# PÁGINA DE INICIO
# =========================================================

@app.route("/")
def inicio():

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    # Obtener cantidad de productos
    cursor.execute("SELECT COUNT(*) AS total FROM productos")
    productos = cursor.fetchone()["total"]

    # Obtener cantidad de clientes
    cursor.execute("SELECT COUNT(*) AS total FROM clientes")
    clientes = cursor.fetchone()["total"]

    # Obtener cantidad de proveedores
    cursor.execute("SELECT COUNT(*) AS total FROM proveedores")
    proveedores = cursor.fetchone()["total"]

    # Obtener cantidad de facturas
    cursor.execute("SELECT COUNT(*) AS total FROM facturas")
    facturas = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    resumen = {
        "productos": productos,
        "clientes": clientes,
        "proveedores": proveedores,
        "facturas": facturas
    }

    nombre_sistema = "SmartVentas Solutions"

    return render_template(
        "index.html",
        nombre_sistema=nombre_sistema,
        resumen=resumen
    )


# =========================================================
# PRODUCTOS
# =========================================================

@app.route("/productos")
@login_required
def productos():

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.id_producto,
            p.nombre,
            p.precio,
            p.stock,
            p.id_proveedor,
            pr.nombre AS proveedor
        FROM productos p
        LEFT JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.id_producto DESC
    """)

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "productos.html",
        productos=productos
    )


@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def formulario_producto():

    form = ProductoForm()

    # =====================================================
    # CARGAR PROVEEDORES EN EL SELECT
    # =====================================================

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    form.id_proveedor.choices = [
        (proveedor["id_proveedor"], proveedor["nombre"])
        for proveedor in proveedores
    ]

    # =====================================================
    # GUARDAR PRODUCTO
    # =====================================================

    if form.validate_on_submit():

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos
            (nombre, precio, stock, id_proveedor)
            VALUES (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.precio.data,
            form.stock.data,
            form.id_proveedor.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )


# =========================================================
# CLIENTES
# =========================================================
@app.route("/clientes")
@login_required
def clientes():

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_cliente,
            nombre,
            cedula,
            telefono,
            correo
        FROM clientes
        ORDER BY id_cliente DESC
    """)

    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "clientes.html",
        clientes=clientes
    )


@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def formulario_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes
            (nombre, cedula, telefono, correo)
            VALUES (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.cedula.data,
            form.telefono.data,
            form.correo.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# =========================================================
# PROVEEDORES
# =========================================================

@app.route("/proveedores")
@login_required
def proveedores():

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre,
            telefono,
            correo
        FROM proveedores
        ORDER BY id_proveedor DESC
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def formulario_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO proveedores
            (nombre, telefono, correo)
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.telefono.data,
            form.correo.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# =========================================================
# FACTURACIÓN
# =========================================================

@app.route("/facturacion")
@login_required
def facturacion():

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            f.id_factura,
            f.id_cliente,
            c.nombre AS cliente,
            f.fecha,
            f.total
        FROM facturas f
        LEFT JOIN clientes c
            ON f.id_cliente = c.id_cliente
        ORDER BY f.id_factura DESC
    """)

    facturas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "facturacion.html",
        facturas=facturas
    )


@app.route("/facturacion/nueva", methods=["GET", "POST"])
@login_required
def formulario_facturacion():

    form = FacturacionForm()

    # =====================================================
    # CARGAR CLIENTES
    # =====================================================

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_cliente, nombre
        FROM clientes
        ORDER BY nombre
    """)

    clientes = cursor.fetchall()

    # =====================================================
    # CARGAR PRODUCTOS
    # =====================================================

    cursor.execute("""
        SELECT id_producto, nombre
        FROM productos
        ORDER BY nombre
    """)

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    # Cargar opciones en los formularios
    form.cliente.choices = [
        (cliente["id_cliente"], cliente["nombre"])
        for cliente in clientes
    ]

    form.producto.choices = [
        (producto["id_producto"], producto["nombre"])
        for producto in productos
    ]

    # =====================================================
    # GUARDAR FACTURA
    # =====================================================

    if form.validate_on_submit():

        # Calcular el total
        total = (
            Decimal(form.cantidad.data)
            * Decimal(form.precio.data)
        )

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO facturas
            (id_cliente, fecha, total)
            VALUES (%s, CURDATE(), %s)
        """, (
            form.cliente.data,
            total
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# =========================================================
# EJECUTAR APLICACIÓN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)