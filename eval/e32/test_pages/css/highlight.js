function highlight(selector) {
    $('.task-cont ' + selector)
        .not('.dom')
        .css({'background-color': 'yellow'});
}

var h = highlight;
