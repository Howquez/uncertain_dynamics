// define seq() function as in R
	function* seq( start, end, step = 1 ){
	  if( end === undefined ) [end, start] = [start, 0];
	  for( let n = start; n <= end; n += step ) yield n;
	}

// initiate vars from python
	let num_rounds  = js_vars.num_rounds;
	series = stock;

// get categories, i.e. the rounds
	var category = Array.from(seq(1, current_round));
	for(var i=0;i<category.length;i++){
		category[i]="Period #"+category[i];
	}

// tick positions
    var max = Math.max.apply(null, stock)
    var min = Math.min.apply(null, stock)
    if (min >  0) {
        min = 0
    }

// line col
    var line_col = "#0d6efd"; //"#198754";
    if (series[current_round-1] < 0) {
        line_col = "#dc3545"
    }

// manipulate series
series[0] = 20;

var chart = Highcharts.chart('container', {
    chart: {
        backgroundColor: "transparent",
        height: (9 / 16 * 100) + '%', // 16:9 ratio
        marginBottom: 5,
        marginLeft: 0,
    },
    title: {
        text: ""
    },
    exporting: {
				enabled: false
	},
    
    xAxis: {
        categories: category,
        lineWidth: 0,
        tickWidth: 0,
        labels: {
		   enabled: false
		}
    },
    yAxis: {
    	gridLineWidth: 0,
        minorGridLineWidth: 0,
        opposite: true,
        labels: {
            enabled: true,
            formatter: function() {
                        	if (this.value == 0 || this.isLast) {
                          	return this.value
                          }
                        }
        },
        tickPositions: [min, 0, max],
        plotLines: [{
                value: 0,
                width: 0.5,
                color: '#aaa',
                dashStyle: 'shortdash',
                zIndex: 0
              }],
        title: {
            text: ""
        }
    },
    tooltip: {
        enabled: false
    },
    credits: {
        enabled: false
    },
    plotOptions: {
    	series: {
    		color: line_col,
    		marker: {
                enabled: false
            }
    	},
    },
    series: [{
        name: "Earnings",
        data: series,
        showInLegend: false
    }]
});