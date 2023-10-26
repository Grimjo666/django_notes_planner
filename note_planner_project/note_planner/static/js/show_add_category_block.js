
document.addEventListener('DOMContentLoaded', function() {
    var addCategoryButton = document.querySelector('.add-category-button');
    var categoryForm = document.getElementById('category-form');

    addCategoryButton.addEventListener('click', function(event) {
        event.preventDefault();
        categoryForm.style.display = 'block';
        addCategoryButton.style.display = 'none';
    });
});
