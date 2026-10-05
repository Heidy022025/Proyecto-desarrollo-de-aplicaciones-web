from flask import Flask, render_template, redirect, url_for, flash, request
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

import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# =========================================================
# CONFIGURACIÓN DE FLASK-WTF Y FLASK-LOGIN
# =========================================================

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Debe iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"


# =========================================================
# CONFIGURACIÓN DE MYSQL
# =========================================================

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "dbname": os.getenv("POSTGRES_DATABASE", "smartventas")
}

def conectar_bd():
    return psycopg2.connect(**DB_CONFIG)


# =========================================================
# CARGAR USUARIO PARA FLASK-LOGIN
# =========================================================

@login_manager.user_loader
def load_user(user_id):

    conn = conectar_bd()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

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
        cursor = conn.cursor(cursor_factory=RealDictCursor)

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
        cursor = conn.cursor(cursor_factory=RealDictCursor)

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
    cursor = conn.cursor(cursor_factory=RealDictCursor)

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
    cursor = conn.cursor(cursor_factory=RealDictCursor)

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



# =========================================================
# EDITAR PRODUCTO
# =========================================================

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):

    # -----------------------------------------------------
    # Conectar a PostgreSQL
    # -----------------------------------------------------

    conn = conectar_bd()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # -----------------------------------------------------
    # Buscar producto
    # -----------------------------------------------------

    cursor.execute("""
        SELECT
            id_producto,
            nombre,
            precio,
            stock,
            id_proveedor
        FROM productos
        WHERE id_producto = %s
    """, (id,))

    producto = cursor.fetchone()

    # -----------------------------------------------------
    # Verificar si existe
    # -----------------------------------------------------

    if producto is None:

        cursor.close()
        conn.close()

        flash(
            "El producto no existe.",
            "danger"
        )

        return redirect(url_for("productos"))

    # -----------------------------------------------------
    # Obtener proveedores
    # -----------------------------------------------------

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    # -----------------------------------------------------
    # Crear formulario
    # -----------------------------------------------------

    form = ProductoForm()

    # Cargar proveedores en el campo SELECT
    form.id_proveedor.choices = [
        (
            proveedor["id_proveedor"],
            proveedor["nombre"]
        )
        for proveedor in proveedores
    ]

    # -----------------------------------------------------
    # GET: cargar datos actuales del producto
    # -----------------------------------------------------

    if request.method == "GET":

        form.nombre.data = producto["nombre"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]
        form.id_proveedor.data = producto["id_proveedor"]

    # -----------------------------------------------------
    # POST: guardar cambios
    # -----------------------------------------------------

    if form.validate_on_submit():

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE productos
            SET
                nombre = %s,
                precio = %s,
                stock = %s,
                id_proveedor = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            form.precio.data,
            form.stock.data,
            form.id_proveedor.data,
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Producto actualizado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    # -----------------------------------------------------
    # Mostrar formulario
    # -----------------------------------------------------

    return render_template(
        "formulario_producto.html",
        form=form,
        titulo="Editar producto"
    )

# =========================================================
# ELIMINAR PRODUCTO
# =========================================================

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):

    conn = conectar_bd()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            DELETE FROM productos
            WHERE id_producto = %s
        """, (id,))

        conn.commit()

        flash(
            "Producto eliminado correctamente.",
            "success"
        )

    except Exception:

        conn.rollback()

        flash(
            "No se pudo eliminar el producto.",
            "danger"
        )

    finally:

        cursor.close()
        conn.close()

    return redirect(url_for("productos"))

# =========================================================
# NUEVO PRODUCTO
# =========================================================

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def formulario_producto():

    form = ProductoForm()

    # =====================================================
    # OBTENER PROVEEDORES
    # =====================================================

    conn = conectar_bd()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    # Cargar proveedores en el SELECT
    form.id_proveedor.choices = [
        (
            proveedor["id_proveedor"],
            proveedor["nombre"]
        )
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
            (
                nombre,
                precio,
                stock,
                id_proveedor
            )
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

        flash(
            "Producto registrado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    # =====================================================
    # MOSTRAR FORMULARIO
    # =====================================================

    return render_template(
        "formulario_producto.html",
        form=form,
        titulo="Registrar producto"
    )


# =========================================================
# CLIENTES
# =========================================================

@app.route("/clientes")
@login_required
def clientes():

    conn = conectar_bd()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

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


# =========================================================
# NUEVO CLIENTE
# =========================================================

@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def formulario_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes
            (
                nombre,
                cedula,
                telefono,
                correo
            )
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

        flash(
            "Cliente registrado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form,
        titulo="Registrar cliente"
    )


# =========================================================
# EDITAR CLIENTE
# =========================================================

@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cliente(id):

    conn = conectar_bd()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Buscar cliente
    cursor.execute("""
        SELECT
            id_cliente,
            nombre,
            cedula,
            telefono,
            correo
        FROM clientes
        WHERE id_cliente = %s
    """, (id,))

    cliente = cursor.fetchone()

    cursor.close()
    conn.close()

    # Verificar si existe
    if cliente is None:

        flash(
            "El cliente no existe.",
            "danger"
        )

        return redirect(url_for("clientes"))

    # Crear formulario
    form = ClienteForm()

    # Cargar datos cuando se abre el formulario
    if request.method == "GET":

        form.nombre.data = cliente["nombre"]
        form.cedula.data = cliente["cedula"]
        form.telefono.data = cliente["telefono"]
        form.correo.data = cliente["correo"]

    # Actualizar
    if form.validate_on_submit():

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE clientes
            SET
                nombre = %s,
                cedula = %s,
                telefono = %s,
                correo = %s
            WHERE id_cliente = %s
        """, (
            form.nombre.data,
            form.cedula.data,
            form.telefono.data,
            form.correo.data,
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Cliente actualizado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form,
        titulo="Editar cliente"
    )


