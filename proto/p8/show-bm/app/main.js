/*jshint strict:false, browser:true */
(function bookmarklet() {

    /* REUSE: code for relative positioning is from http://stackoverflow.com/questions/4666367/how-do-i-position-a-div-relative-to-the-mouse-pointer-using-jquery */
    var mouseX;
    var mouseY;
    $(document).mousemove( function(e) {
       mouseX = e.pageX; 
       mouseY = e.pageY;
    });

    document.body.onmouseup = function() {

        var selString = window.getSelection().toString();
        if (selString.length > 0) {

            // Remove container if it already exists
            var div = document.getElementById('hint-tooltip');
            if (div !== null) {
                document.body.removeChild(div);
            }

            // Create container
            div = document.createElement('div');
            div.id = 'hint-tooltip';
            document.body.appendChild(div);

            // Add visualization and explanatory text to tooltip
            var escString = selString.replace(/\//g, '\\/');
            var explanation = $('<div></div>');
            var intro = $('<p></p>');
            var desc = $('<p></p>');
            intro.text('You found a regular expression!')
                .css('font-size', '16px');
            desc.text('We compare text to regular expressions to see if they match ' +
                'a pattern or not.  To read this regular expression diagram, ' +
                'follow it from left to right as you see the letters and ' +
                'symbols it looks for in a line of text.')
                .css({
                    'font-size': '12px',
                    'line-height': '1.2em'
                });
            explanation.css({
                'width': '400px',
                'margin': 'auto',
                'padding-left': '10px',
                'padding-right': '10px'
            });
            explanation.append(intro);
            explanation.append(desc);
            $(div).append(explanation);
            window.showRegex(div, escString);
            $.get(
                'http://127.0.0.1:8001/regex/' + encodeURIComponent(selString),
                {},
                function(resp) {
                    var pre = document.createElement('pre');
                    pre.innerHTML = resp.trim();
                    pre.style.padding = '15px';
                    pre.style['font-size'] = '14px';
                    pre.style['line-height'] = '1.2em';
                    div.appendChild(pre);
                });

            // Set display parameters and fade in tooltip
            $(div).css({
                left: String(mouseX - 300) + 'px',
                top: String(mouseY + 30) + 'px',
                position: 'absolute',
                border: 'gray 1px dotted',
                'padding-top': '10px',
                'background-color': 'white',
                display: 'none'
            });
            $(div).click(function() {
                $(this).css('display', 'none');
            });
            $(div).fadeIn('slow');


        }
    };

}());
