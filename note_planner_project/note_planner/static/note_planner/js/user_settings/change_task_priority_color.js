
document.addEventListener("DOMContentLoaded", function () {
    var redSlider = document.getElementById("red");
    var greenSlider = document.getElementById("green");
    var blueSlider = document.getElementById("blue");
    var alphaSlider = document.getElementById("alpha");

    function updateBorderColor() {
        var hiddenInput = document.querySelector("input[name='task_priority']");
        var priorityClass = hiddenInput.value;
        var block = document.querySelector("." + priorityClass);
        var invertedAlpha = 255 - alphaSlider.value;
        block.style.borderLeftColor = `rgb(${redSlider.value}, ${greenSlider.value}, ${blueSlider.value}, ${invertedAlpha / 255})`;
    }

    redSlider.addEventListener("input", function () {
        updateBorderColor();
    });

    greenSlider.addEventListener("input", function () {
        updateBorderColor();
    });

    blueSlider.addEventListener("input", function () {
        updateBorderColor();
    });

    alphaSlider.addEventListener("input", function () {
        updateBorderColor();
    });
});

