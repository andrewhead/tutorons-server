$(function () {	

    function setupSearchResults(answers) {
        setupCodeBars(answers);
        setupLegend();
        setupCountChart("#aggregate_chart", answers, "references", class_colors);
        addJavadocsLinks("#aggregate_chart", linksData);
        setupCountChart("#concept_chart", answers, "concepts", concept_colors);
    }
    
    function setupQuestionList(questions, answers) {
 
        function finish() {
            $("#question_panel").fadeOut("slow", function() {
                setupSearchResults(answers, linksData);
            });
        }

        if (window.skipQuestions) {
            /* Only skip questions the first time */
            window.skipQuestions = false;
            finish();
            return;
        }

        /* Flush existing questions first */
        $("#question_panel").fadeIn("slow");        
        var questionList = d3.select("#question_list");
        questionList.selectAll("p, label, input").remove();
        
        questionList.selectAll("input")
            .data(questions)
            .enter()
            .append("p")
            .append("label")
                .attr("for", function(d,i) { return 'q' + d.id_; })
                .html(function(d) { return d.title; })
            .append("input")
                .attr("type", "checkbox")
                .attr("name", "question")
                .attr("id", function(d,i) { return 'q' + d.id_; })
            ;
        d3.select("#question_done_button")
            .on("click", function() {
                // build set (dictionary) of selected question id's
                var selected_qids = {};
                d3.selectAll("input[type=checkbox][name=question]:checked")
                    .each(function(d,i) {
                        selected_qids[ d.id_ ] = true;
                    });
                // filter answers
                answers = answers.filter(function(elem) {
                    return (selected_qids.hasOwnProperty(elem.qid_));
                });
                finish();
            });
    }

	function setupCodeBars(data) {

	    var bar_width = 15;
	    var bar_height = 10;
	    var bar_horizontal_padding = 5;
	    var bar_vertical_padding = 0;

        /* Delete old SVG if it's there */
        d3.select("#search_results > svg").remove();

        var svg = d3.select("#search_results")
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
            .attr("transform", function(d, i) {
                return "translate(" +
                    i * (bar_width + bar_horizontal_padding) + ", 0)";
            })
            .each(function(d,i) {
                d.index = i;
            });

		var lines = responses.selectAll("g")
            .data(function(d) { return d.lines; })
            .enter()
            .append("g")
            .attr("class", "line_g")
            .attr("transform", function(d, i, j) { 
                return "translate(0," +
                    //j * (bar_width + bar_horizontal_padding) + "," +
                    i * (bar_height + bar_vertical_padding) + ")";
            })
            .each(function(d,i){
                d.index = i;
            });

        var bars = lines.append("rect")
            .attr("class", "line_rect")
			.attr("width", bar_width)
			.attr("height", bar_height)
			.style("fill", function(d) { return code_colors(d.type_); })
            .style("stroke", "black")
            .style("pointer-events", "all")
            .on("mouseover", function(d, i) {
                var body = d3.select(this.parentNode.parentNode).datum().body;
                setPreview("#preview_pane", body, d.text);
                if (dragStartParent !== undefined) {
                    dragging(this, d, i);
                }
            })
            .on("mousedown", dragStart)
            .on("mouseup", dragEnd);
            /*
            .on("click", function(d, i){
                //  flip value of sortOrder
                sortOrder = !sortOrder;
                var rs = d3.selectAll(".response_g")
                    .each(function(d, i){
                        sortBars(this);
                    });
            });
            */

        var shadowScale = 1.3;
        var flagBkgds = lines.append("svg")
            .attr("width", bar_width * shadowScale)
            .attr("height", bar_height * shadowScale)
            .attr("x", - (bar_width * (shadowScale - 1) / 2))
            .attr("y", - (bar_height * (shadowScale - 1) / 2))
            .append("use")
            .attr("class", "flag_bkgd")
            .attr("xlink:href", "static/skim/img/sprite.svg#media-record")
            .style("fill", "#fff")
            .style("fill-opacity", 0.0)
            .style("pointer-events", "none"); // do not block mouse events

        var flags = lines.append("svg")
            .attr("width", bar_width)
            .attr("height", bar_height)
            .append("use")
            .attr("class", "flag")
            .attr("xlink:href", "static/skim/img/sprite.svg#media-record")
            .style("fill", "#fff")
            .style("fill-opacity", 0.0)
            .style("pointer-events", "none"); // do not block mouse events

        // Sort UI elements
        d3.select("#sort_type_dropdown")
            .on("change", function(){
                sortResponses();
            });
        d3.selectAll("input[type=radio][name=sort_order]")
            .on("change", function(){
                sortResponses();
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

        var dragStartParent, dragEndParent;
        var dragStartLine, dragEndLine;
        var tempDragRect;        

        function dragStart(d, i) {
            dragEndParent = undefined;
            dragEndLine = undefined;
            dragStartParent = d3.select(this.parentNode.parentNode);
            dragStartLine = d3.select(this.parentNode);
        };

        function drawDragRect(target, d, i) {

            function posFromTranslate(string) {
                tokens = string.split(/[(,)]/);
                return {
                    x: tokens[1],
                    y: tokens[2]
                };
            }

            /* Draw rectangle over selected region */
            dragEndParent = d3.select(target.parentNode.parentNode);
            dragEndLine = d3.select(target.parentNode);
            if (dragEndParent.datum().index === dragStartParent.datum().index) {
                startPos = posFromTranslate(dragStartLine.attr("transform"));
                endPos = posFromTranslate(dragEndLine.attr("transform"));
                var rectX = startPos.x;
                var rectY = Math.min(startPos.y, endPos.y);
                var rectW = Number(d3.select(target).attr("width"));
                var rectH = Math.abs(startPos.y - endPos.y) + Number(d3.select(target).attr("height"));
                var rect = dragEndParent.append("rect")
                    .attr("x", rectX)
                    .attr("y", rectY)
                    .attr("width", rectW)
                    .attr("height", rectH)
                    .style("fill-opacity", 0)
                    .style("stroke", "black")
                    .style("stroke-width", 5)
                    .style("pointer-events", "none");
                return rect;
            }
        }

        function resetDrag() {
            dragStartParent = undefined;
            dragStartLine = undefined;
            if (tempDragRect !== undefined) {
                tempDragRect.remove();
            }
        }

        $("body").mouseup(resetDrag);

        function dragging(target, d, i) {
            if (tempDragRect !== undefined) {
                tempDragRect.remove();
            }
            tempDragRect = drawDragRect(target, d, i);
        };

        function dragEnd(d, i) {

            dragging(this, d, i);
            tempDragRect = undefined;  // hide the rectangle so it can't be overwritten

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
            body.find("span").removeClass("highlight");
            body.html(body.html().replace(/^\s*[\r\n]/gm, ""));

            var snippet = $("<div></div>")
                .addClass("keep");
            var header = snippet.append("<h5>" + window.query + "</h5>")
                .addClass("keep_header")
                .prop("contenteditable", "true")
                .on("keypress", function(e) {
                    if (e.keyCode == 13) {
                        $("#target").blur().next().focus();
                        return false;
                    }
                });
            snippet.append(body);
            $("#keep_cont").prepend(snippet);
            snippet.accordion({
                collapsible: true,
                heightStyle: "content"
            });
            $(".ui-accordion-header").css({ 
                padding: "1px 1px 1px 1px",
                "font-size": "12px"
            });
            $(".ui-accordion-content").css({ 
                padding: "1px 1px 1px 1px",
            });
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

        var sortResponses = function() {
            var sort_type = "length", sort_order="descending";
            sort_type = d3.select("#sort_type_dropdown").property('value');
            sort_order = d3.select("#sort_options_form input[type='radio']:checked").property('value');
            var d3_sort_order = sort_order === "ascending"? d3.ascending : d3.descending;
            d3.selectAll(".response_g")
                .sort(function(a, b) {
                    switch(sort_type) {
                        case "length":
                            //return d3.descending(a.lines.length, b.lines.length);
                            return d3_sort_order(a.lines.length, b.lines.length);
                            break;
                        case "code_lines":
                            return d3_sort_order(
                                a.lines.filter(function(d,i) { return d.type_ == "code"; }).length,
                                b.lines.filter(function(d,i) { return d.type_ == "code"; }).length);
                            break;
                        case "text_lines":
                            return d3_sort_order(
                                a.lines.filter(function(d,i) { return d.type_ == "text"; }).length,
                                b.lines.filter(function(d,i) { return d.type_ == "text"; }).length);
                            break;
                        case "votes":
                            return d3_sort_order(a.votes, b.votes);
                            break;
                        case "reputation":
                            return d3_sort_order(a.reputation, b.reputation);
                            break;
                    }
                })
                .transition()
                .duration(500)
                .attr("transform", function(d, i) { 
                    var transform = d3.transform(d3.select(this).attr("transform")).translate;
                    var xPosition = transform[0];
                    var yPosition = transform[1];
                    return "translate(" +
                        i * (bar_width + bar_horizontal_padding) + "," + 
                        yPosition + ")";
                });
        };
	};

    function setupLegend() {
        var legend_rect_length = 14;
        var legend_padding = 3;
        var svg = d3.select("#legend")
            .insert("svg")
            .attr("width", "100%")     
            .attr("height", legend_rect_length + legend_padding);
        var legend = svg.selectAll(".legend") 
            .data(code_colors.domain())
            .enter()
            .append('g')
            .attr('class', 'legend')
            .attr('transform', function(d,i) {
                // should calculate length and dimensions of rendered text
                return 'translate(' + (20 + (i * 120)) +  ',0)';
            });
        legend.append('rect')
                .attr('width', legend_rect_length)
                .attr('height', legend_rect_length)
                .style('fill', code_colors)
                .style('stroke', code_colors);
        legend.append('text')
                .attr('x', legend_rect_length + legend_padding)
                .attr('y', legend_rect_length - legend_padding)
                .text(function(d) { return code_types_2_readable[d]; });
    }

    function setupCountChart(divId, data, featureKey, colors) {

        /* Delete old chart if it's there. */
        d3.select(divId + " > svg").remove();

        var chart = d3.select(divId);
        var w = px_to_num(chart.style("width"));
        var h = px_to_num(chart.style("height"));
        var svg = chart
            .append("svg")
            .attr("width", w)
            .attr("height", h);
        var margin = {
            top: 10,
            bottom: 60,
            left: 50,
            right: 0
        };

        var REF_COUNT = 10;  // 20 because of category20 colors for D3
        var ref_counts = countCodeFeatures(data, featureKey);
        var sortedFeatCounts = d3.entries(ref_counts)
            .sort(function(a, b) {
                return b.value - a.value;
            })
            .splice(0, REF_COUNT);

        var ref_colors = colors.domain(sortedFeatCounts.map(function(e) { return e.key; }));
        sortedFeatCounts.forEach(function(element) {
            element.featureKey = featureKey;
            element.color = ref_colors(element.key);
        });

        var max_refs = d3.max(d3.entries(ref_counts), function(d) { return d.value; });
        var x_scale = d3.scale.ordinal()
            .domain(sortedFeatCounts.map(function(d) { return d.key; }))
            .rangeRoundBands([margin.left, w - margin.right], .1);
        var y_scale = d3.scale.linear()
            .domain([0, max_refs])
            .range([h - margin.bottom, margin.top]);
        var h_scale = d3.scale.linear()
            .domain([0, max_refs])
            .range([0, h - (margin.top + margin.bottom)]);

        var barConts = svg.selectAll("g")
            .data(sortedFeatCounts)
            .enter()
            .append("g")
            .attr("transform", function(d, i) { 
                return "translate(" + x_scale(d.key) + ",0)" 
            });

        var bars = barConts
            .append("rect")
            .attr("class", "dep_bar")
            .attr("y", function (d) { return y_scale(d.value); })
            .attr("width", x_scale.rangeBand())
            .attr("height", function(d) { return h_scale(d.value); })
            .style("fill", function(d) { return d.color; });

        /* These bars capture all of the mouse events for the displayed bars*/
        var phantomBars = barConts
            .append("rect")
            .attr("class", "phantom_bar")
            .attr("x", 0)
            .attr("y", 0)
            .attr("width", x_scale.rangeBand())
            .attr("height", h)
            .style("fill-opacity", 0)
            .on("mouseover", function() { mouseover(d3.select(this)); })
            .on("click", function() { click(d3.select(this)); })
            .on("mouseout", function(d) { mouseout(d3.select(this), d); });

        var labels = svg.selectAll("text")
            .data(sortedFeatCounts)
            .enter()
            .append("text")
            .attr("text-anchor", "end")
            .attr("class", "ac_label")
            .text(function(d) { return d.key; })
            .attr("transform", function(d) {
                return "translate(" + 
                    Math.floor(x_scale(d.key) + x_scale.rangeBand() / 2) + "," + 
                    (h - margin.bottom + 12) + 
                    ")rotate(-40)";
            });

        var yAxis = d3.svg.axis()
            .scale(y_scale)
            .ticks(4)
            .orient("left");
        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(" + margin.left + ",0)")
            .call(yAxis);

        function getBrotherBar(element) {
            return d3.select(element.node().parentNode).select(".dep_bar");
        }

        function mouseover(element) {
            getBrotherBar(element).classed("hovered", true);
            brighten_lines_with_feature(featureKey, element.data()[0].key, 1.5);
            getBrotherBar(element).call(color_dep_bar);
        }

        function click(element) {
            getBrotherBar(element).classed("selected", function() {
                return ! d3.select(this).classed("selected");
            });
            show_flags_for_selected_features(featureKey);
            getBrotherBar(element).call(color_dep_bar);
        }

        function mouseout(element, d) {
            getBrotherBar(element).classed("hovered", false);
            brighten_lines_with_feature(featureKey, d.key, 0);
            getBrotherBar(element).call(color_dep_bar);
        }

        function color_dep_bar(element) {
            element.style("fill", function(d) {
                var brightness = (
                    d3.select(this).classed("selected") || 
                    d3.select(this).classed("hovered")) ? 
                    1.5 : 0;
                return d3.rgb(d.color).brighter(brightness);
            })
            .style("stroke-width", function() {
                return d3.select(this).classed("selected") ? 2 : 0;
            })
            .style("stroke", function(d) {
                return d3.select(this).classed("selected") ? d.color : "black";
             })
            .style("stroke-dasharray", function() {
                return d3.select(this).classed("selected") ? "0" : "5,5";
            });
        }

        function brighten_lines_with_feature(key, ref, brightness) {
            d3.selectAll(".line_rect").filter(function(d) { 
                return (d[key].indexOf(ref) >= 0); 
            })
            .style("fill", function(d) {
                return d3.rgb(code_colors(d.type_)).brighter(brightness);
            });
        };

        function show_flags_for_selected_features(featureKey) {

            function color_flags_with_feature(featureKey, ref, color) {
                function selectFunc(d) {
                    return (d[featureKey].indexOf(ref) >= 0); 
                }
                d3.selectAll(".flag, .flag_bkgd")
                    .filter(selectFunc)
                    .style("fill-opacity", 1.0);
                d3.selectAll(".flag")
                    .filter(selectFunc)
                    .style("fill", function(d) {
                    return d3.rgb(color);
                });
            }

            /* Start by hiding all flags */
            d3.selectAll(".flag, .flag_bkgd").style("fill-opacity", 0.0);

            /* Fill in flag colors for selected deps, starting with least-used deps.
             * These will get overwritten by the selected most-used deps. */
            var selected = d3.selectAll(".dep_bar.selected");
            if (selected.length > 0) {
                selected[0].reverse();
                selected.each(function(d) {
                    color_flags_with_feature(d.featureKey, d.key, d.color);
                });
            }
        };
    }

    /* Utilities */
    function countCodeFeatures(data, key) {
        
        var feat_counts = {};
        for (var i = 0; i < data.length; i++) {
            var answer_features = [];
            var lines = data[i].lines;

            /* For each answer, get list of features. */
            for (var j = 0; j < lines.length ; j++) {
                var features = lines[j][key];
                for (var k = 0; k < features.length; k++) {
                    var feat = features[k];
                    if (answer_features.indexOf(feat) === -1) {
                        answer_features.push(feat);
                    }
                }
            }

            /* Compile counts of how many examples each featuer occurs in. */
            for (var j = 0; j < answer_features.length; j++) {
                var feat = answer_features[j];
                if (!(feat in feat_counts)) {
                    feat_counts[feat] = 0;
                }
                feat_counts[feat]++;
            }
        }
        return feat_counts;
    };

    function px_to_num(str) {
        return Number(str.replace("px", ""));
    };

    function addJavadocsLinks(divId, linksData) {
        $("#aggregate_chart text.ac_label").each(function() {
            var className = $(this).text();
            var link = undefined;
            if (linksData.hasOwnProperty(className)) {
                link = linksData[className];
            } else {
                link = "https://docs.oracle.com/javase/7/docs/api";
            }
            $(this).data("href", link)
            .on('click', function() {
                window.open($(this).data('href'), '_blank');
            })
            .css({
                cursor: 'pointer',
                cursor: 'hand'
            });
        });
    }

    function setupUI() {
        
        var submit = function(event) {
            $.getJSON("search", data={
                q: $("#query").val()
            }, function(data) {
                var answers = $.parseJSON(data['answers']);
                var questions = $.parseJSON(data['questions']);
                preprocessData(answers);
                setupQuestionList(questions, answers);
                window.query = data['query'];
                $("#query_text").text("Showing search results for \"" + data['query'] + "\"");
            });
            event.preventDefault();
        }

        $("#search_form").on("submit", submit);
        $("#search_button").on("click", submit);
    }

    /* Routines for processing input data */
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

    /* Globals */
    /* Colors for code bars from color brewer: http://colorbrewer2.org */
    //#a6cee3, #1f78b4, #b2df8a, #33a02c
    var code_colors = d3.scale.ordinal()
        .domain(["text", "code", "codecommentinline", "codecommentlong"])
        .range(["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c"]);
    var code_types_2_readable = {"text": "Text", 
                                 "code": "Code",
                                 "codecommentinline": "Inline Comment",
                                 "codecommentlong": "Long Comment"};

    var category10 = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"];
    var class_colors = d3.scale.ordinal()
        .range(category10)
    var concept_colors = d3.scale.ordinal()
        .range(category10.slice(0).reverse())
    var linksData;
    

            

    /* MAIN */
    d3.json("/static/skim/data/javadocs_links.json", function(data) {
        setupUI();
        linksData = data;
        preprocessData(window.answers);
        setupQuestionList(window.questions, window.answers);
    });
});
