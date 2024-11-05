document.addEventListener('DOMContentLoaded', function () {
    const searchIcon = document.getElementById('search-icon');
    const searchContainer = document.getElementById('search-container');

    // Verifique se os elementos existem antes de adicionar o evento
    if (searchIcon && searchContainer) {
        searchIcon.addEventListener('click', function () {
            searchContainer.classList.toggle('visible');
            if (searchContainer.classList.contains('visible')) {
                setTimeout(() => {
                    const input = searchContainer.querySelector('input');
                    if (input) input.focus();
                }, 500);
            }
        });

        document.addEventListener('click', function (event) {
            if (
                !searchContainer.contains(event.target) &&
                !searchIcon.contains(event.target)
            ) {
                searchContainer.classList.remove('visible');
            }
        });
    }
});



