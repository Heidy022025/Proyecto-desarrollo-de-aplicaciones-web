const formulario=document.getElementById("formProducto");

const nombre=document.getElementById("nombre");
const descripcion=document.getElementById("descripcion");
const categoria=document.getElementById("categoria");

const mensaje=document.getElementById("mensaje");
const lista=document.getElementById("listaProductos");
const contador=document.getElementById("contador");

let productos=[];

function validarNombre(){

    if(nombre.value.trim().length<3){

        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        errorNombre.textContent="Debe tener mínimo 3 caracteres.";

        return false;

    }

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");

    errorNombre.textContent="";

    return true;

}

function validarDescripcion(){

    if(descripcion.value.trim().length<10){

        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");

        errorDescripcion.textContent="Ingrese al menos 10 caracteres.";

        return false;

    }

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");

    errorDescripcion.textContent="";

    return true;

}

function validarCategoria(){

    if(categoria.value==""){

        categoria.classList.add("is-invalid");
        categoria.classList.remove("is-valid");

        errorCategoria.textContent="Seleccione una categoría.";

        return false;

    }

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");

    errorCategoria.textContent="";

    return true;

}

nombre.addEventListener("input",validarNombre);
nombre.addEventListener("blur",validarNombre);

descripcion.addEventListener("input",validarDescripcion);
descripcion.addEventListener("blur",validarDescripcion);

categoria.addEventListener("change",validarCategoria);

formulario.addEventListener("submit",function(e){

    e.preventDefault();

    let valido=
    validarNombre() &&
    validarDescripcion() &&
    validarCategoria();

    if(!valido){

        mensaje.innerHTML=
        '<div class="alert alert-danger">Existen errores en el formulario.</div>';

        return;

    }

    productos.push({

        nombre:nombre.value,
        descripcion:descripcion.value,
        categoria:categoria.value

    });

    mostrarProductos();

    formulario.reset();

    nombre.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");
    categoria.classList.remove("is-valid");

    mensaje.innerHTML=
    '<div class="alert alert-success">Producto registrado correctamente.</div>';

});

function mostrarProductos(){

    lista.innerHTML="";

    productos.forEach(function(producto,index){

        lista.innerHTML+=`

        <div class="card mt-3">

            <div class="card-body">

                <h5>${producto.nombre}</h5>

                <p>${producto.descripcion}</p>

                <span class="badge bg-primary">${producto.categoria}</span>

                <br><br>

                <button class="btn btn-danger"
                onclick="eliminarProducto(${index})">

                Eliminar

                </button>

            </div>

        </div>

        `;

    });

    contador.textContent=productos.length;

}

function eliminarProducto(indice){

    productos.splice(indice,1);

    mostrarProductos();

}