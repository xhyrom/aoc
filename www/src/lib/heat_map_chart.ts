import ApexCharts from "apexcharts";
import { secondsToHumanReadable } from "./common";

class Chart extends HTMLElement {
  constructor() {
    super();

    const series = JSON.parse(atob(this.dataset.series!));

    const averages = calculateDailyAverages(series);

    series.unshift({
      name: "Average",
      data: averages,
    });

    const chart = new ApexCharts(document.getElementById(this.dataset.id!), {
      chart: {
        type: "heatmap",
        height: 500,
        animations: {
          enabled: false,
        },
      },
      series,
      plotOptions: {
        heatmap: {
          shadeIntensity: 0.5,
          radius: 0,
          colorScale: {
            ranges: [
              {
                from: -Infinity,
                to: 0,
                name: "-",
                color: "#808080",
              },
              {
                from: 0.01,
                to: 10 * 60,
                name: "easy",
                color: "#1bf514",
              },
              {
                from: 10 * 60 + 1,
                to: 20 * 60,
                name: "medium",
                color: "#f5db14",
              },
              {
                from: 20 * 60 + 1,
                to: 40 * 60,
                name: "hard",
                color: "#f59014",
              },
              {
                from: 40 * 60 + 1,
                to: 80 * 60,
                name: "extreme",
                color: "#f5143d",
              },
              {
                from: 80 * 60 + 1,
                to: Number.MAX_VALUE,
                name: "insane",
                color: "#cf14f5",
              },
            ],
          },
        },
      },
      responsive: [
        {
          breakpoint: 480,
          options: {
            dataLabels: {
              enabled: false,
            },
            chart: {
              height: 300,
            },
            xaxis: {
              categories: Array.from({ length: 25 }, (_, i) => i + 1),
            },
          },
        },
        {
          breakpoint: 768,
          options: {
            dataLabels: {
              enabled: false,
            },
            chart: {
              height: 400,
            },
          },
        },
        {
          breakpoint: 1600,
          options: {
            dataLabels: {
              enabled: false,
            },
          },
        },
      ],
      dataLabels: {
        enabled: true,
        formatter: secondsToHumanReadable,
        style: {
          fontSize: "11px",
          fontFamily: "monospace",
        },
      },
      legend: {
        position: "bottom",
      },
      xaxis: {
        categories: Array.from({ length: 25 }, (_, i) => `Day ${i + 1}`),
      },
      tooltip: {
        y: {
          formatter: secondsToHumanReadable,
        },
      },
    });

    chart.render();
  }
}

const calculateDailyAverages = (series: { data: number[] }[]): number[] => {
  const numDays = series[0]!.data.length;
  const averages = [];

  for (let day = 0; day < numDays; day++) {
    let sum = 0;
    let count = 0;

    for (const serie of series) {
      if (
        serie.data[day] !== undefined &&
        serie.data[day] !== null &&
        serie.data[day]! > 0
      ) {
        sum += serie.data[day]!;
        count++;
      }
    }

    averages.push(count > 0 ? Number((sum / count).toFixed(2)) : 0);
  }

  return averages;
};

customElements.define("aoc-heat-map-chart", Chart);
