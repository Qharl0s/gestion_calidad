def get_grafico_barra(titulo, objetos, div_id):
    categorias = ""
    aprobados = ""
    observados = ""
    pendientes = ""
    for objeto in objetos:
        categorias += "'"+objeto.descripcion+"',"
        aprobados += str(objeto.datos_objeto.aprobados)+","
        observados += str(objeto.datos_objeto.observados)+","
        pendientes += str(objeto.datos_objeto.pendientes)+","

    script = "\
            Highcharts.chart('"+div_id+"', {\
                chart: {\
                    type: 'column'\
                },\
                title: {\
                    text: '"+titulo+"',\
                    align: 'center'\
                },\
                xAxis: {\
                    categories: ["+categorias+"]\
                },\
                yAxis: {\
                    min: 0,\
                    title: {\
                        text: 'Porcentaje'\
                    }\
                },\
                tooltip: {\
                    pointFormat: '<span style=\"color:{series.color}\">{series.name}</span>' +\
                        ': <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',\
                    shared: true\
                },\
                plotOptions: {\
                    column: {\
                        stacking: 'percent',\
                        dataLabels: {\
                            enabled: true,\
                            format: '{point.percentage:.0f}%'\
                        }\
                    }\
                },\
                series: [\
                    {\
                        name: 'Aprobados',\
                        data: ["+aprobados+"]\
                    }, {\
                        name: 'Observados',\
                        data: ["+observados+"]\
                    }, {\
                        name: 'Pendientes',\
                        data: ["+pendientes+"]\
                    }\
                ]\
            });\
            "
    return script

def get_grafico_pie(titulo, objetos, div_id):
    datos = ''
    for obj in objetos:
        datos += "['"+obj.descripcion+"', "+str(obj.datos_objeto.asignados)+"],"


    script = "\
        Highcharts.chart('"+div_id+"', {\
            chart: {\
                type: 'pie',\
                options3d: {\
                    enabled: true,\
                    alpha: 45,\
                    beta: 0\
                }\
            },\
            title: {\
                text: '"+titulo+"',\
                align: 'center'\
            },\
            accessibility: {\
                point: {\
                    valueSuffix: '%'\
                }\
            },\
            tooltip: {\
                pointFormat: '{series.name}: <\b>{point.percentage:.1f}%</b>'\
            },\
            plotOptions: {\
                pie: {\
                    allowPointSelect: true,\
                    cursor: 'pointer',\
                    depth: 35,\
                    dataLabels: {\
                        enabled: true,\
                        format: '{point.name}'\
                    }\
                }\
            },\
            series: [{\
                type: 'pie',\
                name: 'Share',\
                data: ["+datos+"]\
            }]\
        });\
    "
    return script