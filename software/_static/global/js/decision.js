console.log("decision ready!")

// form validation
if (template == "instructions"){
    var current_endowment = 35;
} else {
    var current_endowment = endowments[current_round - 1]
}

// change border color as feedback for invalid inputs
document.getElementById("id_contribution").addEventListener('input', () => {
    input = parseInt(document.getElementById("id_contribution").value) || 0;
    if (input > current_endowment){
        document.getElementById("id_contribution").className = "form-control border-danger m-0";
    } else {
        document.getElementById("id_contribution").className = "form-control border-primary m-0"; // border border-success
    }
});

// change button on input
document.getElementById("id_contribution").addEventListener('input', () => {
    input = parseInt(document.getElementById("id_contribution").value) || null;
    document.getElementById("submit_button").className = "btn-primary btn w-100"
    if (input > 0){
        document.getElementById("submit_button").innerHTML = "To Group Account";
    } else {
        document.getElementById("submit_button").innerHTML = "Keep everything";
        // document.getElementById("id_contribution").value = null;
    }
});

// submit Form after validation
/*
function submitForm() {
    contribution = document.getElementById("id_contribution").value
    if (contribution == "") {
        document.getElementById("id_contribution").value = 0;
    }
    if (contribution <= current_endowment){
        document.forms[0].submit()
    }
    investment = document.getElementById("id_investment").value
        if (investment == "") {
            document.getElementById("id_investment").value = 0;
        }
        if (investment <= current_endowment){
            document.forms[0].submit()
        }
}
*/



