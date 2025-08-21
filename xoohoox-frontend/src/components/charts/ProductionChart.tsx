import React from 'react';
import { Line } from 'react-chartjs-2';
import { LineChart } from '@mui/x-charts';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

// Types for our props
interface ProductionChartProps {
  data: {
    labels: string[];
    values: number[];
  };
  title: string;
  useMUI?: boolean;
}

export const ProductionChart: React.FC<ProductionChartProps> = ({
  data,
  title,
  useMUI = false
}) => {
  // If using MUI X-Charts
  if (useMUI) {
    return (
      <LineChart
        xAxis={[{ 
          data: data.labels,
          label: 'Time Period',
          scaleType: 'band'
        }]}
        series={[
          {
            data: data.values,
            label: title,
            area: true,
          }
        ]}
        width={600}
        height={400}
        margin={{ left: 70, right: 30, top: 50, bottom: 50 }}
        sx={{
          '.MuiLineElement-root': {
            strokeWidth: 2,
          },
        }}
      />
    );
  }

  // Using Chart.js
  const chartData = {
    labels: data.labels,
    datasets: [
      {
        label: title,
        data: data.values,
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: title,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Production Volume',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Time Period',
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default ProductionChart; 