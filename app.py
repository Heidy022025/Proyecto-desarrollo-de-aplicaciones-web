from flask import Flask, render_template

app = Flask(__name__)


# Página de inicio
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


# Módulo de productos
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


# Módulo de clientes
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


# Módulo de proveedores
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


# Módulo de facturación
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


if __name__ == '__main__':
    app.run(debug=True)