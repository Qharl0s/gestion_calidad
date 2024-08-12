from evidencia.models import Oficina, Periodo
def valida_pre_estandar(oficina_id, periodo_id):
    error = ''
    try:
        oficinas = Oficina.objects.filter(lVigente=True, lAcreditacion=True)
    except Oficina.DoesNotExist:
        error += '<li class="list-group-item">No se tiene oficinas configuradas.</li>'
    
    if oficina_id==0:
        error += '<li class="list-group-item">Seleccione una oficina.</li>'
    try:
        if oficina_id>0:
            oficina = Oficina.objects.get(lVigente=True, lAcreditacion=True, id=oficina_id)
    except Oficina.DoesNotExist:
        error += '<li class="list-group-item">No se encontró la oficina seleccionada.</li>'

    try:
        periodos = Periodo.objects.filter(lVigente=True, categoria__id=4).order_by('-id')
    except Periodo.DoesNotExist:
        error += '<li class="list-group-item">No se tiene Peridos configurados.</li>'

    try:
        if periodo_id>0:
            periodo_seleccionado = Periodo.objects.get(id=periodo_id)
    except Periodo.DoesNotExist:
        error += '<li class="list-group-item">No se encontró el Periodo seleccionado.</li>'

    if error != '':
        error = '<ul class="list-group"> <li class="list-group-item active">Mensaje:</li>' + error +'</ul>'
    return error
