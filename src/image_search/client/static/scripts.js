function check_input(obj) {
    var input_text = $(obj).val();
    var input_char = input_text.slice(-1).toLowerCase();
    var secondlast_char = input_text.slice(-2, -1);
    cleaned = false;
    if (!(
        (input_char >= 'a' && input_char <= 'z') ||
        (input_char == ' ' && secondlast_char != ' ' && input_text != ' ')
    )) {
        obj.value = input_text.slice(0, -1);
        cleaned = true;
    }
    return cleaned
}

function autocomplete(inp) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*close any already open lists of autocompleted values*/
    closeAllLists();
    if (!inp.value) { return false; }
    var currentFocus = -1, a, b;
    /*create a DIV element that will contain the items (values):*/
    a = document.createElement("DIV");
    a.setAttribute("id", inp.id + "_autocomplete-list");
    a.setAttribute("class", "autocomplete-items");
    /*append the DIV element as a child of the autocomplete container:*/
    inp.parentNode.appendChild(a);
    var arr;
    if (term_correction.length == 1) {
        arr = term_correction.concat(completions)
    }
    else {
        if (term_completion.length == 1) {
            arr = term_completion.concat(completions)
        }
        else {
            if (term_prediction.length == 1) {
                arr = term_prediction.concat(completions)
            }
            else {
                arr = completions
            }
        }
    }
    //term_completion.concat(term_correction, term_prediction, completions)
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
    inp.addEventListener("keydown", function(e) {
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
    });
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
var timer_completion = 0;
var completions = [];
$("#query").on("input", function() {
    cleaned = check_input(this);
    if (timer_completion) {
        clearTimeout(timer_completion);
    }
    partial_query = $(this).val();
    if (partial_query.length == 0 || cleaned) return false;
    timer_completion = setTimeout(function() {
        $.post("/complete", {"partial_query": partial_query}).done(function(response) {
            completions = response.completions;
            autocomplete(document.getElementById("query"));
        });
    }, 300);
});

/*execute a function when someone writes in the text field:*/
var timer_term_prediction = 0;
var term_prediction = [];
$("#query").on("input", function() {
    cleaned = check_input(this);
    if (timer_term_prediction) {
        clearTimeout(timer_term_prediction);
    }
    partial_query = $(this).val();
    if (partial_query.length == 0 || partial_query.slice(-1) != ' ' || cleaned) {
        term_prediction = []
        return false;
    }
    timer_term_prediction = setTimeout(function() {
        term_prediction = []
        $.post("/predict_term", {"partial_query": partial_query}).done(function(response) {
            if (response.next_term != null) {
                term_prediction = ["<i>(term prediction) </i>" + partial_query + response.next_term];
            }
            autocomplete(document.getElementById("query"));
        });
    }, 300);
});

/*execute a function when someone writes in the text field:*/
var timer_term_correction = 0;
var term_correction = [];
$("#query").on("input", function() {
    cleaned = check_input(this);
    if (timer_term_correction) {
        clearTimeout(timer_term_correction);
    }
    partial_query = $(this).val();
    if (partial_query.length == 0 || partial_query.slice(-1) != ' ' || cleaned) {
        term_correction = []
        return false;
    }
    timer_term_correction = setTimeout(function() {
        $.post("/correct_term", {"partial_query": partial_query}).done(function(response) {
            term_correction = []
            if (response.correct_term != null) {
                partial_query = partial_query.split(" ").slice(0, -2).join(" ") + " ";
                term_correction = ["<i>(term correction) </i>" + partial_query + response.correct_term]
            }
            autocomplete(document.getElementById("query"));
        });
    }, 300);
});

/*execute a function when someone writes in the text field:*/
var timer_term_completion = 0;
var term_completion = [];
$("#query").on("input", function() {
    cleaned = check_input(this);
    if (timer_term_completion) {
        clearTimeout(timer_term_completion);
    }
    partial_query = $(this).val();
    if (partial_query.length == 0 || cleaned) {
        term_completion = []
        return false;
    }
    timer_term_completion = setTimeout(function() {
        $.post("/complete_term", {"partial_query": partial_query}).done(function(response) {
            term_completion = []
            if (response.complete_term != null) {
                partial_query = partial_query.split(" ").slice(0, -1).join(" ") + " ";
                term_completion = ["<i>(term completion) </i>" + partial_query + response.complete_term];
            }
            autocomplete(document.getElementById("query"));
        });
    }, 300);
});