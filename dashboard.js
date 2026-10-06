/* ==========================================================================
   DEEPGUARD AI - CHART.JS DASHBOARD INTERACTIVE VISUALIZATIONS
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initUserDashboardCharts();
    initAdminDashboardCharts();
});

function initUserDashboardCharts() {
    const distCanvas = document.getElementById('chart-distribution');
    const mediaCanvas = document.getElementById('chart-media');

    if (!distCanvas || !window.USER_CHART_DATA) return;

    const data = window.USER_CHART_DATA;

    // Distribution Chart (Real vs Fake)
    new Chart(distCanvas, {
        type: 'doughnut',
        data: {
            labels: ['Likely Real', 'Possibly Fake'],
            datasets: [{
                data: [data.distribution.real, data.distribution.fake],
                backgroundColor: ['#10b981', '#f43f5e'],
                borderColor: '#060911',
                borderWidth: 3,
                hoverOffset: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#94a3b8', font: { family: 'Inter', size: 12 } }
                }
            },
            cutout: '70%'
        }
    });

    // Media Type Chart (Image vs Video)
    if (mediaCanvas) {
        new Chart(mediaCanvas, {
            type: 'bar',
            data: {
                labels: ['Images', 'Videos'],
                datasets: [{
                    label: 'Analyzed Media',
                    data: [data.media_type.image, data.media_type.video],
                    backgroundColor: ['#00f0ff', '#8b5cf6'],
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                    y: { ticks: { color: '#94a3b8', stepSize: 1 }, grid: { color: 'rgba(255,255,255,0.05)' } }
                }
            }
        });
    }
}

function initAdminDashboardCharts() {
    const dailyCanvas = document.getElementById('admin-chart-daily');
    if (!dailyCanvas || !window.ADMIN_CHART_DATA) return;

    const data = window.ADMIN_CHART_DATA;

    new Chart(dailyCanvas, {
        type: 'line',
        data: {
            labels: data.daily.labels,
            datasets: [{
                label: 'System Scans',
                data: data.daily.counts,
                borderColor: '#00f0ff',
                backgroundColor: 'rgba(0, 240, 255, 0.12)',
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#00f0ff',
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#94a3b8' } }
            },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                y: { ticks: { color: '#94a3b8', stepSize: 1 }, grid: { color: 'rgba(255,255,255,0.05)' } }
            }
        }
    });
}
