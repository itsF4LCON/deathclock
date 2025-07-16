document.addEventListener("DOMContentLoaded", () => {
    let remaining = totalSeconds;
    const countdown = document.getElementById("countdown");

    function update() {
        const days = Math.floor(remaining / 86400);
        const hours = Math.floor((remaining % 86400) / 3600);
        const minutes = Math.floor((remaining % 3600) / 60);
        const seconds = remaining % 60;

        countdown.textContent = `Time remaining: ${days}d ${hours}h ${minutes}m ${seconds}s`;
        remaining--;

        if (remaining >= 0) {
            setTimeout(update, 1000);
        } else {
            countdown.textContent = "Time's up!";
        }
    }

    update();
});