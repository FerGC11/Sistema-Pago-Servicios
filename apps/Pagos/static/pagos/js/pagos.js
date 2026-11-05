document.addEventListener("DOMContentLoaded", () => {
    const modalConfirmacionPago = document.getElementById("modalConfirmacionPago");
    const campoReferencia = document.getElementById("confirmacionReferencia");

    if (!modalConfirmacionPago || !campoReferencia) {
        return;
    }

    modalConfirmacionPago.addEventListener("show.bs.modal", (event) => {
        const botonEstatus = event.relatedTarget;
        campoReferencia.value = "";
        document.getElementById("confirmacionPagoId").value = botonEstatus?.dataset.pagoId ?? "";
        document.getElementById("confirmacionReferenciaOriginal").value = botonEstatus?.dataset.referencia ?? "";
    });

    modalConfirmacionPago.addEventListener("shown.bs.modal", () => {
        campoReferencia.focus();
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const buscador = document.getElementById('buscadorClientePago');
    const resultados = document.getElementById('resultadosClientesPago');
    const idInfoPago = document.getElementById('idInfoPago');
    if (!buscador || !resultados || !idInfoPago || !buscador.dataset.urlBusqueda) return;
    const formulario = buscador.closest('form');
    let temporizador;
    let controlador;
    let version = 0;
    const mensaje = texto => {
        const aviso = document.createElement('p');
        aviso.textContent = texto;
        resultados.replaceChildren(aviso);
    };
    buscador.addEventListener('input', () => {
        const texto = buscador.value.trim();
        const actual = ++version;
        idInfoPago.value = '';
        buscador.setCustomValidity('');
        resultados.replaceChildren();
        clearTimeout(temporizador);
        controlador?.abort();
        if (texto.length < 2) return;
        temporizador = setTimeout(async () => {
            controlador = new AbortController();
            try {
                const url = new URL(buscador.dataset.urlBusqueda, window.location.origin);
                url.searchParams.set('q', texto);
                const respuesta = await fetch(url, {signal: controlador.signal});
                if (!respuesta.ok) throw new Error(`Busqueda HTTP ${respuesta.status}; folio ${respuesta.headers.get('X-Request-ID') || '-'}`);
                const datos = await respuesta.json();
                if (actual !== version) return;
                resultados.replaceChildren();
                if (!datos.resultados.length) mensaje('No se encontraron clientes.');
                datos.resultados.forEach(cliente => {
                    const opcion = document.createElement('button');
                    opcion.type = 'button';
                    opcion.className = 'resultado-cliente';
                    opcion.textContent = `${cliente.nombre} - Ref. ${cliente.referencia ?? 'Sin referencia'}${cliente.alias ? ` - Alias: ${cliente.alias}` : ''}`;
                    opcion.addEventListener('click', () => {
                        version++;
                        buscador.value = opcion.textContent;
                        idInfoPago.value = cliente.idInfoPago;
                        buscador.setCustomValidity('');
                        resultados.replaceChildren();
                    });
                    resultados.appendChild(opcion);
                });
            } catch (error) {
                if (error.name !== 'AbortError' && actual === version) {
                    console.error('Busqueda de clientes:', error);
                    mensaje('No se pudo consultar clientes. Intenta de nuevo.');
                }
            }
        }, 300);
    });
    formulario.addEventListener('submit', event => {
        if (!idInfoPago.value) {
            event.preventDefault();
            buscador.setCustomValidity('Selecciona un cliente de las coincidencias.');
            buscador.reportValidity();
        }
    });
    formulario.addEventListener('reset', () => {
        version++;
        clearTimeout(temporizador);
        controlador?.abort();
        idInfoPago.value = '';
        buscador.setCustomValidity('');
        resultados.replaceChildren();
    });
});


document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-copiar-referencia]').forEach(boton => {
        boton.addEventListener('click', async () => {
            const referencia = boton.dataset.copiarReferencia;
            if (!referencia) return;
            try {
                if (window.isSecureContext && navigator.clipboard?.writeText) {
                    await navigator.clipboard.writeText(referencia);
                } else {
                    const auxiliar = document.createElement('textarea');
                    auxiliar.value = referencia;
                    auxiliar.style.position = 'fixed';
                    auxiliar.style.opacity = '0';
                    document.body.appendChild(auxiliar);
                    let copiado;
                    try {
                        auxiliar.select();
                        copiado = document.execCommand('copy');
                    } finally {
                        auxiliar.remove();
                        boton.focus();
                    }
                    if (!copiado) throw new Error('No se pudo copiar');
                }
                if (window.Swal) Swal.fire({icon:'success',title:'Referencia copiada',timer:1200,showConfirmButton:false});
            } catch (error) {
                console.error('Copiar referencia:', error);
                if (window.Swal) Swal.fire({icon:'error',title:'No se pudo copiar la referencia'});
            }
        });
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modalDetalleServicio');
    if (!modal) return;
    const formulario = modal.querySelector('.formulario-detalle-servicio');
    const mensaje = document.getElementById('detalleMensaje');
    const selector = document.getElementById('detalleSelectorCliente');
    const contenedor = document.getElementById('detalleSelectorContenedor');
    const actualizar = modal.querySelector('.boton-actualizar-servicio');
    let controlador;
    let version = 0;
    let clientes = [];
    const camposCliente = ['detalleNombre','detallePrimerApellido','detalleSegundoApellido','detalleAlias','detalleServicioTexto','detalleEstado','detalleMunicipio','detalleColonia','detalleCalle','detalleNumero'];
    function cargarCliente(cliente) {
        camposCliente.forEach(id => { document.getElementById(id).value = cliente?.[id] ?? ''; });
        document.getElementById('detalleActivo').checked = cliente?.detalleActivo ?? false;
    }
    selector.addEventListener('change', () => cargarCliente(clientes.find(cliente => String(cliente.id) === selector.value)));
    modal.addEventListener('show.bs.modal', async event => {
        const actual = ++version;
        controlador?.abort();
        controlador = new AbortController();
        formulario.reset();
        cargarCliente(null);
        ['detalleReferencia','detalleImporte','detalleFechaCorte'].forEach(id => {document.getElementById(id).value = '';});
        selector.replaceChildren();
        contenedor.hidden = true;
        actualizar.disabled = true;
        mensaje.textContent = 'Cargando datos del registro...';
        try {
            const url = event.relatedTarget?.dataset.detalleUrl;
            if (!url) throw new Error('Falta el registro seleccionado');
            const respuesta = await fetch(url, {signal: controlador.signal});
            if (!respuesta.ok) throw new Error(`Detalle HTTP ${respuesta.status}`);
            const datos = await respuesta.json();
            if (actual !== version) return;
            ['detalleReferencia','detalleImporte','detalleFechaCorte'].forEach(id => {document.getElementById(id).value = datos[id] ?? '';});
            clientes = datos.clientes;
            clientes.forEach(cliente => {
                const opcion = document.createElement('option');
                opcion.value = cliente.id;
                opcion.textContent = `${cliente.detalleNombre} ${cliente.detallePrimerApellido} ${cliente.detalleSegundoApellido}`;
                selector.appendChild(opcion);
            });
            contenedor.hidden = clientes.length < 2;
            cargarCliente(clientes[0]);
            mensaje.textContent = clientes.length ? '' : 'El registro no tiene cliente asociado.';
            actualizar.disabled = !clientes.length;
        } catch (error) {
            if (error.name !== 'AbortError' && actual === version) {
                mensaje.textContent = 'No se pudo cargar el detalle. Cierra y vuelve a intentarlo.';
                console.error('Detalle del pago:', error);
            }
        }
    });
    modal.addEventListener('hidden.bs.modal', () => {version++; controlador?.abort();});
});
