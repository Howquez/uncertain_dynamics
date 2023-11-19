Highcharts.chart('damage_viz', {
    chart: {
        type: 'area',
        backgroundColor: "transparent"
    },

    title: {
        text: ""
    },

    exporting: {
				enabled: false
    },

    tooltip: {
        formatter: function () {
            return 'If your group contributes <b>' + this.x +
                '%</b> a damage would cause a loss of <b>' + this.y + '%</b> of your stock.';
        }
    },

    xAxis: {
        categories: [0,10,20,30,40,50,60,70,80,90,100],
        title: {
        		text : "Share of Total Endowments Contributed"
        },
        labels: {
            format: '{value}%'
        },
    },

    yAxis: {
        title: {
        		text : "Possible Damage of Stock in Percent"
        },
        labels: {
            format: '{value}%'
        },
    },

    legend: {
    		enabled: false
    },

    plotOptions: {
        series: {
            fillColor: {
                linearGradient: [0, 0, 0, 300],
                stops: [
                    [0, "rgba(217, 83, 79, 0.5)"],
                    [1, "rgba(217, 83, 79, 0.05)"]
                ]
            },
            color: "#d9534f",
            marker: {
                enabled: false
            }
        }
    },

    series: [{
        name: 'Possible Damage',
        data: [50,45,40,35,30,25,20,15,10,5,0]
    }]
});