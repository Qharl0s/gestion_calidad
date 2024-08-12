Highcharts.setOptions({
    colors: [
        '#2680D1', '#FF4187', '#FFB020', '#DDDF00', '#24CBE5', '#64E572',
        '#FF9655', '#FFF263', '#6AF9C4'
    ]
});


Highcharts.chart('condiciones_barras', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Evidecias de Condiciones',
        align: 'left'
    },
    subtitle: {
        text: 'Source: <a href="http://localhost:8000/condiciones/">Condiciones</a>',
        align: 'left'
    },
    xAxis: {
        categories: ['Condición 1', 'Condición 2', 'Condición 3', 'Condición 4', 'Condición 5', 'Condición 6', 'Condición 7', 'Condición 8']
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
            data: [4, 12, 3, 1, 3, 2, 0, 6]
        }, {
            name: 'Observados',
            data: [2, 1, 0, 12, 1, 1, 0, 0]
        }, {
            name: 'Pendientes',
            data: [5, 2, 8, 2, 1, 12, 3, 0]
        }
    ]
});