# =========================================================
# ELIMINAR CLIENTE
# =========================================================

@app.route("/clientes/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_cliente(id):

    conn = conectar_bd()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            DELETE FROM clientes
            WHERE id_cliente = %s
        """, (id,))

        conn.commit()

        flash(
            "Cliente eliminado correctamente.",
            "success"
        )

    except Exception:

        conn.rollback()

        flash(
            "No se pudo eliminar el cliente. "
            "Puede estar relacionado con una factura.",
            "danger"
        )

    finally:

        cursor.close()
        conn.close()

    return redirect(url_for("clientes"))



# =========================================================
# PROVEEDORES
# =========================================================

@app.route("/proveedores")
@login_required
def proveedores():

    conn = conectar_bd()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

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


# =========================================================
# NUEVO PROVEEDOR
# =========================================================

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def formulario_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO proveedores
            (
                nombre,
                telefono,
                correo
            )
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.telefono.data,
            form.correo.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Proveedor registrado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form,
        titulo="Registrar proveedor"
    )


# =========================================================
# EDITAR PROVEEDOR
# =========================================================

@app.route("/proveedores/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id):

    conn = conectar_bd()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Buscar proveedor
    cursor.execute("""
        SELECT
            id_proveedor,
            nombre,
            telefono,
            correo
        FROM proveedores
        WHERE id_proveedor = %s
    """, (id,))

    proveedor = cursor.fetchone()

    cursor.close()
    conn.close()

    # Verificar si existe
    if proveedor is None:

        flash(
            "El proveedor no existe.",
            "danger"
        )

        return redirect(url_for("proveedores"))

    # Crear formulario
    form = ProveedorForm()

    # Cargar datos actuales
    if request.method == "GET":

        form.nombre.data = proveedor["nombre"]
        form.telefono.data = proveedor["telefono"]
        form.correo.data = proveedor["correo"]

    # Guardar cambios
    if form.validate_on_submit():

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE proveedores
            SET
                nombre = %s,
                telefono = %s,
                correo = %s
            WHERE id_proveedor = %s
        """, (
            form.nombre.data,
            form.telefono.data,
            form.correo.data,
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Proveedor actualizado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form,
        titulo="Editar proveedor"
    )


# =========================================================
# ELIMINAR PROVEEDOR
# =========================================================

@app.route("/proveedores/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_proveedor(id):

    conn = conectar_bd()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            DELETE FROM proveedores
            WHERE id_proveedor = %s
        """, (id,))

        conn.commit()

        flash(
            "Proveedor eliminado correctamente.",
            "success"
        )

    except Exception:

        conn.rollback()

        flash(
            "No se puede eliminar el proveedor porque "
            "puede estar relacionado con productos.",
            "danger"
        )

    finally:

        cursor.close()
        conn.close()

    return redirect(url_for("proveedores"))




# =========================================================
# FACTURACIÓN
# =========================================================

@app.route("/facturacion")
@login_required
def facturacion():

    conn = conectar_bd()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

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
    cursor = conn.cursor(cursor_factory=RealDictCursor)

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
            VALUES (%s, CURRENT_DATE, %s)
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