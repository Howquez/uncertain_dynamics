console.log("calculator ready!")

function calculate() {
    yourContribution = parseInt(document.getElementById("yourContribution").value)
    othersContributions = parseInt(document.getElementById("othersContributions").value)
    var ewe = document.getElementById("eweFlexSwitch").checked
    var yourReturn = Math.ceil((othersContributions * (num_players - 1) + yourContribution) * factor) - yourContribution;
    if (ewe) {
    yourReturn = yourReturn - Math.floor((1 - (othersContributions * (num_players - 1) + yourContribution) / wealth) * damage * endowment);
    }
    var futureEndowment = endowment + yourReturn

    document.getElementById("yourContributionTable").innerHTML = yourContribution;
    document.getElementById("othersContributionsTable").innerHTML = othersContributions;
    document.getElementById("yourReturnTable").innerHTML = yourReturn;
    document.getElementById("yourReturn").value = yourReturn;
    document.getElementById("yourEndowmentTable").innerHTML = futureEndowment;

    document.getElementById("calculator_button").innerHTML = "Re-calculate";
}

// Measure the time the calculator was opened
var startTime;
var endTime;
var increment = 0;
var sum = 0;

var myOffcanvas = document.getElementById('offcanvasCalculator')
myOffcanvas.addEventListener('show.bs.offcanvas',
function () {
    startTime = Date.now()
})

myOffcanvas.addEventListener('hidden.bs.offcanvas',
function () {
    endTime = Date.now();
    increment = endTime - startTime;
    sum += increment

    document.getElementById("calculator_time").value = sum/1000;
})
