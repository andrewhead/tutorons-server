/*jshint strict:false, browser:true */
(function bookmarklet() {

    /* Assumes we have already loaded Nicolas Hoening's NHPUP popus */

    var selString = window.getSelection().toString();
    if (selString.length > 0) {
        var div = document.createElement('div');
        window.showRegex(div, selString);
        console.log(div);
        window.nhpup.popup(div.outerHTML);
    }

}());
