import ApexCharts from "apexcharts";
import { secondsToHumanReadable } from "./common";

class Chart extends HTMLElement {
  constructor() {
    super();

    const series = JSON.parse(atob(this.dataset.series!));
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
                from: 0,
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
          // set breakpoint for small devices and also disable data labels
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
          // breakpoint from 480 up
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

customElements.define("aoc-heat-map-chart", Chart);
