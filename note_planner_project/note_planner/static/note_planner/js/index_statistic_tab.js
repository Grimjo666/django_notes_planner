document.addEventListener("DOMContentLoaded", function() {
    var showStatisticButton = document.querySelector('.button-show-statistic');
    var showGraphsButton = document.querySelector('.button-show-graphs');
    var textStatisticBlock = document.querySelector('.text-statistic-block');
    var graphsStatisticBlock = document.querySelector('.graphs-statistic-block');

    showStatisticButton.addEventListener('click', function() {
        showStatistic();
    });

    showGraphsButton.addEventListener('click', function() {
        showGraphs();
    });

    function showStatistic() {
        showStatisticButton.classList.add('activ-tab');
        showGraphsButton.classList.remove('activ-tab');

        textStatisticBlock.classList.remove('hidden');
        graphsStatisticBlock.classList.add('hidden');
    }

    function showGraphs() {
        showStatisticButton.classList.remove('activ-tab');
        showGraphsButton.classList.add('activ-tab');

        textStatisticBlock.classList.add('hidden');
        graphsStatisticBlock.classList.remove('hidden');
    }
});
