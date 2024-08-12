Highcharts.setOptions({
    colors: [
        '#2680D1', '#FF4187', '#FFB020', '#DDDF00', '#24CBE5', '#64E572',
        '#FF9655', '#FFF263', '#6AF9C4'
    ]
});

Highcharts.chart('container', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Estado de Evidencias',
        align: 'center'
    },
    xAxis: {
        categories: ['Condiciones', 'Requerimientos', 'Recomendaciones', 'Renovaciones']
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Porcentaje'
        }
    },
    tooltip: {
        pointFormat: '<span style="color:{series.color}">{series.name}</span>' +
            ': <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
        shared: true
    },
    plotOptions: {
        column: {
            stacking: 'percent',
            dataLabels: {
                enabled: true,
                format: '{point.percentage:.0f}%'
            }
        }
    },
    series: [
        {
            name: 'Aprobados',
            data: [4, 10, 3, 10]
        }, {
            name: 'Observados',
            data: [2, 3, 10, 2]
        }, {
            name: 'Pendientes',
            data: [15, 1, 1, 2]
        }
    ]
});


Highcharts.chart('pieChart', {
    chart: {
        type: 'pie',
        options3d: {
            enabled: true,
            alpha: 45,
            beta: 0
        }
    },
    title: {
        text: 'Medios de Verificación Asignados',
        align: 'center'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            depth: 35,
            dataLabels: {
                enabled: true,
                format: '{point.name}'
            }
        }
    },
    series: [{
        type: 'pie',
        name: 'Share',
        data: [
            ['Condiciones', 10],
            ['Requerimientos', 4],
            ['Recomendaciones', 2],
            ['Renovaciones', 2]
        ]
    }]
});