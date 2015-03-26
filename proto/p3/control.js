$(function() {

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

function splitFromSelect() {
    var selectRange = window.getSelection().getRangeAt(0);
    
    var tRange = document.createRange();
    tRange.setStart(selectRange.startContainer, selectRange.startOffset);
    tRange.setEnd(selectRange.endContainer, selectRange.endOffset);
    expandRangeToStart(tRange);
    expandRangeToEOL(tRange);
    var bRange = document.createRange();
    bRange.setStart(tRange.endContainer, tRange.endOffset);
    bRange.setEnd(tRange.endContainer, tRange.endOffset);
    expandRangeToEnd(bRange);

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
    
    $(preCont).append("<br/>");
    $(preCont).append($(".share-box"));

    var bPre = $("<pre></pre>");
    var bCode = $("<code></code>");
    $(preCont).append(bPre);
    bPre.append(bCode);
    bCode.append(bRange.cloneContents());

    $(element).detach();
}
