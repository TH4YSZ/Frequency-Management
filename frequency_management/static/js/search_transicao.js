document.addEventListener('DOMContentLoaded', function () {
    const searchIcon = document.getElementById('search-icon');
    const searchContainer = document.getElementById('search-container');

    searchIcon.addEventListener('click', function () {
        searchContainer.classList.toggle('visible');
        if (searchContainer.classList.contains('visible')) {
            setTimeout(() => {
                searchContainer.querySelector('input').focus();
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
});