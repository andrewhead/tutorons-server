$(function () {	

    var code_colors = d3.scale.category10()
        .domain(["text", "code", "codecommentinline", "codecommentlong"])

    /* JQuery UI setup */
    $(".keep_cont").resizable({
        'containment': '#keep_col',
    });

    /* Routines for processing incoming data */
    function preprocessData(data) {

        function addSpans(body) {
            var code = body.children("pre");
            if (code.length > 0) {
                code.each(function() {
                    $(this).html(function(_, text) {
                        return text.replace(/^<code>/, "<span>")
                            .replace(/(\r\n|\n|\r)/gm, "</span>\r\n<span>")
                            .replace(/<\/code>$/, "</span>");
                    });
                });
            }
            var par = body.children("p");
            if (par.length > 0) {
                par.each(function() {
                    $(this).html(function(_, text) {
                        return "<span>" + text.replace(/\.\s/gm, "</span>\r\n<span>") + "</span>";
                    });
                });
            }
            return body;
        }

        function highlightCode(body) {
           body.find("pre").each(function(_, block) {
               hljs.highlightBlock(block);
           });
        }

        /* Add spans for each line of each answer body so we can look move the
         * preview window to focus precisely at that line. */
        for (var i = 0; i < data.length; i++) {
            data[i].body = addSpans($("<div>" + data[i].body + "</div>"));
            highlightCode(data[i].body);
        }
    }

	function displayData(data) {
		
	    var bar_width = 30;
	    var bar_height = 15;
	    var bar_horizontal_padding = 5;
	    var bar_vertical_padding = 0;

        /* Build search bars */
        var svg = d3.select("#search_bars")
            .append("svg")
            .attr("width", data.length * (bar_width + bar_horizontal_padding))
            //.attr("height", data.length * (bar_height + bar_vertical_padding));
            .attr("height", d3.max(data, function(d) { return d.lines.length }) * 
                    (bar_height + bar_vertical_padding));

        var responses = svg.selectAll("g")
            .data(data)
            .enter()
            .append("g")
            .attr("class", "response_g")
            .each(function(d,i) {
                d.index = i;
            });

		var lines = responses.selectAll("g")
            .data(function(d) { return d.lines; })
            .enter()
            .append("g")
            .attr("class", "line_g")
            .attr("transform", function(d, i, j) { 
                return "translate(" +
                    j * (bar_width + bar_horizontal_padding) + "," +
                    i * (bar_height + bar_vertical_padding) + ")";
            })
            .each(function(d,i){
                d.index = i;
            });

        function setPreview(selector, body, line) {
            preview = $(selector);
            preview.empty();
            preview.append(body);
            var textSpan = preview.find('span:contains(' + line + ')');

            /* We don't scroll to lines with less than 5 characters, as they might be
             * a false match to another blank line or "try {" line ! */
            if (textSpan.length > 0 && line.length > 10) {

                /* Move highlighting to new terms */
                preview.find('span').removeClass("highlight");
                textSpan.addClass("highlight");

                /* Animate a scroll to the current line */
                preview.stop(true)
                    .animate({
                        scrollTop: textSpan.offset().top - 
                            preview.offset().top + preview.scrollTop() -
                            preview.height() / 3,
                        duration: 300
                });
            }
        }

        var bars = lines.append("rect")
            .attr("class", "line_rect")
			.attr("width", bar_width)
			.attr("height", bar_height)
			.style("fill", function(d) { return code_colors(d.type_); })
            .style("stroke", "black")
            .style("pointer-events", "all")
            .on("mouseover", function(d) {
                var body = d3.select(this.parentNode.parentNode).datum().body;
                setPreview("#preview_pane", body, d.text);
            })
            .on("mousedown", dragStart)
            .on("mouseup", dragEnd)
            .on("click", function(d, i){
                //  flip value of sortOrder
                sortOrder = !sortOrder;
                var rs = d3.selectAll(".response_g")
                    .each(function(d, i){
                        sortBars(this);
                    });
            });

        var dragStartParent, dragEndParent;
        var dragStartLine, dragEndLine;
        
        function dragStart(d, i) {
            dragEndParent = undefined;
            dragEndLine = undefined;
            dragStartParent = d3.select(this.parentNode.parentNode);
            dragStartLine = d3.select(this.parentNode);
        };

        function dragEnd(d, i) {

            function posFromTranslate(string) {
                tokens = string.split(/[(,)]/);
                return {
                    x: tokens[1],
                    y: tokens[2]
                };
            }

            dragEndParent = d3.select(this.parentNode.parentNode);
            dragEndLine = d3.select(this.parentNode);
            if (dragEndParent.datum().index === dragStartParent.datum().index) {
                startPos = posFromTranslate(dragStartLine.attr("transform"));
                endPos = posFromTranslate(dragEndLine.attr("transform"));
                var rectX = startPos.x;
                var rectY = Math.min(startPos.y, endPos.y);
                var rectW = Number(d3.select(this).attr("width"));
                var rectH = Math.abs(startPos.y - endPos.y) + Number(d3.select(this).attr("height"));
                dragEndParent.append("rect")
                    .attr("x", rectX)
                    .attr("y", rectY)
                    .attr("width", rectW)
                    .attr("height", rectH)
                    .style("fill-opacity", 0)
                    .style("stroke", "black")
                    .style("stroke-width", 5)
                    .style("pointer-events", "none");
            }

            /* Keep only the lines in the body that have been selected by the user */
            var body = $(dragStartParent.datum().body).clone();
            var startIndex = Math.min(dragStartLine.datum().index, dragEndLine.datum().index);
            var endIndex = Math.max(dragStartLine.datum().index, dragEndLine.datum().index);
            for (var i = startIndex; i <= endIndex; i++) {
                var lineText = dragStartParent.datum().lines[i].text;
                if (lineText.length > 0) {
                    var spans = body.find('span:contains(' + lineText + ')')
                            .addClass('keep');
                }
            }
            body.find("pre > span").not(".keep").remove();
            body.find("p > span").not(".keep").remove();
            body.find("p:not(:has(*))").remove();
            body.find("pre:not(:has(*))").remove();
            body.css("height", "150px")
                .css("overflow", "auto");
            body.html(body.html().replace(/^\s*[\r\n]/gm, ""));

            var newEntry = $("<div></div>");
            var header = newEntry.append("<h3>" + window.query + "</h3>")
                .prop("contenteditable", "true")
                .on("keypress", function(e) {
                    if (e.keyCode == 13) {
                        $("#target").blur().next().focus();
                        return false;
                    }
                });
            newEntry.append(body);
            $("#keep_col").prepend(newEntry);
            newEntry.accordion({
                collapsible: true,
                heightStyle: "content"
            });

            dragStartParent = undefined;
            dragStartLine = undefined;
        };

        var sortOrder = false;
        var sortBars = function(response) {
            //  flip value of sortOrder
            //sortOrder = !sortOrder;
            d3.selectAll(response.childNodes)
                .sort(function(a, b) {
                    if (sortOrder) {
                        // sort by type
                        if (a.type_ === b.type_)
                            return d3.ascending(a.index, b.index);
                        else
                            return d3.ascending(a.type_, b.type_);
                    } else {
                        // return to original order
                        return d3.ascending(a.index, b.index);
                    }
                })
                .transition()
                //.delay(function(d, i) {
                    //return i * 50;
                //})
                .duration(500)
                .attr("transform", function(d, i) { 
                    var transform = d3.transform(d3.select(this).attr("transform")).translate;
                    var xPosition = transform[0];
                    var yPosition = transform[1];
                    return "translate(" +
                        xPosition + "," + 
                        //yPosition + ")";
                        i * (bar_height + bar_vertical_padding) + ")";
                });
        };

        var flags = lines.append("svg")
            .attr("width", bar_width)
            .attr("height", bar_height)
            .append("use")
            .attr("class", "flag")
            .attr("xlink:href", "static/skim/img/sprite.svg#media-record")
            .style("fill", "#fff")
            .style("fill-opacity", 0.0)
            .style("pointer-events", "none"); // do not block mouse events

        function brighten_lines_with_reference(ref, brightness) {
            d3.selectAll(".line_rect").filter(function(d) { 
                return (d.references.indexOf(ref) >= 0); 
            }).style("fill", function(d) {
                return d3.rgb(code_colors(d.type_)).brighter(brightness);
            });
        };

        function show_flags_for_selected_references() {

            function color_flags_with_reference(ref, color) {
                d3.selectAll(".flag").filter(function(d) { 
                    return (d.references.indexOf(ref) >= 0); 
                }).style("fill", function(d) {
                    return d3.rgb(color);
                }).style("fill-opacity", 1.0);
            }

            /* Start by hiding all flags */
            d3.selectAll(".flag").style("fill-opacity", 0.0);

            /* Fill in flag colors for selected deps, starting with least-used deps.
             * These will get overwritten by the selected most-used deps. */
            var selected = d3.selectAll(".dep_bar.selected");
            if (selected.length > 0) {
                selected[0].reverse();
                selected.each(function(d) {
                    color_flags_with_reference(d.key, ref_colors(d.key));
                });
            }
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

        function color_dep_bar(element) {
            var data = element.data()[0];
            var base_color = ref_colors(data.key);
            element.style("fill", function(d) {
                var brightness = (
                    d3.select(this).classed("selected") || 
                    d3.select(this).classed("hovered")) ? 
                    1.5 : 0;
                return d3.rgb(ref_colors(d.key)).brighter(brightness);
            });
        }

		var ac_bars = ac_svg.selectAll("rect")
            .data(sorted_ref_counts)
            .enter()
            .append("rect")
            .attr("class", "dep_bar")
            .attr("x", function (d, i) { return x_scale(d.key); })
            .attr("y", function (d) { return y_scale(d.value); })
            .attr("width", x_scale.rangeBand())
            .attr("height", function(d) { return h_scale(d.value); })
            .style("fill", function(d) { return ref_colors(d.key) })
            .on("mouseover", function(d) {
                d3.select(this).classed("hovered", true);
                brighten_lines_with_reference(d.key, 1.5);
                d3.select(this).call(color_dep_bar);
            })
            .on("click", function() {
                d3.select(this).classed("selected", function() {
                    return ! d3.select(this).classed("selected");
                });
                show_flags_for_selected_references();
                d3.select(this).call(color_dep_bar);
            })
            .on("mouseout", function(d) {
                d3.select(this).classed("hovered", false);
                brighten_lines_with_reference(d.key, 0);
                d3.select(this).call(color_dep_bar);
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
	};

    /* MAIN */
    preprocessData(data);
    displayData(data);

});
