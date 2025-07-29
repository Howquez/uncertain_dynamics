Highcharts.chart('mpcr_viz', {
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
            return 'Wenn Sie <b>' + this.x*10 +
                "%</b> der gesamten Ausstattung der Gruppe besitzen, dann wird Ihnen am Ende der Periode ein prozentualer Anteil von <b>" + this.y + '%</b> aller Punkte im Gruppenkonto ausgeschüttet.';
        }
    },

    xAxis: {
        categories: [0,10,20,30,40,50,60,70,80,90,100],
        title: {
        		text : "Ihr Anteil der gesamten Ausstattung der Gruppe"
        },
        labels: {
            format: '{value}%'
        },
    },

    yAxis: {
        title: {
        		text : "Ausschüttungsrate aus dem Gruppenkonto"
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
                    [0, "rgba(2,117,216, 0.5)"],
                    [1, "rgba(2,117,216, 0.05)"]
                ]
            },
            color: "#0275d8",
            marker: {
                enabled: false
            }
        }
    },

    series: [{
        name: 'Your Quota',
        data: [37.5,36.5,35.5,34.5,33.5,32.5,31.5,30.5,29.5,28.5,27.5]
    }]
});