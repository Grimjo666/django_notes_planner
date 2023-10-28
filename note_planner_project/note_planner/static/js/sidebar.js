document.addEventListener('DOMContentLoaded', function() {
    var innerUserBlock = document.querySelector('.inner-user-block');
    var hiddenUserBlock = document.querySelector('.hidden-user-block');

    innerUserBlock.addEventListener('click', function() {
        if (hiddenUserBlock.style.display === 'block') {
            hiddenUserBlock.style.display = 'none'; // Если видим, скрываем
        } else {
            hiddenUserBlock.style.display = 'block'; // Иначе делаем видимым
        }
    });
});
