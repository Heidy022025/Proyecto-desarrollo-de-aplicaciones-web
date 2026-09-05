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
const spinner = document.getElementById("spinner");
const modalRegistro = new bootstrap.Modal(document.getElementById("modalRegistro"));

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");

// ==============================
// Arreglo de objetos
// ==============================



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

        mensaje.className = "alert alert-danger mt-3";
        mensaje.textContent = "Existen errores en el formulario.";


        return;

    }

    productos.push({

        nombre: nombre.value,

        descripcion: descripcion.value,

        categoria: categoria.value,

        fecha: new Date().toLocaleDateString()

    });

spinner.classList.remove("d-none");

setTimeout(function(){

    spinner.classList.add("d-none");

    mostrarProductos();

    modalRegistro.show();

    formulario.reset();

},1500);

nombre.classList.remove("is-valid");
descripcion.classList.remove("is-valid");
categoria.classList.remove("is-valid");

mensaje.classList.remove("d-none");
mensaje.textContent = "Producto registrado correctamente.";
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

    mensaje.classList.remove("d-none");

    if(productos.length === 0){

        mensaje.className = "alert alert-warning mt-3";
        mensaje.textContent = "Todos los productos fueron eliminados.";

    }else{

        mensaje.className = "alert alert-info mt-3";
        mensaje.textContent = "Producto eliminado correctamente.";

    }

}
// ==============================
// Mostrar productos al iniciar
// ==============================

mostrarProductos();