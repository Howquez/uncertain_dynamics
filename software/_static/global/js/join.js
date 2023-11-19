console.log("join ready!")

// Join the club?

function changeJoinButtonText() {
    btn = document.getElementById("join_id")
    text = document.getElementById("join_id2")
    if (btn.innerHTML == "Join club") {
        btn.innerHTML = "I'm in!"
        text.innerHTML = "Click again to undo."
        return;
    }
    if (btn.innerHTML == "I'm in!") {
        btn.innerHTML = "Join club"
        text.innerHTML = "Click to join the club."
        return;
    }
}

function changeLeaveButtonText() {
    btn = document.getElementById("leave_id")
    text = document.getElementById("leave_id2")
    if (btn.innerHTML == "Leave club") {
        btn.innerHTML = "I'm out!"
        text.innerHTML = "Click again to undo."
        return;
    }
    if (btn.innerHTML == "I'm out!") {
        btn.innerHTML = "Leave club"
        text.innerHTML = "Click to leave the club."
        return;
    }

}
