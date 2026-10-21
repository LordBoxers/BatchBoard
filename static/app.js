const chartInstances = {};
const POLL_INTERVAL_MS = 300000; // 5 minutter

async function loadBatchData() {
  try {
    const response = await fetch('/api/batch/current');
    if (!response.ok) {
      throw new Error(`HTTP fejl: ${response.status}`);
    }
    const payload = await response.json();

    updateHeader(payload.metadata);

    for (const [key, chartConfig] of Object.entries(payload.charts)) {
      renderOrUpdateChart(key, chartConfig);
    }
  } catch (error) {
    console.error("Kunne ikke hente batchdata:", error);
  }
}

function updateHeader(meta) {
  document.getElementById('batchName').textContent = meta.batch_name;
  document.getElementById('recipeName').textContent = meta.recipe;
  document.getElementById('batchStatus').textContent = meta.status;
  document.getElementById('lastUpdated').textContent = meta.last_updated;
}

function renderOrUpdateChart(chartKey, config) {
  const canvasId = `chart-${chartKey}`;
  const titleId = `title-${chartKey}`;

  const titleElem = document.getElementById(titleId);
  if (titleElem) {
    titleElem.textContent = `${config.title} (${config.unit})`;
  }

  if (chartInstances[chartKey]) {
    const chart = chartInstances[chartKey];
    chart.data.labels = config.labels;
    config.series.forEach((s, idx) => {
      if (chart.data.datasets[idx]) {
        chart.data.datasets[idx].data = s.data;
      }
    });
    chart.update();
    return;
  }

  const datasets = config.series.map(s => ({
    label: s.name,
    data: s.data,
    borderColor: s.color,
    backgroundColor: s.color + '22',
    borderWidth: 2,
    tension: 0.25,
    fill: false,
    pointRadius: 2
  }));

  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  chartInstances[chartKey] = new Chart(ctx, {
    type: 'line',
    data: {
      labels: config.labels,
      datasets: datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      scales: {
        x: {
          grid: { color: '#21262d' },
          ticks: { color: '#8b949e', maxRotation: 45, minRotation: 45 }
        },
        y: {
          grid: { color: '#21262d' },
          ticks: { color: '#8b949e' }
        }
      },
      plugins: {
        legend: {
          labels: { color: '#c9d1d9' }
        }
      }
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  loadBatchData();
  setInterval(loadBatchData, POLL_INTERVAL_MS);
});