document.addEventListener("DOMContentLoaded", function() {
    var showDescriptionButtons = document.querySelectorAll('.button-show-description');
    var addSubtaskButtons = document.querySelectorAll('.add-subtask-bottom');
    var detailedTaskBlocks = document.querySelectorAll('.more-detailed-task');
    var addSubtaskBlocks = document.querySelectorAll('.add-subtask-block');
    var saveButtons = document.querySelectorAll('.save-button');
    var showSubtaskDescriptionButtons = document.querySelectorAll('.button-show-subtask-description');

    showSubtaskDescriptionButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var subtaskId = button.classList[1].split('-')[2];
            var subtaskDescription = document.querySelector('.subtask-description.subtask-id-' + subtaskId);
            subtaskDescription.classList.toggle('hidden');
        });
    });

    showDescriptionButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var taskId = button.classList[1].split('-')[2];
            var detailedTaskBlock = document.querySelector('.task-id-' + taskId + '.more-detailed-task');
            detailedTaskBlock.classList.toggle('hidden');
        });
    });

    addSubtaskButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var taskId = button.classList[1].split('-')[2];
            var addSubtaskBlock = document.querySelector('.task-id-' + taskId + '.add-subtask-block');
            var addSubtaskButton = document.querySelector('.task-id-' + taskId + '.add-subtask-bottom');
            addSubtaskBlock.classList.toggle('hidden');
            addSubtaskButton.classList.toggle('hidden');
        });
    });

    saveButtons.forEach(function(button) {
        button.addEventListener('click', async function(event) {
            // Отправить форму программно
            var form = button.closest('form');
            await form.submit(); // Ждать завершения отправки

            // После завершения отправки, скрыть блоки
            var taskId = button.classList[1].split('-')[2];
            var addSubtaskBlock = document.querySelector('.task-id-' + taskId + '.add-subtask-block');
            var addSubtaskButton = document.querySelector('.task-id-' + taskId + '.add-subtask-bottom');
            addSubtaskBlock.classList.add('hidden');
            addSubtaskButton.classList.remove('hidden');
        });
    });
});

    saveButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            var taskId = button.classList[1].split('-')[2];
            var addSubtaskBlock = document.querySelector('.task-id-' + taskId + '.add-subtask-block');
            var addSubtaskButton = document.querySelector('.task-id-' + taskId + '.add-subtask-bottom');
            addSubtaskBlock.classList.toggle('hidden');
            addSubtaskButton.classList.toggle('hidden');
        });
    });
