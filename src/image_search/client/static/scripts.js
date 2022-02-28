function check_input(obj) {
    obj.value = obj.value.toLowerCase();
    var input_text = $(obj).val();
    var input_char = input_text.slice(-1);
    var secondlast_char = input_text.slice(-2, -1);
    cleaned = false;
    if (!(
        (input_char >= 'a' && input_char <= 'z') ||
        (input_char == ' ' && secondlast_char != ' ' && input_text != ' ')
    )) {
        obj.value = input_text.slice(0, -1)
        cleaned = true;
    }
    return cleaned
}

function update_dropdown(e) {
    var x = document.getElementById(this.id + "_autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
    } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
    } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
            /*and simulate a click on the "active" item:*/
            if (x) {
                x[currentFocus].click();
                currentFocus = -1
            }
        }
        else if (currentFocus == -1) {
            document.getElementById("query_form").submit()
        }
    }
}

function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
}
function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
    }
}

function autocomplete(inp, arr) {
    /*close any already open lists of autocompleted values*/
    closeAllLists();
    if (!inp.value) { return false; }
    var a, b;
    /*create a DIV element that will contain the items (values):*/
    a = document.createElement("DIV");
    a.setAttribute("id", inp.id + "_autocomplete-list");
    a.setAttribute("class", "autocomplete-items");
    /*append the DIV element as a child of the autocomplete container:*/
    inp.parentNode.appendChild(a);
    /*for each item in the array...*/
    for (var i = 0; i < arr.length; i++) {
        /*create a DIV element for each matching element:*/
        b = document.createElement("DIV");
        b.innerHTML += arr[i];
        /*insert a input field that will hold the current array item's value:*/
        b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
        /*execute a function when someone clicks on the item value (DIV element):*/
        b.addEventListener("click", function(e) {
            /*insert the value for the autocomplete text field:*/
            selection = this.getElementsByTagName("input")[0].value;
            selection = selection.replace(/ *\<i>[^</]*\<\/i> */g, "");
            inp.value = selection.match(/[a-z]+/g).join(" ");
            /*close the list of autocompleted values,
            (or any other open lists of autocompleted values:*/
            closeAllLists();
        });
        a.appendChild(b);
    }
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", update_dropdown);
    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

/*execute a function when someone writes in the text field:*/
var timer = 0;
var suggestions;
var currentFocus = -1;
$("#query").on("input", function() {
    var cleaned = check_input(this);
    if (timer) {
        clearTimeout(timer);
    }
    var partial_query = $(this).val();
    suggestions = [];
    this.removeEventListener("keydown", update_dropdown);
    currentFocus = -1;
    if (partial_query.length == 0 || cleaned) {
        return false;
    }
    timer = setTimeout(function() {
        $.post("/complete", {"partial_query": partial_query}).done(function(response) {
            var completions = response.completions;
            if (partial_query.slice(-1) == ' ') {
                $.post("/correct_term", {"partial_query": partial_query}).done(function(response) {
                    if (response.correct_term != null) {
                        partial_query = partial_query.split(" ").slice(0, -2).join(" ") + " ";
                        suggestions = ["<i>(term correction) </i>" + partial_query + response.correct_term]
                        suggestions = suggestions.concat(completions);
                        autocomplete(document.getElementById("query"), suggestions);
                    }
                    else {
                        $.post("/predict_term", {"partial_query": partial_query}).done(function(response) {
                            if (response.next_term != null) {
                                suggestions = ["<i>(term prediction) </i>" + partial_query + response.next_term];
                                suggestions = suggestions.concat(completions);
                                autocomplete(document.getElementById("query"), suggestions);
                            }
                        });
                    }
                });
            }
            else {
                $.post("/complete_term", {"partial_query": partial_query}).done(function(response) {
                    if (response.complete_term != null) {
                        partial_query = partial_query.split(" ").slice(0, -1).join(" ") + " ";
                        suggestions = ["<i>(term completion) </i>" + partial_query + response.complete_term];
                        suggestions = suggestions.concat(completions);
                        autocomplete(document.getElementById("query"), suggestions);
                    }
                    else {
                        suggestions = completions;
                        autocomplete(document.getElementById("query"), suggestions);
                    }
                });
            }
        });
    }, 300);
});
