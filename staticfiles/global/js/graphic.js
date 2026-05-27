(() => {
    const dataElement = document.getElementById("productivity-chart-data");
    const canvas = document.getElementById("productivity-chart");

    if (!dataElement || !canvas || typeof Chart === "undefined") {
        return;
    }

    const chartData = JSON.parse(dataElement.textContent);
    const buttons = document.querySelectorAll("[data-chart-period]");
    const periodConfig = {
        weekly: {
            labels: chartData.weekly.labels,
            values: chartData.weekly.data,
            label: "Tarefas concluídas na semana",
        },
        monthly: {
            labels: chartData.monthly.labels,
            values: chartData.monthly.data,
            label: "Tarefas concluídas no mês",
        },
    };

    const sliceColors = [
        "rgba(13, 110, 253, 0.85)",
        "rgba(32, 201, 151, 0.85)",
        "rgba(255, 193, 7, 0.85)",
        "rgba(220, 53, 69, 0.85)",
        "rgba(111, 66, 193, 0.85)",
        "rgba(23, 162, 184, 0.85)",
        "rgba(253, 126, 20, 0.85)",
        "rgba(108, 117, 125, 0.85)",
    ];

    const makeSliceColors = (count) => Array.from({ length: count }, (_, index) => sliceColors[index % sliceColors.length]);

    const chart = new Chart(canvas, {
        type: "pie",
        data: {
            labels: periodConfig.weekly.labels,
            datasets: [
                {
                    label: periodConfig.weekly.label,
                    data: periodConfig.weekly.values,
                    backgroundColor: makeSliceColors(periodConfig.weekly.values.length),
                    borderColor: "#ffffff",
                    borderWidth: 2,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        usePointStyle: true,
                        pointStyle: "circle",
                        boxWidth: 10,
                        padding: 18,
                    },
                },
                tooltip: {
                    backgroundColor: "rgba(15, 23, 42, 0.95)",
                    padding: 12,
                    displayColors: true,
                },
            },
        },
    });

    const setActiveButton = (period) => {
        buttons.forEach((button) => {
            const isActive = button.dataset.chartPeriod === period;
            button.classList.toggle("btn-primary", isActive);
            button.classList.toggle("btn-outline-primary", !isActive);
        });
    };

    const updateChart = (period) => {
        const config = periodConfig[period];

        chart.data.labels = config.labels;
        chart.data.datasets[0].label = config.label;
        chart.data.datasets[0].data = config.values;
        chart.data.datasets[0].backgroundColor = makeSliceColors(config.values.length);
        chart.update();
        setActiveButton(period);
    };

    buttons.forEach((button) => {
        button.addEventListener("click", () => updateChart(button.dataset.chartPeriod));
    });

    updateChart("weekly");
})();