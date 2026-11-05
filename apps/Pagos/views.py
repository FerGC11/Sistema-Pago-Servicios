import logging
from functools import wraps
from time import perf_counter
from uuid import uuid4

from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import pagos, informacionPagos, estatusPagos
from apps.Clientes.models import colonias, clientes
from .forms import InformacionPagoForm, ClienteForm, DireccionForm, PagoForm
from django.http import JsonResponse
from django.db.models import Q


logger = logging.getLogger(__name__)


def registrar_logs(vista):
    @wraps(vista)
    def wrapper(request, *args, **kwargs):
        request.log_id = uuid4().hex[:12]
        inicio = perf_counter()
        logger.info("id=%s vista=%s metodo=%s inicio", request.log_id, vista.__name__, request.method)
        try:
            respuesta = vista(request, *args, **kwargs)
        except Exception:
            logger.exception("id=%s vista=%s error_no_controlado", request.log_id, vista.__name__)
            raise
        logger.info("id=%s vista=%s estado_http=%s duracion_ms=%.1f", request.log_id,
                    vista.__name__, respuesta.status_code, (perf_counter() - inicio) * 1000)
        respuesta["X-Request-ID"] = request.log_id
        return respuesta
    return wrapper

@registrar_logs
@require_GET
def indexPagos(request):

    pagosDia = pagos.objects.filter(dFechaPago=timezone.localdate()).select_related('idInfoPago', 'idEstatusPago', 'idEstadoPago').prefetch_related('idInfoPago__clientes_set')

    fechaActual = timezone.localdate()
    
    coloniasRegistradas = colonias.objects.all().order_by('cColonia')

    clientesRegistrados = clientes.objects.select_related('idInfoPago').all()

    context = {
        'pagosDia': pagosDia,
        'fechaActual': fechaActual,
        'colonias': coloniasRegistradas,
        'clientes': clientesRegistrados
    }
        
    return render(request, 'pagos/Pagos.html', context)


@registrar_logs
@require_POST
def registrarServicio(request):

    info_pago_form = InformacionPagoForm(request.POST)
    cliente_form = ClienteForm(request.POST)
    direccion_form = DireccionForm(request.POST)

    # Validamos todos los formularios
    formularios_validos = all([
        info_pago_form.is_valid(),
        cliente_form.is_valid(),
        direccion_form.is_valid()
    ])

    # Si alguno falla, mostrar mensaje y regresar
    if not formularios_validos:
        for nombre, formulario in (("informacion_pago", info_pago_form),
                                   ("cliente", cliente_form), ("direccion", direccion_form)):
            errores = {campo: [error.code for error in lista]
                       for campo, lista in formulario.errors.as_data().items()}
            if errores:
                logger.warning("id=%s vista=registrarServicio validacion formulario=%s errores=%s",
                               request.log_id, nombre, errores)

        messages.error(
            request,
            f'No se pudo registrar el servicio. Verifica los datos. Folio: {request.log_id}'
        )

        return redirect('pagos:indexPagos')
    
     # Todos los formularios son válidos
    etapa = "iniciar_transaccion"
    try:
        with transaction.atomic():

            # 1. Guardar información del pago
            etapa = "guardar_informacion_pago"
            info_pago = info_pago_form.save()

            # 3. Guardar dirección
            etapa = "guardar_direccion"
            direccion = direccion_form.save(commit=False)
            direccion.idestado_id = 1
            direccion.idmunicipio_id = 1
            direccion.save()

            # 4. Guardar cliente con sus relaciones
            etapa = "guardar_cliente"
            cliente = cliente_form.save(commit=False)
            cliente.idInfoPago = info_pago
            cliente.idDireccion = direccion
            cliente.save()

        logger.info("id=%s vista=registrarServicio servicio_guardado cliente_id=%s info_pago_id=%s direccion_id=%s",
                    request.log_id, cliente.pk, info_pago.pk, direccion.pk)
        messages.success(
            request,
            'Nuevo servicio registrado correctamente.'
        )

    except Exception:
        logger.exception("id=%s vista=registrarServicio error_guardado etapa=%s", request.log_id, etapa)
        messages.error(
            request,
            f'Ocurrió un error al guardar el servicio. Folio: {request.log_id}'
        )

    return redirect('pagos:indexPagos')


@registrar_logs
@require_GET
def buscarCliente(request):

    texto = request.GET.get('q', '').strip()

    if len(texto) < 2:
        return JsonResponse({'resultados': []})

    consulta = Q()
    for termino in texto.split():
        consulta &= (
            Q(cNombre__icontains=termino) |
            Q(cApellidoPaterno__icontains=termino) |
            Q(cApellidoMaterno__icontains=termino) |
            Q(idInfoPago__iReferencia__icontains=termino) |
            Q(cAlias__icontains=termino)
        )
    clientesEncontrados = (
        clientes.objects.select_related('idInfoPago')
        .filter(consulta)
        .order_by('cNombre', 'cApellidoPaterno', 'pk')[:10]
    )

    resultados = []

    for cliente in clientesEncontrados:

        pago_info = cliente.idInfoPago

        resultados.append({
            'id': cliente.pk,
            'idInfoPago': pago_info.pk,
            'nombre': f"{cliente.cNombre} {cliente.cApellidoPaterno} {cliente.cApellidoMaterno}",
            'referencia': pago_info.iReferencia,
            'alias': cliente.cAlias
        })

    logger.info("id=%s vista=buscarCliente coincidencias=%s", request.log_id, len(resultados))
    return JsonResponse({'resultados': resultados})

