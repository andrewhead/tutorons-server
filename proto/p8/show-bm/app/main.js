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
            window.showRegex(div, escString);
            $.get(
                'http://127.0.0.1:8001/regex/' + encodeURIComponent(selString),
                {},
                function(resp) {
                    var pre = document.createElement('pre');
                    pre.innerHTML = resp;
                    pre.style.padding = '15px';
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
