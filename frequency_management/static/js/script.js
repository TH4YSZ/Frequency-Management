
document.addEventListener("DOMContentLoaded", function() {
    const themeToggleBtn = document.getElementById("theme-toggle");
    let currentTheme = localStorage.getItem("theme") || "light";

    // Define o tema inicial baseado no valor armazenado no localStorage ou padrão 'light'
    document.documentElement.setAttribute("data-theme", currentTheme);

    // Adiciona evento de clique para alternar tema
    themeToggleBtn.addEventListener("click", function() {
        currentTheme = currentTheme === "light" ? "dark" : "light";
        document.documentElement.setAttribute("data-theme", currentTheme);
        localStorage.setItem("theme", currentTheme); // Armazena a preferência do usuário
    });
});

