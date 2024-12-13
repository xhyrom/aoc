import ApexCharts from "apexcharts";
import { secondsToHumanReadable, yearsBetween } from "./common";

class Chart extends HTMLElement {
  constructor() {
    super();

    const series = JSON.parse(atob(this.dataset.series!));
    const chart = new ApexCharts(document.getElementById(this.dataset.id!), {
      chart: {
        type: "line",
        height: 500,
        animations: {
          enabled: false,
        },
      },
      series,
      xaxis: {
        categories: Array.from({ length: 25 }, (_, i) => `Day ${i + 1}`),
      },
      colors: [
        "#008FFB", // Light Blue
        "#00E396", // Green
        "#FEB019", // Yellow
        "#f514f1", // Pink
        "#775DD0", // Purple
        "#546E7A", // Gray-Blue
        "#26a69a", // Teal
        "#29388c", // Navy Blue
        "#fc0303", // Red
        "#ff5733", // Orange
        "#33ff57", // Lime Green
        "#5733ff", // Indigo
        "#ffd700", // Gold
        "#ff1493", // Deep Pink
        "#00ced1", // Dark Turquoise
        "#7fffd4", // Aquamarine
        "#d2691e", // Chocolate
        "#b22222", // Firebrick
        "#4b0082", // Indigo
        "#adff2f", // Green Yellow
      ],
      stroke: {
        curve: "smooth",
        width: yearsBetween(2015).map((year) =>
          year == new Date().getFullYear() ? 5 : 2,
        ),
      },
      legend: {
        tooltipHoverFormatter: (val, opts) => {
          const value =
            opts.w.globals.series[opts.seriesIndex][opts.dataPointIndex];
          const hours = Math.floor(value / 60 / 60);
          const minutes = Math.floor((value - hours * 60 * 60) / 60);
          const seconds = value - hours * 60 * 60 - minutes * 60;
          return val + " - " + `${hours}h ${minutes}m ${seconds}s` + "";
        },
      },
      tooltip: {
        shared: true,
        y: {
          formatter: secondsToHumanReadable,
        },
      },
      yaxis: {
        min: minInSeries(series),
        max: maxInSeries(series),
        labels: {
          formatter: secondsToHumanReadable,
        },
        logarithmic: true,
      },
    });

    chart.render();
  }
}

const minInSeries = (series: { data: number[] }[]) => {
  let min = Infinity;
  for (const serie of series) {
    for (const value of serie.data) {
      if (value < min) {
        min = value;
      }
    }
  }
  return min;
};

const maxInSeries = (series: { data: number[] }[]) => {
  let max = -Infinity;
  for (const serie of series) {
    for (const value of serie.data) {
      if (value > max) {
        max = value;
      }
    }
  }
  return max;
};

customElements.define("aoc-line-chart", Chart);
