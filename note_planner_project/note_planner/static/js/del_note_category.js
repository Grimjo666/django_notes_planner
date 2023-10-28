document.addEventListener('DOMContentLoaded', function() {
    var overlay = document.getElementById('overlay');
    var delCategoryButton = document.querySelector('.del-category-button');
    var categoryButtons = document.querySelectorAll('.category-button');

    delCategoryButton.addEventListener('click', function(event) {
        event.preventDefault();
        overlay.style.display = 'block'; // Показать затемненный фон

        categoryButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                var latinName = this.value;
                // Отправьте запрос на сервер для удаления категории с помощью JavaScript или AJAX
                // ...

                overlay.style.display = 'none'; // Скрываем затемненный фон после удаления категории
            });
        });
    });
});

