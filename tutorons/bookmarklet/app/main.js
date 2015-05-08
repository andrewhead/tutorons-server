/*jshint strict:false, browser:true */
(function bookmarklet() {

    /* REUSE: code for relative positioning is from http://stackoverflow.com/questions/4666367/how-do-i-position-a-div-relative-to-the-mouse-pointer-using-jquery */
    var mouseX;
    var mouseY;
    $(document).mousemove( function(e) {
       mouseX = e.pageX; 
       mouseY = e.pageY;
    });

    var explanations = {};

    // Process full page to get all explanations of commands
    $.post('http://127.0.0.1:8000/wget',
        document.body.innerHTML,
        function(resp) {
            explanations = JSON.parse(resp);
        });

    document.body.onmouseup = function() {

        var selString = window.getSelection().toString();

        if (selString.length > 0) {

            // Find the first command that contains this string
            var explanation;
            for (var key in explanations) {
                if (explanations.hasOwnProperty(key)) {
                    if (key.indexOf(selString) !== -1) {
                        explanation = explanations[key];
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

            // Set display parameters and fade in tooltip
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
