document.addEventListener('DOMContentLoaded', function () {
    const searchIcon = document.getElementById('search-icon');
    const searchContainer = document.getElementById('search-container');

    searchIcon.addEventListener('click', function () {
        searchContainer.classList.toggle('visible');
        if (searchContainer.classList.contains('visible')) {
            searchContainer.querySelector('input').focus();
        }
    });

    // Fechar a pesquisa quando clicar fora dela
    document.addEventListener('click', function (event) {
        if (!searchContainer.contains(event.target) && !searchIcon.contains(event.target)) {
            searchContainer.classList.remove('visible');
        }
    });
});