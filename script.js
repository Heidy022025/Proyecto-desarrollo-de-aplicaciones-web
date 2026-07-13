// ==============================
// Obtención de elementos del DOM
// ==============================

const formulario = document.getElementById("formProducto");

const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const mensaje = document.getElementById("mensaje");
const lista = document.getElementById("listaProductos");
const contador = document.getElementById("contador");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");

// ==============================
// Arreglo de objetos
// ==============================

let productos = [

    {
        nombre: "Laptop Lenovo",
        descripcion: "Laptop Core i5 con 8 GB de memoria RAM.",
        categoria: "Electrónica",
        fecha: "Producto inicial"
    },

    {
        nombre: "Cuaderno Universitario",
        descripcion: "Cuaderno de 100 hojas para uso académico.",
        categoria: "Oficina",
        fecha: "Producto inicial"
    }

];

// ==============================
// Validaciones
// ==============================

function validarNombre(){

    if(nombre.value.trim().length < 3){

        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        errorNombre.textContent = "Debe tener mínimo 3 caracteres.";

        return false;

    }

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");

    errorNombre.textContent = "";

    return true;

}

function validarDescripcion(){

    if(descripcion.value.trim().length < 10){

        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");

        errorDescripcion.textContent = "Ingrese al menos 10 caracteres.";

        return false;

    }

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");

    errorDescripcion.textContent = "";

    return true;

}

function validarCategoria(){

    if(categoria.value == ""){

        categoria.classList.add("is-invalid");
        categoria.classList.remove("is-valid");

        errorCategoria.textContent = "Seleccione una categoría.";

        return false;

    }

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");

    errorCategoria.textContent = "";

    return true;

}

// ==============================
// Eventos
// ==============================

nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

categoria.addEventListener("change", validarCategoria);

// ==============================
// Registrar producto
// ==============================

formulario.addEventListener("submit", function(e){

    e.preventDefault();

    let valido =

        validarNombre() &&
        validarDescripcion() &&
        validarCategoria();

    if(!valido){

        mensaje.innerHTML =

        `<div class="alert alert-danger">

            Existen errores en el formulario.

        </div>`;

        return;

    }

    productos.push({

        nombre: nombre.value,

        descripcion: descripcion.value,

        categoria: categoria.value,

        fecha: new Date().toLocaleDateString()

    });

    mostrarProductos();

    formulario.reset();

    nombre.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");
    categoria.classList.remove("is-valid");

    mensaje.innerHTML =

    `<div class="alert alert-success">

        Producto registrado correctamente.

    </div>`;

});

// ==============================
// Mostrar productos
// ==============================

function mostrarProductos(){

    lista.innerHTML = "";

    if(productos.length === 0){

        lista.innerHTML =

        `<div class="col-12">

            <div class="alert alert-warning text-center">

                No existen productos registrados.

            </div>

        </div>`;

    }else{

        productos.forEach(function(producto, index){

            lista.innerHTML += `

            <div class="col-md-4 mb-4">

                <div class="card h-100 shadow">

                    <div class="card-body">

                        <h5 class="card-title">

                            ${producto.nombre}

                        </h5>

                        <p>

                            ${producto.descripcion}

                        </p>

                        <span class="badge bg-primary">

                            ${producto.categoria}

                        </span>

                        <hr>

                        <p>

                            <strong>Fecha:</strong>

                            ${producto.fecha}

                        </p>

                        <button

                            class="btn btn-danger w-100"

                            onclick="eliminarProducto(${index})">

                            Eliminar

                        </button>

                    </div>

                </div>

            </div>

            `;

        });

    }

    contador.textContent = productos.length;

}

// ==============================
// Eliminar producto
// ==============================

function eliminarProducto(indice){

    productos.splice(indice, 1);

    mostrarProductos();

    if(productos.length === 0){

        mensaje.innerHTML =

        `<div class="alert alert-warning">

            Todos los productos fueron eliminados.

        </div>`;

    }else{

        mensaje.innerHTML =

        `<div class="alert alert-info">

            Producto eliminado correctamente.

        </div>`;

    }

}

// ==============================
// Mostrar productos al iniciar
// ==============================

mostrarProductos();