document.addEventListener("DOMContentLoaded", function () {
    var form = document.querySelector("form");

    form.addEventListener("submit", function () {
        // Обновляем значения ползунков перед отправкой формы
        document.querySelector("input[name='red']").value = document.getElementById("red").value;
        document.querySelector("input[name='green']").value = document.getElementById("green").value;
        document.querySelector("input[name='blue']").value = document.getElementById("blue").value;
        document.querySelector("input[name='alpha']").value = document.getElementById("alpha").value;
    });
});