@registrar_logs
@require_POST
def registrarPago(request):

    pago_form = PagoForm(request.POST)

    if not pago_form.is_valid():
        errores = {campo: [error.code for error in lista]
                   for campo, lista in pago_form.errors.as_data().items()}
        logger.warning("id=%s vista=registrarPago validacion formulario errores=%s", request.log_id, errores)
        messages.error(
            request,
            f'No se pudo registrar el pago. Verifica los datos. Folio: {request.log_id}'
        )
        return redirect('pagos:indexPagos')

    etapa = "iniciar_transaccion"
    try:
        with transaction.atomic():

            # Guardar pago
            etapa = "guardar_pago"
            pago = pago_form.save(commit=False)
            pago.dFechaPago = timezone.localdate()
            pago.idEstatusPago_id = 2  
            pago.save()

        logger.info("id=%s vista=registrarPago pago_guardado pago_id=%s", request.log_id, pago.pk)
        messages.success(
            request,
            'Pago registrado correctamente.'
        )

    except Exception:
        logger.exception("id=%s vista=registrarPago error_guardado etapa=%s", request.log_id, etapa)
        messages.error(
            request,
            f'Ocurrió un error al registrar el pago. Folio: {request.log_id}'
        )

    return redirect('pagos:indexPagos')

@registrar_logs
@require_POST
def confirmarPago(request):
    pago_id = request.POST.get('pago_id', '')
    referencia = request.POST.get('referencia', '').strip()
    original = request.POST.get('referencia_original', '').strip()
    if not pago_id.isdecimal() or not referencia or not original:
        messages.error(request, 'Completa la referencia y selecciona un pago valido.')
        return redirect('pagos:indexPagos')
    try:
        with transaction.atomic():
            pago = pagos.objects.select_for_update().select_related('idInfoPago', 'idEstatusPago').get(pk=pago_id)
            referencia_real = pago.idInfoPago.iReferencia
            if referencia_real is None or referencia != original or original != str(referencia_real):
                logger.warning('id=%s vista=confirmarPago referencias_no_coinciden pago_id=%s', request.log_id, pago.pk)
                messages.error(request, 'Las referencias no coinciden.')
                return redirect('pagos:indexPagos')
            pagado = estatusPagos.objects.get(cEstatusPago__iexact='Pagado')
            pago.idEstatusPago = pagado
            pago.save(update_fields=['idEstatusPago'])
        logger.info('id=%s vista=confirmarPago pago_confirmado pago_id=%s', request.log_id, pago.pk)
        messages.success(request, 'Pago confirmado correctamente. Estatus: Pagado.')
    except pagos.DoesNotExist:
        messages.error(request, 'El pago seleccionado no existe.')
    except Exception:
        logger.exception('id=%s vista=confirmarPago error_confirmacion pago_id=%s', request.log_id, pago_id)
        messages.error(request, f'No se pudo confirmar el pago. Folio: {request.log_id}')
    return redirect('pagos:indexPagos')


@registrar_logs
@require_GET
def detallePago(request, pago_id):
    pago = get_object_or_404(pagos.objects.select_related('idInfoPago'), pk=pago_id)
    info = pago.idInfoPago
    registros = info.clientes_set.select_related(
        'idDireccion__idEstado', 'idDireccion__idMunicipio', 'idDireccion__idColonia'
    ).order_by('pk')
    datos_clientes = []
    for cliente in registros:
        direccion = cliente.idDireccion
        datos_clientes.append({
            'id': cliente.pk,
            'detalleNombre': cliente.cNombre,
            'detallePrimerApellido': cliente.cApellidoPaterno,
            'detalleSegundoApellido': cliente.cApellidoMaterno,
            'detalleAlias': cliente.cAlias or '',
            'detalleServicioTexto': cliente.cDetalle or '',
            'detalleEstado': direccion.idEstado.cEstado if direccion and direccion.idEstado else '',
            'detalleMunicipio': direccion.idMunicipio.cMunicipio if direccion and direccion.idMunicipio else '',
            'detalleColonia': direccion.idColonia.cColonia if direccion and direccion.idColonia else '',
            'detalleCalle': direccion.cCalle or '' if direccion else '',
            'detalleNumero': direccion.cNumero or '' if direccion else '',
            'detalleActivo': cliente.bActivo,
        })
    return JsonResponse({
        'pago_id': pago.pk,
        'detalleReferencia': info.iReferencia,
        'detalleImporte': info.iImporte,
        'detalleFechaCorte': info.dFechaCorte.isoformat() if info.dFechaCorte else '',
        'clientes': datos_clientes,
    })
