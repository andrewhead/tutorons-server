SHARE_DIV = '<div class="share-box">' +
'<form>' +
'<input type="text" class="form-control" style="vertical-align:top;"></input><br>' +
'<div style="display:block;">' +
'<div class="ctn-radio">' +
'<input type="radio" id="r-bug" name="insight" value="bug"/>' +
'<label for="r-bug">Bug Fix</label>' +
'<input type="radio" id="r-learning" name="insight" value="learning"/>' +
'<label for="r-learning">Learning Tip</label>' +
'<input type="radio" id="r-implementation" name="insight" value="implementation"/>' +
'<label for="r-implementation">Implementation Tip</label>' +
'</div>' +
'<div class="btn-share col-xs-3">' +
'<a href="#" class="btn btn-primary btn-block btn-large">Share</a>' +
'</div>' +
'</div>' +
'</form>' +
'</div>';

self.port.on("write", function() { 
    splitFromSelect();
});

function expandRangeToStart(range) {
    var element = range.startContainer;
    while (element.tagName !== "CODE") {
        element = element.parentNode;
    }
    range.setStart(element, 0);
    return range;
}

function expandRangeToEOL(range) {
    var textElement = range.endContainer;
    var parentNode = textElement;
    while (parentNode.tagName !== "CODE") {
        textElement = parentNode;
        parentNode = textElement.parentNode;
    }
    range.setEnd(textElement, 0);
    var charIndex = 0;
    while (true) {
        var text = range.toString();
        if (text[text.length - 1] === "\n") {
            break;
        } else if (charIndex < textElement.length) {
            charIndex++;
            range.setEnd(textElement, charIndex);
        } else if (textElement.nextSibling != null) {
            textElement = textElement.nextSibling;
            charIndex = 0;
            range.setEnd(textElement, charIndex);
        } else {
            break;
        }
    }
    return range;
}

function expandRangeToEnd(range) {
    var element = range.startContainer;
    while (element.tagName !== "CODE") {
        element = element.parentNode;
    }
    var origStartCont = range.startContainer;
    var origStartOffset = range.startOffset;
    range.selectNode(element);
    range.setStart(origStartCont, origStartOffset);
    return range;
}

function newlines(r) {
    return r.toString().split("\n").length - 1;
}

function backNLines(range, n) {

    var origNl = newlines(range);

    var textElement = range.endContainer;
    var parentNode = textElement;
    while (parentNode.tagName !== "CODE") {
        textElement = parentNode;
        parentNode = textElement.parentNode;
    }

    /* Move start of selection back to the start of the section.
     * Then we iterate through until the number of newlines is back to
     * the original, consuming in the range everything before that. */
    var charIndex = 0;
    textElement = parentNode;
    range.setStart(textElement, charIndex);
    while (newlines(range) > origNl + n) {
        var text = range.toString();
        if (charIndex < textElement.textContent.length) {
            charIndex++;
            range.setStart(textElement, charIndex);
        } else if (textElement.nextSibling != null) {
            textElement = textElement.nextSibling;
            charIndex = 0;
            range.setStart(textElement, charIndex);
        } else {
            break;
        }
    }
    return range;
}

function expandRangeToBOL(range) {
    backNLines(range, 0);
}

function splitFromSelect() {

    var selection = window.getSelection();
    var selectRange = window.getSelection().getRangeAt(0);
    var origNl = newlines(selectRange);
   
    var tRange = document.createRange();
    tRange.setStart(selectRange.startContainer, selectRange.startOffset);
    tRange.setEnd(selectRange.endContainer, selectRange.endOffset);
    expandRangeToStart(tRange);
    expandRangeToEOL(tRange);
    var bRange = document.createRange();
    bRange.setStart(tRange.endContainer, tRange.endOffset);
    bRange.setEnd(tRange.endContainer, tRange.endOffset);
    expandRangeToEnd(bRange);

    /* Embolden the selected text */
    var boldRange = document.createRange();
    boldRange.setEnd(tRange.endContainer, tRange.offset);
    boldRange.setStart(tRange.endContainer, tRange.offset);
    backNLines(boldRange, origNl);
    
    var ul = $("<u></u>")[0];
    var bold = $("<b></b>")[0];
    bold.appendChild(boldRange.cloneContents());
    ul.appendChild(bold);
    boldRange.deleteContents();
    boldRange.insertNode(ul);

    var element = selectRange.startContainer;
    while (element.tagName !== "PRE") {
        element = element.parentNode;
    }
    var preCont = element.parentNode;

    var tPre = $("<pre></pre>");
    var tCode = $("<code></code>");
    $(preCont).append(tPre);
    tPre.append(tCode);
    tCode.append(tRange.cloneContents());
    
    var shareDiv = $(SHARE_DIV);
    $(preCont).append(shareDiv);
    $('.share-box .btn').click(function(e) { 
        e.preventDefault();
        var cont = bPre[0];
        var par = cont.parentNode;
        while ($(par).find('p').length == 0 && $(par).find('h3').length == 0) {
            cont = par;
            par = par.parentNode;
        }
        var text = $('.share-box .form-control').val()
        var par = $("<p>" + text + "</p>");
        par.css('margin-top', '10px');
        shareDiv.detach();
        $('u').click(function() {
            par.insertAfter(cont);
        });
        self.port.emit("share");
    });

    var bPre = $("<pre></pre>");
    var bCode = $("<code></code>");
    $(preCont).append(bPre);
    bPre.append(bCode);
    bCode.append(bRange.cloneContents());

    $(element).detach();
}
