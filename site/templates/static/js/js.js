
var bg_color = []
var border_color = []

function gera_cor(qtd=1){

    for(let i = 0; i < qtd; i++){
        let r = Math.random() * 255;
        let g = Math.random() * 255;
        let b = Math.random() * 255;
        bg_color.push(`rgba(${r}, ${g}, ${b}, ${0.2})`)
        border_color.push(`rgba(${r}, ${g}, ${b}, ${1})`)
    }

}


function renderiza_tmp(url){
    fetch(url, {
        method: 'get',
    }).then(function(result) {
        return result.json();
    }).then(function(data) {
        const ctx = document.getElementById('tmp').getContext('2d');

        // Check if the chart already exists and destroy it
        if (Chart.getChart(ctx)) {
            Chart.getChart(ctx).destroy();
        }

        const myChart = new Chart(ctx, {
            type: 'bar',
            options: {
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';

                                if (label) {
                                    label += ': ';
                                }

                                if (context.parsed.y !== null) {
                                    // Include both data_lux and data_alunos values in the label
                                    label = 'Temperatura: ' + context.dataset.data[context.dataIndex] + ',  Alunos: ' + context.dataset.data_alunos[context.dataIndex];
                                }

                                return label;
                            }
                        }
                    },
                    legend:{
                        labels:{
                          boxWidth: 0.
                        }
                    }
                }
            },
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Média de Celsius',
                    data: data.data_temperatura, // Assuming data_lux is available in your data
                    data_alunos: data.data_alunos, // Assuming data_alunos is available in your data
                    backgroundColor: bg_color,
                    borderColor: border_color,
                    borderWidth: 1
                }]
            },
        });
    });
}


function renderiza_hum(url){
    fetch(url, {
        method: 'get',
    }).then(function(result) {
        return result.json();
    }).then(function(data) {
        const ctx = document.getElementById('hum').getContext('2d');

        // Check if the chart already exists and destroy it
        if (Chart.getChart(ctx)) {
            Chart.getChart(ctx).destroy();
        }

        const myChart = new Chart(ctx, {
            type: 'bar',
            options: {
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';

                                if (label) {
                                    label += ': ';
                                }

                                if (context.parsed.y !== null) {
                                    // Include both data_lux and data_alunos values in the label
                                    label = 'Umidade: ' + context.dataset.data[context.dataIndex] + ',  Alunos: ' + context.dataset.data_alunos[context.dataIndex];
                                }


                                return label;
                            }
                        }
                    },
                    legend:{
                        labels:{
                          boxWidth: 0.
                        }
                    }
                }
            },
            data: {

                labels: data.labels,
                datasets: [{
                    label: 'Média de Umidade',
                    data: data.data_humidade, // Assuming data_lux is available in your data
                    data_alunos: data.data_alunos, // Assuming data_alunos is available in your data
                    backgroundColor: bg_color,
                    borderColor: border_color,
                    borderWidth: 1
                }]
            },
        });
    });
}


function renderiza_lux(url) {
    fetch(url, {
        method: 'get',
    }).then(function(result) {
        return result.json();
    }).then(function(data) {
        const ctx = document.getElementById('lux').getContext('2d');

        // Check if the chart already exists and destroy it
        if (Chart.getChart(ctx)) {
            Chart.getChart(ctx).destroy();
        }

        const myChart = new Chart(ctx, {
            type: 'bar',
            options: {
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';

                                if (label) {
                                    label += ': ';
                                }

                                if (context.parsed.y !== null) {
                                    // Include both data_lux and data_alunos values in the label
                                    label = 'Lux: ' + context.dataset.data[context.dataIndex] + ',  Alunos: ' + context.dataset.data_alunos[context.dataIndex];
                                }


                                return label;
                            }
                        }
                    },
                    legend:{
                        labels:{
                          boxWidth: 0.
                        }
                    }
                }
            },
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Média de Lux',
                    data: data.data_lux, // Assuming data_lux is available in your data
                    data_alunos: data.data_alunos, // Assuming data_alunos is available in your data
                    backgroundColor: bg_color,
                    borderColor: border_color,
                    borderWidth: 1
                }]
            },
        });
    });
}



function renderiza_volts(url){
    fetch(url, {
        method: 'get',
    }).then(function(result) {
        return result.json();
    }).then(function(data) {
        const ctx = document.getElementById('volts').getContext('2d');

        // Check if the chart already exists and destroy it
        if (Chart.getChart(ctx)) {
            Chart.getChart(ctx).destroy();
        }

        const myChart = new Chart(ctx, {
            type: 'bar',
            options: {
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';

                                if (label) {
                                    label += ': ';
                                }

                                if (context.parsed.y !== null) {
                                    // Include both data_lux and data_alunos values in the label
                                    label = 'Volts: ' + context.dataset.data[context.dataIndex] + ',  Alunos: ' + context.dataset.data_alunos[context.dataIndex];
                                }


                                return label;
                            }
                        }
                    },
                    legend:{
                        labels:{
                          boxWidth: 0.
                        }
                    }
                }
            },
            data: {

                labels: data.labels,
                datasets: [{
                    label: 'Média de Volts',
                    data: data.data_volts, // Assuming data_lux is available in your data
                    data_alunos: data.data_alunos, // Assuming data_alunos is available in your data
                    backgroundColor: bg_color,
                    borderColor: border_color,
                    borderWidth: 1
                }]
            },
        });
    });
}
/*
function renderiza_combo(url){

    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

        const ctx = document.getElementById('combo').getContext('2d');
        //var cores_lux = gera_cor(qtd=12)
        if (Chart.getChart(ctx)) {
            Chart.getChart(ctx).destroy();
         }
        const myChart = new Chart(ctx, {

            data: {

                datasets: [{
                    type: 'bar',
                    label: 'Média em Lux',
                    data: data.data_lux,
                    backgroundColor: bg_color,
                    borderColor: border_color,
                    borderWidth: 1
                }, {
                    type: 'line',
                    label: 'Média da Humidade',
                    data: data.data_humidade,
                    backgroundColor: bg_color,
                    borderColor: border_color,
                    borderWidth: 1
                }, {
                    type: 'bar',
                    label: 'Média em Célsius',
                    data: data.data_temperatura,
                    backgroundColor: bg_color,
                    borderColor: border_color,
                    borderWidth: 1
                }],
                 labels: data.labels,
            },
        });
    })
}
*/