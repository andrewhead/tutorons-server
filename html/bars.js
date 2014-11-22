$(function () {	

	var DATA_FILE_PATH = "./data/309424.lines.json";

    var code_colors = d3.scale.category10()
        .domain(["text", "code", "codecommentinline", "codecommentlong"])

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

	    var bar_width = 10;
	    var bar_height = 20;
	    var bar_horizontal_padding = 1;
	    var bar_vertical_padding = 5;
		var bar_attributes = bars
            .attr("class", "line_rect")
			.attr("x", function (d, i) { return i * (bar_width + bar_horizontal_padding); })
			.attr("y", function (d, i, j) { return j * (bar_height + bar_vertical_padding); })
			.attr("width", bar_width)
			.attr("height", bar_height)
			.style("fill", function(d) { return code_colors(d.type_); });

        function brighten_lines_with_reference(ref, brightness) {
            d3.selectAll(".line_rect").filter(function(d) { 
                return (d.references.indexOf(ref) >= 0); 
            }).style("fill", function(d) {
                return d3.rgb(code_colors(d.type_)).brighter(brightness);
            });
        };

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
        };

        function px_to_num(str) {
            return Number(str.replace("px", ""));
        };

        var REF_COUNT = 20;  // 20 because of category20 colors for D3
        var ref_counts = extract_reference_counts(data);
        var sorted_ref_counts = d3.entries(ref_counts).sort(function(a, b) {
            return b.value - a.value;
        }).splice(0, REF_COUNT);
        var ref_colors = d3.scale.category20b()
            .domain(d3.keys(sorted_ref_counts));
        
        var ac_margin = {top: 20, bottom: 70, left: 20, right: 20};
        var aggregate_chart = d3.select("#aggregate_chart");
        var acw = px_to_num(aggregate_chart.style("width"));
        var ach = px_to_num(aggregate_chart.style("height"));
        var x_scale = d3.scale.ordinal()
            .domain(sorted_ref_counts.map(function(d) { return d.key; }))
            .rangeRoundBands([ac_margin.left, acw - ac_margin.right], .1);

        var ac_svg = aggregate_chart
            .append("svg")
            .attr("width", acw)
            .attr("height", ach);

        var max_count = d3.max(d3.entries(ref_counts), function(d) { return d.value; })
        var y_scale = d3.scale.linear()
            .domain([0, max_count])
            .range([ach - ac_margin.bottom, ac_margin.top]);
        var h_scale = d3.scale.linear()
            .domain([0, max_count])
            .range([0, ach - (ac_margin.top + ac_margin.bottom)]);

		var ac_bars = ac_svg.selectAll("rect")
            .data(sorted_ref_counts)
            .enter()
            .append("rect")
            .attr("x", function (d, i) { return x_scale(d.key); })
            .attr("y", function (d) { return y_scale(d.value); })
            .attr("width", x_scale.rangeBand())
            .attr("height", function(d) { return h_scale(d.value); })
            .style("fill", function(d) { return ref_colors(d.key) })
            .on("mouseover", function(d) {
                brighten_lines_with_reference(d.key, 1.5);
                d3.select(this).style("fill", function(d) { 
                    return d3.rgb(ref_colors(d.key)).brighter(); 
                });
            })
            .on("mouseout", function(d) {
                brighten_lines_with_reference(d.key, 0);
                d3.select(this).style("fill", function(d) { 
                    return d3.rgb(ref_colors(d.key)); 
                });
            });
        
        var ac_labels = ac_svg.selectAll("text")
            .data(sorted_ref_counts)
            .enter()
            .append("text")
            .attr("text-anchor", "end")
            .attr("class", "ac_label")
            .text(function(d) { return d.key; })
            .attr("transform", function(d) {
                return "translate(" + 
                    Math.floor(x_scale(d.key) + x_scale.rangeBand() / 2) + "," + 
                    (ach - ac_margin.bottom + 12) + 
                    ")rotate(-40)";
            });

        var yAxis = d3.svg.axis()
            .scale(y_scale)
            .ticks(4)
            .orient("left");
        ac_svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(" + ac_margin.left + ",0)")
            .call(yAxis);
	});
});
