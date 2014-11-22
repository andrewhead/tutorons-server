$(function () {	

	var DATA_FILE_PATH = "./data/309424.lines.json";

	linetype_2_color = {
        "text": "red",
        "code": "blue",
        "codecommentinline": "green",
        "codecommentlong": "pink"
    };

 	// width and height
 	var width = 500;
 	var height = '100%'; // would depend on number of responses

	var svg = d3.select("#search_bars")
				.append("svg")
				.attr("width", width)
				.attr("height", height);

	d3.json(DATA_FILE_PATH, function(error, data) {
		console.log(error);
		var responses = svg.selectAll("g")
						.data(data)
						.enter()
						.append("g")

		var bars = responses.selectAll("rect")
						.data(function(d) { return d.lines; })
						.enter()
						.append("rect");

	    var bar_width = 20;
	    var bar_height = 50;
	    var bar_horizontal_padding = 1;
	    var bar_vertical_padding = 5;
		var bar_attributes = bars
			.attr("x", function (d, i) { return i * (bar_width + bar_horizontal_padding); })
			.attr("y", function (d, i, j) { return j * (bar_height + bar_vertical_padding); })
			.attr("width", bar_width)
			.attr("height", bar_height)
			.style("fill", function(d) { return linetype_2_color[d.type_]; });

        var refCounts = {};
        for (var i = 0; i < data.length; i++) {
            var lines = data[i].lines;
            for (var j = 0; j < lines.length ; j++) {
                var references = lines[j].references;
                for (var k = 0; k < references.length; k++) {
                    var ref = references[k];
                    if (!(ref in refCounts)) {
                        refCounts[ref] = 0;
                    }
                    refCounts[ref]++;
                }
            }
        }

        var acw = 800;
        var ach = 400;
        var ac_bar_width = 20;
        var ac_bar_horiz_padding = 5;

        var acSvg = d3.select("#aggregate_chart")
                    .append("svg")
                    .attr("width", acw)
                    .attr("height", ach);

        var sortedRefCounts = d3.entries(refCounts).sort(function(a, b) {
            return b.value - a.value;
        })
        
		var acBars = acSvg.selectAll("rect")
                    .data(sortedRefCounts)
                    .enter()
                    .append("rect")
                    .attr("x", function (d, i) { return i * (ac_bar_width + ac_bar_horiz_padding); })
                    .attr("y", function (d) { return ach - (10 * d.value); })
                    .attr("width", ac_bar_width)
                    .attr("height", function(d) { return 10 * d.value; })
                    .style("fill", function(d) { return "blue"; });
	});
});
