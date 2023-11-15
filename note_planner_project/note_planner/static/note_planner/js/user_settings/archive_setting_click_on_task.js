document.addEventListener("DOMContentLoaded", function () {
    var taskPriorityBlocks = document.querySelectorAll(".task-priority");
    var hiddenInput = document.querySelector("input[name='task_priority']");

    function updateStyles() {
        taskPriorityBlocks.forEach(function (block) {
            var priorityClass = block.classList[1];
            if (priorityClass === hiddenInput.value) {
                // Если блок совпадает с выбранным приоритетом, добавляем стили
                block.style.fontSize = "105%";
                block.style.width = "95%";
            } else {
                // В противном случае сбрасываем стили
                block.style.fontSize = "";
                block.style.width = "";
            }
        });
    }

    taskPriorityBlocks.forEach(function (block) {
        block.addEventListener("click", function () {
            var priorityClass = block.classList[1];
            hiddenInput.value = priorityClass;
            updateStyles();
        });
    });

    // Инициализация при загрузке страницы
    updateStyles();
});



