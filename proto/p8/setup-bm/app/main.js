/*jshint strict:false, browser:true */
(function bookmarklet() {

    var SERVER = 'http://127.0.0.1:8000';

    /* REUSE: from http://www.javascriptkit.com/javatutors/loadjavascriptcss.shtml */
    function loadjscssfile(filename, filetype) {
        var fileref;
        if (filetype === 'js') {
            fileref = document.createElement('script');
            fileref.setAttribute('type','text/javascript');
            fileref.setAttribute('src', filename);
        }
        else if (filetype === 'css'){
            fileref = document.createElement('link');
            fileref.setAttribute('rel', 'stylesheet');
            fileref.setAttribute('type', 'text/css');
            fileref.setAttribute('href', filename);
        }
        if (typeof fileref !== 'undefined') {
            document.getElementsByTagName('head')[0].appendChild(fileref);
        }
    }

    loadjscssfile(SERVER + '/build/js/javascript.js', 'js');
    loadjscssfile(SERVER + '/build/css/main.css', 'css');
    loadjscssfile(SERVER + '/build/css/svg.css', 'css');

}());
