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
    
    // Track mouse current cursor.
    /* REUSE ALERT: code for relative positioning is from 
     * http://stackoverflow.com/questions/4666367 */
    var mouseX;
    var mouseY;
    $(document).mousemove(function(e) {
        mouseX = e.pageX; 
        mouseY = e.pageY;
    });

    // Trigger tooltip on raising mouse after selection
    document.body.onmouseup = function() {

        var selString = window.getSelection().toString();
        if (selString.length > 0) {

            console.log(explanations);
            // Find the first command that contains this string
            var explanation;
            for (var tutKey in explanations) {
                if (explanations.hasOwnProperty(tutKey)) {
                    var tut = explanations[tutKey];
                    for (var key in tut) {
                        if (tut.hasOwnProperty(key)) {
                            if (key.indexOf(selString) !== -1) {
                                console.log('Match');
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
                left: String(mouseX - 300) + 'px',
                top: String(mouseY + 30) + 'px',
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

            $(div).click(function() {
                $(this).css('display', 'none');
            });
            $(div).fadeIn('slow');

        }
    };
}());
