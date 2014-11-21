
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

	var svg = d3.select("body")
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
	});
    
});
