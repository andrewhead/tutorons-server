$(function () {	

	var DATA_FILE_PATH = "./data/309424.lines.json";

	linetype_2_color = {
        "text": "red",
        "code": "blue",
        "codecommentinline": "green",
        "codecommentlong": "pink"
    };

 	// width and height
	var svg = d3.select("#search_bars")
        .append("svg")
        .attr("width", "100%")
        .attr("height", "100%");

	d3.json(DATA_FILE_PATH, function(error, data) {
		var responses = svg.selectAll("g")
            .data(data)
            .enter()
            .append("g")

		var bars = responses.selectAll("rect")
            .data(function(d) { return d.lines; })
            .enter()
            .append("rect");

	    var bar_width = 15;
	    var bar_height = 20;
	    var bar_horizontal_padding = 1;
	    var bar_vertical_padding = 5;
		var bar_attributes = bars
			.attr("x", function (d, i) { return i * (bar_width + bar_horizontal_padding); })
			.attr("y", function (d, i, j) { return j * (bar_height + bar_vertical_padding); })
			.attr("width", bar_width)
			.attr("height", bar_height)
			.style("fill", function(d) { return linetype_2_color[d.type_]; });

        function extract_reference_counts(data) {
            var ref_counts = {};
            for (var i = 0; i < data.length; i++) {
                var lines = data[i].lines;
                for (var j = 0; j < lines.length ; j++) {
                    var references = lines[j].references;
                    for (var k = 0; k < references.length; k++) {
                        var ref = references[k];
                        if (!(ref in ref_counts)) {
                            ref_counts[ref] = 0;
                        }
                        ref_counts[ref]++;
                    }
                }
            }
            return ref_counts;
        }

        function px_to_num(str) {
            return Number(str.replace("px", ""));
        }

        var ref_counts = extract_reference_counts(data);
        var sorted_ref_counts = d3.entries(ref_counts).sort(function(a, b) {
            return b.value - a.value;
        })
        
        var aggregate_chart = d3.select("#aggregate_chart");
        var acw = px_to_num(aggregate_chart.style("width"));
        var ach = px_to_num(aggregate_chart.style("height"));
        var ac_bar_width = 20;
        var ac_bar_horiz_padding = 5;
        var ac_edge_padding = 20;

        var acSvg = aggregate_chart
            .append("svg")
            .attr("width", acw)
            .attr("height", ach);

        var max_count = d3.max(d3.entries(ref_counts), function(d) { return d.value; })
        var yScale = d3.scale.linear()
            .domain([0, max_count])
            .range([ach - ac_edge_padding, ac_edge_padding]);
        var hScale = d3.scale.linear()
            .domain([0, max_count])
            .range([0, ach - ac_edge_padding * 2]);

		var acBars = acSvg.selectAll("rect")
            .data(sorted_ref_counts)
            .enter()
            .append("rect")
            .attr("x", function (d, i) { 
                return ac_edge_padding + i * (ac_bar_width + ac_bar_horiz_padding); 
            })
            .attr("y", function (d) { return yScale(d.value); })
            .attr("width", ac_bar_width)
            .attr("height", function(d) { return hScale(d.value); })
            .style("fill", function(d) { return "blue"; });
        
        var yAxis = d3.svg.axis()
            .scale(yScale)
            .ticks(4)
            .orient("left");
        acSvg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(" + ac_edge_padding + ",0)")
            .call(yAxis);
	});
});
