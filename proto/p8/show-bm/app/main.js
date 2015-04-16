/*jshint strict:false, browser:true */
(function bookmarklet() {

    /* REUSE: code from http://stackoverflow.com/questions/4666367/how-do-i-position-a-div-relative-to-the-mouse-pointer-using-jquery */
    var mouseX;
    var mouseY;
    $(document).mousemove( function(e) {
       mouseX = e.pageX; 
       mouseY = e.pageY;
    });

    document.body.onmouseup = function() {

        var selString = window.getSelection().toString();
        if (selString.length > 0) {

            var div = document.createElement('div');
            document.body.appendChild(div);
            window.showRegex(div, selString);

            $(div).css({
                left: String(mouseX) + 'px',
                top: String(mouseY) + 'px',
                position: 'absolute',
                border: 'gray 1px dotted',
                'padding-top': '10px',
                'background-color': 'white',
                display: 'none'
            });
            $(div).fadeIn('slow');

        }
    };

}());
