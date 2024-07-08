$(document).ready(function () {
    // Enfocar automáticamente el campo de escaneo al cargar la página
    $("#codigoBarras").focus();

    // Ocultar el campo de búsqueda de clientes inicialmente
    $("#buscarClienteDiv").hide();

    // Manejar la selección del tipo de pago
    $("#tipoPago").change(function () {
        if ($(this).val() === "pendiente") {
            $("#buscarClienteDiv").show();
        } else {
            $("#buscarClienteDiv").hide();
        }
    });

    // Manejar la selección del tipo de documento (Boleta / Factura)
    $("#tipoDocumento").change(function () {
        var tipoSeleccionado = $(this).val();
        if (tipoSeleccionado === "factura") {
            $("#tipoDocumentoTexto").text("Factura");
            $("#camposFactura").show();
            $("#detalleCliente").hide(); // Ocultar detalles del cliente cuando es factura
            // Habilitar la búsqueda de clientes por nombre/razón social
            $("#nombreClienteInput").on("input", buscarClientes);
        } else {
            $("#tipoDocumentoTexto").text("Boleta");
            $("#camposFactura").hide();
            $("#detalleCliente").show(); // Mostrar detalles del cliente cuando es boleta
            // Deshabilitar la búsqueda de clientes si no es factura
            $("#nombreClienteInput").off("input", buscarClientes);
        }
    });

    // Función para buscar clientes por nombre/razón social
    function buscarClientes() {
        var nombreCliente = $('#nombreClienteInput').val().trim();
        if (nombreCliente.length === 0) {
            // Limpiar los campos si no hay texto de búsqueda
            limpiarCamposCliente();
            $('#listaClientes').empty().hide(); // Ocultar la lista si no hay resultados
            return;
        }
    
        // Realizar una solicitud AJAX al backend de Django para buscar clientes
        $.ajax({
            url: '/buscar-clientes/',  
            method: 'GET',
            data: { nombre: nombreCliente },
            success: function (response) {
                mostrarResultadosClientes(response);
            },
            error: function (xhr, status, error) {
                console.error('Error en la solicitud AJAX:', error);
                alert('Error al buscar clientes. Por favor, inténtelo de nuevo.');
            }
        });
    }

    // Función para mostrar los resultados de búsqueda de clientes
    function mostrarResultadosClientes(response) {
        var listaClientes = $('#listaClientes');
        listaClientes.empty(); // Limpiar la lista de resultados
    
        if (!response.clientes || response.clientes.length === 0) {
            listaClientes.hide(); // Ocultar la lista si no hay resultados
            return;
        }
    
        // Mostrar la lista de resultados y llenarla con los clientes encontrados
        listaClientes.show();
        response.clientes.forEach(function (cliente) {
            var itemLista = $('<li class="list-group-item buscar-cliente-item"></li>');
            itemLista.text(cliente.nombre); 
    
            // Manejar clic en un cliente de la lista
            itemLista.click(function () {
                llenarCamposCliente(cliente);
                listaClientes.hide(); 
            });
    
            listaClientes.append(itemLista);
        });
    }

    // Función para llenar automáticamente los campos del cliente seleccionado
    function llenarCamposCliente(cliente) {
        $("#nombreClienteInput").val(cliente.nombre);
        $("#rutClienteInput").val(cliente.rut);
        $("#direccionClienteInput").val(cliente.direccion);
        $("#telefonoClienteInput").val(cliente.telefono);
        
    }

    // Función para limpiar los campos del cliente
    function limpiarCamposCliente() {
        $("#nombreClienteInput").val("");
        $("#rutClienteInput").val("");
        $("#direccionClienteInput").val("");
        $("#telefonoClienteInput").val("");
       
    }

    // Manejar clic en botón de escanear
    $("#btnEscanear").click(function () {
        escanearCodigo();
    });

    // Detectar presión de tecla "Enter" en el campo de escaneo
    $("#codigoBarras").keypress(function (e) {
        if (e.which === 13) {

            escanearCodigo();
        }
    });

    // Función para escanear el código de barras y agregar producto al detalle de venta
    function escanearCodigo() {
        var codigo = document.getElementById("codigoBarras").value.trim(); // Obtener el valor del campo y eliminar espacios en blanco

        // Verificar que el campo no esté vacío
        if (codigo === "") {
            alert("Por favor ingresa un código de barras válido");
            return;
        }

        // Solicitud AJAX al backend en Django para obtener datos del producto
        $.ajax({
            url: "/obtener-producto/", 
            method: "GET",
            data: { codigo: codigo },
            success: function (response) {
                // Si la solicitud es exitosa, response contendrá los datos del producto
                if (response) {
                    agregarProducto(
                        response.nombre,
                        response.precio,
                        1,
                        response.codigo
                    );
                } else {
                    alert("Producto no encontrado");
                }
            },
            error: function (xhr, status, error) {
                console.error("Error en la solicitud AJAX:", error);
                alert(
                    "Error al buscar el producto. Por favor, inténtelo de nuevo."
                );
            },
        });

        // Limpiar el campo de código de barras después de escanear
        document.getElementById("codigoBarras").value = "";
    }

    // Función para manejar cambios en la cantidad de productos
    $(document).on("click", ".cantidad-btn", function () {
        const action = $(this).data("action");
        const input = $(this).closest("li").find(".cantidad-input");
        let cantidad = parseInt(input.val());
        if (action === "decrement") {
            cantidad = Math.max(1, cantidad - 1);
        } else if (action === "increment") {
            cantidad += 1;
        }
        input.val(cantidad);
        actualizarSubtotal($(this).closest("li"));
        actualizarTotalVenta();
    });

    // Función para agregar un producto al detalle de venta
    function agregarProducto(nombre, precio, cantidad, codigo) {
        const itemHTML = `
            <li class="list-group-item d-flex justify-content-between align-items-center" data-codigo="${codigo}">
                <div class="row w-100">
                    <div class="col-md-4">
                        <h6 class="my-0">${nombre}</h6>
                    </div>
                    <div class="col-md-2">
                        <span class="badge badge-primary badge-pill producto-precio">$${precio.toFixed(
                            0
                        )}</span>
                    </div>
                    <div class="col-md-3">
                        <div class="input-group">
                            <button type="button" class="btn btn-outline-secondary btn-sm cantidad-btn" data-action="decrement">-</button>
                            <input type="number" class="form-control form-control-sm cantidad-input" value="${cantidad}" min="1" readonly>
                            <button type="button" class="btn btn-outline-secondary btn-sm cantidad-btn" data-action="increment">+</button>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <span class="subtotal">$${(precio * cantidad).toFixed(
                            0
                        )}</span>
                    </div>
                    <div class="col-md-1">
                        <button type="button" class="btn btn-danger btn-sm eliminar-producto">Eliminar</button>
                    </div>
                </div>
            </li>
        `;
        $("#detalleVenta").append(itemHTML);
        actualizarTotalVenta();
    }

    // Función para actualizar el subtotal de un producto
    function actualizarSubtotal(item) {
        const precio = parseFloat(
            item.find(".producto-precio").text().replace("$", "")
        );
        const cantidad = parseInt(item.find(".cantidad-input").val());
        const subtotal = precio * cantidad;
        item.find(".subtotal").text("$" + subtotal.toFixed(0));
    }

    // Función para actualizar el total de la venta
    function actualizarTotalVenta() {
        let nuevoTotal = 0;
        $("#detalleVenta li").each(function () {
            const subtotal = parseFloat(
                $(this).find(".subtotal").text().replace("$", "")
            );
            nuevoTotal += subtotal;
        });

        // Formatear el total con solo un decimal
        const totalFormateado = nuevoTotal.toLocaleString("es-CL", {
            minimumFractionDigits: 0,
            maximumFractionDigits: 1,
        });

        $("#totalVenta").text(totalFormateado);
    }

    // Función para generar la boleta en formato PDF usando pdf-lib
    async function generarBoletaPDF() {
        // Crear un nuevo documento PDF
        const pdfDoc = await PDFLib.PDFDocument.create();
        const page = pdfDoc.addPage([350, 400]); 

        // Definir un nuevo objeto de fuente para el documento PDF
        const timesRomanFont = await pdfDoc.embedFont(
            PDFLib.StandardFonts.Helvetica
        );

        // Título de la boleta
        page.drawText("Boleta de Venta", {
            x: 50,
            y: 350,
            size: 24,
            font: timesRomanFont,
        });

        // Detalles de la venta
        let y = 300;
        $("#detalleVenta li").each(function (index) {
            const nombre = $(this).find("h6").text();
            const precio = $(this)
                .find(".producto-precio")
                .text();
            const cantidad = $(this).find(".cantidad-input").val();

            page.drawText(nombre + " - " + cantidad + " x " + precio, {
                x: 50,
                y: y,
                size: 12,
                font: timesRomanFont,
            });

            y -= 20;
        });

        // Total de la venta
        const total = $("#totalVenta").text();
        page.drawText("Total: $" + total, {
            x: 50,
            y: y,
            size: 14,
            font: timesRomanFont,
        });

        // Obtener el contenido del documento PDF como una ArrayBuffer
        const pdfBytes = await pdfDoc.save();


        const pdfBlob = new Blob([pdfBytes], { type: "application/pdf" });


        const pdfUrl = URL.createObjectURL(pdfBlob);
        window.open(pdfUrl);

        // Limpiar la URL del objeto luego de abrir la ventana
        URL.revokeObjectURL(pdfUrl);
    }

    // Manejar clic en botón "Finalizar Venta"
    $("#btnFinalizarVenta").click(function () {
        generarBoletaPDF();
    });
});
