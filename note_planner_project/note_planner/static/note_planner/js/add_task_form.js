document.addEventListener("DOMContentLoaded", function() {
    var overlay = document.querySelector('.overlay');
    var addTaskBlock = document.querySelector('.add-task-block');
    var addButton = document.querySelector('.button-add-task');
    var closeButton = document.querySelector('.button-close-task-form');
    var saveButton = document.querySelector('.save-task-button'); // Добавлено: кнопка сохранения

    function closeTaskBlock() {
        overlay.classList.add('hidden');
        addTaskBlock.classList.add('hidden');
    }

    function openTaskBlock() {
        overlay.classList.remove('hidden');
        addTaskBlock.classList.remove('hidden');
    }

    addButton.addEventListener('click', openTaskBlock);

    closeButton.addEventListener('click', closeTaskBlock);

    overlay.addEventListener('click', function(event) {
        if (event.target.classList.contains('overlay')) {
            closeTaskBlock();
        }
    });

    // Добавлено: обработчик клика по кнопке "Сохранить"
    saveButton.addEventListener('click', function() {
        // Проверка валидности формы
        var formIsValid = validateTaskForm(); // Замените на функцию, которая проверяет валидность формы

        // Если форма валидна, закрываем блок задач
        if (formIsValid) {
            closeTaskBlock();
        }
    });

    // Добавлено: функция для проверки валидности формы (замените на свою логику)
    function validateTaskForm() {
        // Реализуйте вашу логику проверки валидности формы
        // Верните true, если форма валидна, и false в противном случае
        return false;
    }
});
