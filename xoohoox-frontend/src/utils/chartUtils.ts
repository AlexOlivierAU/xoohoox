import { ChartOptions } from 'chart.js';

// MUI X-Charts theme configuration
export const muiChartTheme = {
  palette: {
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#9c27b0',
      light: '#ba68c8',
      dark: '#7b1fa2',
    },
    error: {
      main: '#d32f2f',
      light: '#ef5350',
      dark: '#c62828',
    },
    warning: {
      main: '#ed6c02',
      light: '#ff9800',
      dark: '#e65100',
    },
    info: {
      main: '#0288d1',
      light: '#03a9f4',
      dark: '#01579b',
    },
    success: {
      main: '#2e7d32',
      light: '#4caf50',
      dark: '#1b5e20',
    },
  },
};

// Chart.js default options
export const getDefaultChartOptions = (title: string): ChartOptions => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const,
      labels: {
        font: {
          size: 12,
        },
        padding: 20,
      },
    },
    title: {
      display: true,
      text: title,
      font: {
        size: 16,
        weight: 'bold',
      },
      padding: {
        top: 10,
        bottom: 30,
      },
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      titleColor: '#000',
      bodyColor: '#000',
      borderColor: '#ddd',
      borderWidth: 1,
      padding: 10,
      boxPadding: 4,
      usePointStyle: true,
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(0, 0, 0, 0.05)',
      },
      ticks: {
        font: {
          size: 11,
        },
      },
    },
    x: {
      grid: {
        display: false,
      },
      ticks: {
        font: {
          size: 11,
        },
      },
    },
  },
  interaction: {
    mode: 'nearest',
    axis: 'x',
    intersect: false,
  },
  elements: {
    line: {
      tension: 0.3,
      borderWidth: 2,
    },
    point: {
      radius: 4,
      hoverRadius: 6,
    },
  },
});

// Format data for Chart.js
export const formatChartData = (
  labels: string[],
  datasets: Array<{
    label: string;
    data: number[];
    color?: string;
    fill?: boolean;
  }>
) => {
  return {
    labels,
    datasets: datasets.map((dataset, index) => ({
      label: dataset.label,
      data: dataset.data,
      fill: dataset.fill ?? false,
      borderColor: dataset.color ?? getColorByIndex(index),
      backgroundColor: dataset.fill ? `${getColorByIndex(index)}33` : undefined,
      borderWidth: 2,
      pointBackgroundColor: getColorByIndex(index),
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: getColorByIndex(index),
    })),
  };
};

// Get color by index (for consistent colors across charts)
export const getColorByIndex = (index: number): string => {
  const colors = [
    '#1976d2', // primary
    '#9c27b0', // secondary
    '#2e7d32', // success
    '#ed6c02', // warning
    '#0288d1', // info
    '#d32f2f', // error
    '#546e7a', // blue-grey
    '#795548', // brown
    '#607d8b', // blue-grey
    '#8d6e63', // brown
  ];
  
  return colors[index % colors.length];
};

// Format date for chart labels
export const formatDateForChart = (date: Date | string): string => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString(undefined, { 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// Calculate percentage change
export const calculatePercentageChange = (current: number, previous: number): number => {
  if (previous === 0) return 0;
  return ((current - previous) / previous) * 100;
};

// Format percentage for display
export const formatPercentage = (value: number): string => {
  return `${value.toFixed(1)}%`;
};

// Generate time series data
export const generateTimeSeriesData = (
  startDate: Date,
  endDate: Date,
  interval: 'hour' | 'day' | 'week' | 'month' = 'day'
): string[] => {
  const labels: string[] = [];
  const currentDate = new Date(startDate);
  
  while (currentDate <= endDate) {
    labels.push(formatDateForChart(currentDate));
    
    switch (interval) {
      case 'hour':
        currentDate.setHours(currentDate.getHours() + 1);
        break;
      case 'day':
        currentDate.setDate(currentDate.getDate() + 1);
        break;
      case 'week':
        currentDate.setDate(currentDate.getDate() + 7);
        break;
      case 'month':
        currentDate.setMonth(currentDate.getMonth() + 1);
        break;
    }
  }
  
  return labels;
}; 