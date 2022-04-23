function handleHoverInner(item) {
    console.log(item);
}

function handleHoverOuter(evt, item) {
    console.log(evt, item);
}

function updateChart(func, nb = '') {
    $.ajax({
        type: "POST",
        url: '/pir/chart',
        dataType: 'json',
        data: {
            'func': func,
            'size': window.innerWidth
        },
        success: function(data) {
            var ctxL = document.getElementById("chart" + nb).getContext('2d');
            const chartData = {
                type: data.type,
                data: data.data
            }
            new Chart(ctxL, chartData);
        }
    });
}