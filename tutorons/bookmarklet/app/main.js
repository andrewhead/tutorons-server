/*jshint strict:false, browser:true */
(function bookmarklet() {

    var SERVER_BASE = 'http://127.0.0.1:8000/';
    var TUTORONS = ['wget', 'css'];

    // Get explanations for the full page
    var explanations = {};
    var saveExplanation = function(tutName) {
        return function(resp) {
            explanations[tutName] = JSON.parse(resp);
        };
    };
    for (var i = 0; i < TUTORONS.length; i++) {
        var tutName = TUTORONS[i];
        explanations[tutName] = {};
        $.post(SERVER_BASE + tutName, document.body.innerHTML, saveExplanation(tutName));
    }
    
    // Trigger tooltip on raising mouse after selection
    document.body.onmouseup = function() {

        var selection = window.getSelection();
        var selString = selection.toString();
        if (selString.length > 0) {

            // Find the first command that contains this string
            var explanation;
            var closestDist = Number.MAX_VALUE;
            for (var tutKey in explanations) {
                if (explanations.hasOwnProperty(tutKey)) {
                    var tut = explanations[tutKey];
                    for (var key in tut) {
                        if (tut.hasOwnProperty(key)) {
                            var editDist = levenshtein(selString, key);
                            if (editDist < closestDist) {
                                closestDist = editDist;
                                explanation = tut[key];
                            }
                        }
                    }
                }
            }

            if (explanation === undefined) {
                return;
            }

            // Remove container if it already exists
            var div = document.getElementById('hint-tooltip');
            if (div !== null) {
                document.body.removeChild(div);
            }

            // Create container
            div = document.createElement('div');
            div.id = 'hint-tooltip';
            document.body.appendChild(div);

            // Add explanation to tooltip
            div.innerHTML = explanation;

            // Style the tooltip
            $(div).css({
                width: '600px',
                position: 'absolute',
                border: 'gray 2px dashed',
                'padding-top': '10px',
                'background-color': 'white',
                'padding': '20px',
                'font-family': '"Palatino Linotype", "Book Antiqua", Palatino, serif',
                'font-size': '14px',
                display: 'none',
            });
            $(div).find('p, ul').css({
                'margin-bottom': '.4em',
            });
            $(div).find('.wget-opt').css({
                'font-family': '"Courier New", Courier, monospace',
            });

            // Center tooltip beneath text.  Doesn't work in IE9.
            var selRange = selection.getRangeAt(0);
            var selRect = selRange.getBoundingClientRect();
            var selMidX = selRect.left + selRect.width / 2;
            var selMidY = selRect.top + selRect.height / 2;
            $(div).css({
                left: String(selMidX - $(this).width() / 2) + 'px',
                top: String(selMidY - $(this).height() / 2) + 'px',
            });

            // Hide tooltip when click happens outside it
            var hide = function() {
                $(div).css('display', 'none');
                $(document.body).unbind('click', hide);
            };
            $(document.body).bind('click', hide);

            // Fade in the tooltip!
            $(div).fadeIn('slow');

        }
    };


    // LEVENSHTEIN EDIT DISTANCE
    /*
    Copyright (c) 2011 Andrei Mackenzie
    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    */
    // Compute the edit distance between the two given strings
    var levenshtein = function(a, b){

        if (a.length === 0) {
            return b.length; 
        }
        if (b.length === 0) {
            return a.length; 
        }
       
        var matrix = [];
       
        // increment along the first column of each row
        var i;
        for (i = 0; i <= b.length; i++){
            matrix[i] = [i];
        }
       
        // increment each column in the first row
        var j;
        for (j = 0; j <= a.length; j++){
            matrix[0][j] = j;
        }
       
        // Fill in the rest of the matrix
        for (i = 1; i <= b.length; i++){
            for (j = 1; j <= a.length; j++){
                if (b.charAt(i-1) === a.charAt(j-1)){
                    matrix[i][j] = matrix[i-1][j-1];
                } else {
                    matrix[i][j] = Math.min(matrix[i-1][j-1] + 1, // substitution
                                   Math.min(matrix[i][j-1] + 1, // insertion
                                   matrix[i-1][j] + 1)); // deletion
                }
            }
        }
       
        return matrix[b.length][a.length];
    };

}());
