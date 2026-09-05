from flask import Flask, render_template, redirect, url_for

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)

# Configuración de Flask-WTF y protección CSRF
app.config["SECRET_KEY"] = "smartventas-clave-secreta-2026"


# =========================================================
# PÁGINA DE INICIO
# =========================================================

@app.route('/')
def inicio():

    nombre_sistema = "SmartVentas Solutions"

    resumen = {
        "productos": 3,
        "clientes": 3,
        "proveedores": 3,
        "facturas": 2
    }

    return render_template(
        'index.html',
        nombre_sistema=nombre_sistema,
        resumen=resumen
    )


# =========================================================
# PRODUCTOS
# =========================================================

@app.route('/productos')
def productos():

    productos = [
        {
            "nombre": "Laptop Lenovo",
            "categoria": "Tecnología",
            "precio": 850.00,
            "stock": 5
        },
        {
            "nombre": "Mouse inalámbrico",
            "categoria": "Accesorios",
            "precio": 14.00,
            "stock": 12
        },
        {
            "nombre": "Teclado USB",
            "categoria": "Accesorios",
            "precio": 25.00,
            "stock": 0
        }
    ]

    return render_template(
        'productos.html',
        productos=productos
    )


@app.route('/productos/nuevo', methods=['GET', 'POST'])
def formulario_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        producto = {
            "nombre": form.nombre.data,
            "categoria": form.categoria.data,
            "precio": form.precio.data,
            "stock": form.stock.data
        }

        print("Producto registrado:", producto)

        return redirect(url_for('productos'))

    return render_template(
        'formulario_producto.html',
        form=form
    )


# =========================================================
# CLIENTES
# =========================================================

@app.route('/clientes')
def clientes():

    clientes = [
        {
            "nombre": "Juan Pérez",
            "cedula": "1723456789",
            "telefono": "0991234567",
            "correo": "juan@gmail.com"
        },
        {
            "nombre": "María González",
            "cedula": "1712345678",
            "telefono": "0987654321",
            "correo": "maria@gmail.com"
        },
        {
            "nombre": "Carlos Rodríguez",
            "cedula": "1709876543",
            "telefono": "0976543210",
            "correo": "carlos@gmail.com"
        }
    ]

    return render_template(
        'clientes.html',
        clientes=clientes
    )


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def formulario_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        cliente = {
            "nombre": form.nombre.data,
            "cedula": form.cedula.data,
            "telefono": form.telefono.data,
            "correo": form.correo.data
        }

        print("Cliente registrado:", cliente)

        return redirect(url_for('clientes'))

    return render_template(
        'formulario_cliente.html',
        form=form
    )


# =========================================================
# PROVEEDORES
# =========================================================

@app.route('/proveedores')
def proveedores():

    proveedores = [
        {
            "empresa": "TecnoMarket",
            "contacto": "Andrés López",
            "telefono": "022345678",
            "producto": "Computadoras"
        },
        {
            "empresa": "CompuExpress",
            "contacto": "Laura Martínez",
            "telefono": "023456789",
            "producto": "Accesorios"
        },
        {
            "empresa": "Digital Store",
            "contacto": "Pedro Sánchez",
            "telefono": "024567890",
            "producto": "Equipos electrónicos"
        }
    ]

    return render_template(
        'proveedores.html',
        proveedores=proveedores
    )


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def formulario_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        proveedor = {
            "empresa": form.empresa.data,
            "contacto": form.contacto.data,
            "telefono": form.telefono.data,
            "producto": form.producto.data
        }

        print("Proveedor registrado:", proveedor)

        return redirect(url_for('proveedores'))

    return render_template(
        'formulario_proveedor.html',
        form=form
    )


# =========================================================
# FACTURACIÓN
# =========================================================

@app.route('/facturacion')
def facturacion():

    facturas = [
        {
            "numero": "FAC-001",
            "cliente": "Juan Pérez",
            "fecha": "22/08/2026",
            "total": 665.00,
            "estado": "Pagada"
        },
        {
            "numero": "FAC-002",
            "cliente": "María González",
            "fecha": "22/08/2026",
            "total": 40.00,
            "estado": "Pendiente"
        }
    ]

    return render_template(
        'facturacion.html',
        facturas=facturas
    )


@app.route('/facturacion/nueva', methods=['GET', 'POST'])
def formulario_facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        factura = {
            "cliente": form.cliente.data,
            "producto": form.producto.data,
            "cantidad": form.cantidad.data,
            "precio": form.precio.data
        }

        print("Factura registrada:", factura)

        return redirect(url_for('facturacion'))

    return render_template(
        'formulario_facturacion.html',
        form=form
    )


# =========================================================
# EJECUTAR APLICACIÓN
# =========================================================

if __name__ == '__main__':
    app.run(debug=True)