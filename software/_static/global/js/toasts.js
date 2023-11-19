console.log("toasts ready!")

// initialize toasts with a timer
/*
setTimeout(
    function () {
        if (template == "decision"){
            var toastElList = [].slice.call(document.querySelectorAll('.toast'))
            var toastList = toastElList.map(function(toastEl) {
                // Creates an array of toasts (it only initializes them)
                return new bootstrap.Toast(toastEl) // No need for options; use the default options
            });
            toastList.forEach(toast => toast.show()); // This show them
        }
    },
    3000
);*/

setTimeout(
    function () {
        if (template == "decision"){
            document.getElementById("timeoutToast").style.display = "block";
            document.getElementById("timeoutToast").classList.add("show")
        }
    },
    (timeout - 0.5) * 60 * 1000
);
