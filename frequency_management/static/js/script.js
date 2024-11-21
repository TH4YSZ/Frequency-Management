document.addEventListener("DOMContentLoaded", function () {
    const themeToggleBtn = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    let currentTheme = localStorage.getItem("theme") || "light";

    // Set initial theme and icon
    document.documentElement.setAttribute("data-theme", currentTheme);
    themeIcon.classList.remove("bi-sun-fill", "bi-moon-fill");
    themeIcon.classList.add(currentTheme === "light" ? "bi-sun-fill" : "bi-moon-fill");

    themeToggleBtn.addEventListener("click", function () {
        currentTheme = currentTheme === "light" ? "dark" : "light";

        // Update theme attribute
        document.documentElement.setAttribute("data-theme", currentTheme);

        // Update localStorage
        localStorage.setItem("theme", currentTheme);

        // Update icon
        themeIcon.classList.remove("bi-sun-fill", "bi-moon-fill");
        themeIcon.classList.add(currentTheme === "light" ? "bi-sun-fill" : "bi-moon-fill");
    });
});