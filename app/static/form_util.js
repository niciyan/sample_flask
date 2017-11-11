// var listener = document.getElementById("replace-listener");
// listener.onclick("click", replace, false);

//@doc
//replace textarea value and return string
function replace() {
    // var input = document.getElementById("flask-pagedown-body").value;
    var selection = $("flask-pagedown-body").getSelection();
    $("flask-pagedown-body").replaceSelectedText(selection.text.replace(/^/gm, "    "));
}

