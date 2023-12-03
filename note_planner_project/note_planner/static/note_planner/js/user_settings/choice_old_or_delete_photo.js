document.addEventListener("DOMContentLoaded", function() {
    var updateToOldButton = document.querySelector('.button-update-to-old');
    var deleteButton = document.querySelector('.button-delete');
    var closeButton = document.querySelector('.button-close');
    var choiceBlock = document.querySelector('.choice-block');
    var overlay = document.querySelector('.overlay');

    function showChoiceBlock() {
        choiceBlock.classList.remove('hidden');
        overlay.classList.remove('hidden');
    }

    function hideChoiceBlock() {
        choiceBlock.classList.add('hidden');
        overlay.classList.add('hidden');
    }

    updateToOldButton.addEventListener('click', showChoiceBlock);
    deleteButton.addEventListener('click', showChoiceBlock);
//    closeButton.addEventListener('click', hideChoiceBlock);

    overlay.addEventListener('click', function(event) {
        if (event.target.classList.contains('overlay')) {
            hideChoiceBlock();
        }
    });
});
