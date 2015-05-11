function highlight(selector) {
    $('.test-cont ' + selector)
        .not('.dom')
        .css({'background-color': 'yellow'});
    return 'Check to make the elements reading "Select Me" turned yellow.';
}

var h = highlight;
