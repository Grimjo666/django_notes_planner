document.addEventListener("DOMContentLoaded", function() {
    var overlay = document.querySelector('.overlay'); // Получаем элемент с классом "overlay"
    var addTaskBlock = document.querySelector('.add-task-block'); // Получаем элемент с классом "add-task-block"
    var addButton = document.querySelector('.button-add-task'); // Получаем кнопку с классом "button-add-task"
    var closeButton = document.querySelector('.button-close-task-form'); // Получаем кнопку с классом "button-close-task-form"

    // Функция для закрытия блока задач
    function closeTaskBlock() {
        overlay.classList.add('hidden'); // Добавляем класс "hidden" к элементу с классом "overlay"
        addTaskBlock.classList.add('hidden'); // Добавляем класс "hidden" к элементу с классом "add-task-block"
    }

    // Обработчик клика по кнопке "Добавить задачу"
    addButton.addEventListener('click', function() {
        overlay.classList.remove('hidden'); // Удаляем класс "hidden" у элемента с классом "overlay"
        addTaskBlock.classList.remove('hidden'); // Удаляем класс "hidden" у элемента с классом "add-task-block"
    });

    // Обработчик клика по кнопке "Закрыть форму задачи"
    closeButton.addEventListener('click', closeTaskBlock);

    // Обработчик клика по элементу с классом "overlay"
    overlay.addEventListener('click', function(event) {
        // Проверяем, что элемент, по которому кликнули, имеет класс "overlay"
        if (event.target.classList.contains('overlay')) {
            closeTaskBlock(); // Вызываем функцию для закрытия блока задач
        }
    });
});