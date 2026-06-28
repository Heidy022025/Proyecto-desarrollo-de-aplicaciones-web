const formulario = document.getElementById("formProducto");
const lista = document.getElementById("listaProductos");
const mensaje = document.getElementById("mensaje");
const contador = document.getElementById("contador");

let total = 0;

formulario.addEventListener("submit", function(e){

    e.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();
    const categoria = document.getElementById("categoria").value.trim();

    if(nombre==="" || descripcion==="" || categoria===""){

        mensaje.innerHTML=
        '<div class="alert alert-danger">Complete todos los campos.</div>';

        return;
    }

    mensaje.innerHTML=
    '<div class="alert alert-success">Producto registrado correctamente.</div>';

    const card=document.createElement("div");

    card.className="card shadow mb-3";

    card.innerHTML=`
        <div class="card-body">
            <h5>${nombre}</h5>
            <p>${descripcion}</p>
            <span class="badge bg-primary">${categoria}</span>
            <br><br>

            <button class="btn btn-danger eliminar">
                Eliminar
            </button>
        </div>
    `;

    card.querySelector(".eliminar").addEventListener("click",function(){

        card.remove();

        total--;

        contador.textContent=total;

    });

    lista.appendChild(card);

    total++;

    contador.textContent=total;

    formulario.reset();

});