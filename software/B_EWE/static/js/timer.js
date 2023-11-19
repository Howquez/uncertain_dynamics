console.log("timer ready")

document.addEventListener("DOMContentLoaded", function (event) {
    $('.otree-timer__time-left').on('update.countdown', function (event) {
        if (event.offset.totalSeconds === 20) {
            $('.otree-timer').show();
        }
    });
});