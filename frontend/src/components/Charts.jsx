import React, { useEffect, useRef } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
} from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
);

// Glass morphic base colors (Tailwind-ish palette)
const colors = {
    blue: { bg: 'rgba(59, 130, 246, 0.25)', border: 'rgba(59, 130, 246, 0.6)' },
    purple: { bg: 'rgba(139, 92, 246, 0.25)', border: 'rgba(139, 92, 246, 0.6)' },
    emerald: { bg: 'rgba(16, 185, 129, 0.25)', border: 'rgba(16, 185, 129, 0.6)' },
    amber: { bg: 'rgba(245, 158, 11, 0.25)', border: 'rgba(245, 158, 11, 0.6)' },
    rose: { bg: 'rgba(244, 63, 94, 0.25)', border: 'rgba(244, 63, 94, 0.6)' },
    cyan: { bg: 'rgba(6, 182, 212, 0.25)', border: 'rgba(6, 182, 212, 0.6)' },
};

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
            labels: {
                color: '#a3a3a3',
                font: { family: "'Inter', sans-serif", size: 12 }
            }
        },
        title: { display: false },
        tooltip: {
            backgroundColor: 'rgba(23, 23, 23, 0.9)',
            titleColor: '#fff',
            bodyColor: '#a3a3a3',
            borderColor: '#2e2e2e',
            borderWidth: 1,
            padding: 10,
            cornerRadius: 8,
            displayColors: true,
        }
    },
    scales: {
        x: {
            grid: { color: 'rgba(46, 46, 46, 0.5)' },
            ticks: { color: '#737373', font: { size: 11 } },
            border: { display: false }
        },
        y: {
            grid: { color: 'rgba(46, 46, 46, 0.5)' },
            ticks: { color: '#737373', font: { size: 11 } },
            border: { display: false }
        }
    }
};

export const DistributionChart = ({ data }) => {
    const labels = Object.keys(data);
    const values = Object.values(data);

    // Cycle through glass colors
    const colorKeys = Object.keys(colors);
    const bgColors = labels.map((_, i) => colors[colorKeys[i % colorKeys.length]].bg);
    const borderColors = labels.map((_, i) => colors[colorKeys[i % colorKeys.length]].border);

    const chartData = {
        labels,
        datasets: [
            {
                label: '# of Equipment',
                data: values,
                backgroundColor: bgColors,
                borderColor: borderColors,
                borderWidth: 1,
                hoverOffset: 4
            },
        ],
    };

    return <Doughnut data={chartData} options={{
        ...chartOptions,
        cutout: '65%',
        scales: { x: { display: false }, y: { display: false } }
    }} />;
};

export const ParametersChart = ({ equipmentList }) => {
    const slice = equipmentList.slice(0, 10);
    const labels = slice.map(e => e.name);

    const data = {
        labels,
        datasets: [
            {
                label: 'Flowrate',
                data: slice.map(e => e.flowrate),
                backgroundColor: colors.blue.bg,
                borderColor: colors.blue.border,
                borderWidth: 1,
                borderRadius: 4,
                barThickness: 12,
            },
            {
                label: 'Temperature',
                data: slice.map(e => e.temperature),
                backgroundColor: colors.rose.bg,
                borderColor: colors.rose.border,
                borderWidth: 1,
                borderRadius: 4,
                barThickness: 12,
            },
            {
                label: 'Pressure (x10)',
                data: slice.map(e => e.pressure * 10),
                backgroundColor: colors.emerald.bg,
                borderColor: colors.emerald.border,
                borderWidth: 1,
                borderRadius: 4,
                barThickness: 12,
            },
        ],
    };

    return <Bar data={data} options={chartOptions} />;
};
