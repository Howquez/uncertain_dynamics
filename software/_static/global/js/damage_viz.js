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
            return 'Wenn Ihre Gruppe <b>' + this.x*10 +
                '%</b> der gesamten Ausstattung (über alle Gruppenmitglieder hinweg) dem Gruppenkonto zuweist, würde das im Schadensfall zu einem Verlust von <b>' + this.y + '%</b> Ihrer Ausstattung führen.';
        }
    },

    xAxis: {
        categories: [0,10,20,30,40,50,60,70,80,90,100],
        title: {
        		text : "Anteil der gesamten Ausstattung (über alle Gruppenmitglieder hinweg) der dem Gruppenkonto zugewiesen wurde."
        },
        labels: {
            format: '{value}%'
        },
    },

    yAxis: {
        title: {
        		text : "Schaden als Anteil an Ihrer Ausstattung"
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
        name: 'Schaden',
        data: [-50,-45,-40,-35,-30,-25,-20,-15,-10,-5,0]
    }]
});