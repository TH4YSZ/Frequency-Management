document.addEventListener("DOMContentLoaded", function () {
    const alertContainer = document.getElementById("alert-container");
    if (alertContainer) {
        setTimeout(() => {
            alertContainer.classList.add("fade-out-hidden");
        }, 3000);
    }
});