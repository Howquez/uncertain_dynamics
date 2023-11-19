// define seq() function as in R
	function* seq( start, end, step = 1 ){
	  if( end === undefined ) [end, start] = [start, 0];
	  for( let n = start; n <= end; n += step ) yield n;
	}

// initiate vars from python
	let flat_fee = js_vars.flat_fee || 0;
	let exchange_rate = js_vars.exchange_rate;
	let num_rounds  = js_vars.num_rounds;
	let euros = js_vars.euros || 0;

	var plot_height = 4;

// create dummy data for instructions
    if (template == "instructions"){
        current_round = 4;
        endowments = [20, 21, 27, 28]
    }

// get categories, i.e. the rounds
	var category = Array.from(seq(1, current_round));
	for(var i=0;i<category.length;i++){
		category[i]="Period #"+category[i];
	}

// create participation fee series
	var flat = Array(current_round).fill(flat_fee)


// determine which series to be displayed
	var series = endowments;
	var suffix = " Points";
	var plot_line_width = 1;
	var show_in_legend = false;
	var max = num_rounds;

	if (template == "decision"){
	    series = stock;
	    plot_height = 5;
	}

	if (template == "results"){
	    series = stock;
	    series.shift();
		plot_line_width = 1;
		plot_height = 4;
		max = num_rounds - 1;
	}

	if (template == "final"){
		series = euros;
		suffix = " Euro";
		plot_line_width = 0;
		show_in_legend = true;
		plot_height = 4;
		max = num_rounds - 1;
	}

	// console.log(current_round);
	// console.log(endowments);
	// console.log(category);


var chart = Highcharts.chart('container', {
    chart: {
        type: "areaspline",
        backgroundColor: "transparent",
        height: (plot_height / 16 * 100) + '%' // 16:9 ratio
    },
    title: {
        text: ""
    },
    exporting: {
				enabled: false
	},
    
    xAxis: {
        max: max,
        categories: category,
        labels: {
		   enabled: true,
		   formatter: function () {
                return "End"
            }
		},
		tickPositions: [max],
		plotLines: [{
        	zIndex: 5,
                value: max,
                color: 'grey',
                //dashStyle: 'shortdash',
                width: plot_line_width,
        }]
    },
    yAxis: {
    	gridLineWidth: 0,
        minorGridLineWidth: 0,
        title: {
            text: ""
        },
        plotLines: [{
        	zIndex: 5,
                value: 20,
                color: 'grey',
                dashStyle: 'shortdash',
                width: plot_line_width,
        }]
    },
    tooltip: {
        shared: true,
        valueSuffix: suffix
    },
    credits: {
        enabled: false
    },
    plotOptions: {
    	series: {
    	    fillColor: {
                linearGradient: [0, 0, 0, series[series.length - 1]*1.5],
                stops: [
                    [0, "rgba(62,56,242,0.5)"],
                    [1, "rgba(62,56,242,0.1)"]
                ]
            },
    		color: "#3E38F2",
    		marker: {
                enabled: false
            }
    	},
        areaspline: {
        	stacking: "normal",
        	//fillOpacity: 0.33
        },
    },
    series: [{
        name: "Earnings",
        data: series,
        showInLegend: false //show_in_legend
    },{
        name: "Showup Fee",
        data: flat,
        color: "#00fad1",
        showInLegend: false, //show_in_legend,
        visible: false //template == "final"
    }]
});

if (template != "decision"){
    chart.tooltip.refresh([chart.series[0].points[current_round - 1]]);
}