import ApexCharts from "apexcharts";
import { numberFormatter } from "./common";

class Chart extends HTMLElement {
  private data: any;
  private chart: ApexCharts;
  static observedAttributes = ["data-year"];

  constructor() {
    super();

    this.data = JSON.parse(atob(this.dataset.data!));
    const selectedYear = this.dataset.year
      ? parseInt(this.dataset.year)
      : new Date().getFullYear();

    const selectedData = this.data.find((e: any) => e.name == selectedYear);

    const series = [
      {
        name: "First star",
        data: selectedData.data.map((e: any) => e.first).reverse(),
      },
      {
        name: "Both stars",
        data: selectedData.data.map((e: any) => e.both).reverse(),
      },
    ];

    this.chart = new ApexCharts(document.getElementById(this.dataset.id!), {
      chart: {
        type: "bar",
        height: 500,
        background: "#262626",
        stacked: true,
        animations: {
          enabled: false,
        },
      },
      theme: {
        mode: "dark",
      },
      responsive: [
        {
          // set breakpoint for small devices and also disable data labels
          breakpoint: 480,
          options: {
            dataLabels: {
              enabled: false,
            },
            plotOptions: {
              bar: {
                dataLabels: {
                  total: {
                    enabled: false,
                  },
                },
              },
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
            plotOptions: {
              bar: {
                dataLabels: {
                  total: {
                    enabled: false,
                  },
                },
              },
            },
            chart: {
              height: 400,
            },
          },
        },
      ],
      series,
      xaxis: {
        categories: Array.from({ length: 25 }, (_, i) => `Day ${i + 1}`),
      },
      plotOptions: {
        bar: {
          dataLabels: {
            total: {
              style: {
                color: "#fff",
              },
              enabled: true,
            },
          },
        },
      },
      dataLabels: {
        formatter: numberFormatter,
      },
      tooltip: {
        shared: true,
        intersect: false,
        y: {
          formatter: numberFormatter,
        },
      },
      yaxis: {
        labels: {
          formatter: numberFormatter,
        },
      },
      colors: ["#40403d", "#f5db14"],
    });

    this.chart.render();
  }

  attributeChangedCallback(_: string, __: string, newValue: string) {
    const selectedData = this.data.find((e: any) => e.name == newValue);

    const series = [
      {
        name: "First star",
        data: selectedData.data.map((e: any) => e.first).reverse(),
      },
      {
        name: "Both stars",
        data: selectedData.data.map((e: any) => e.both).reverse(),
      },
    ];

    this.chart.updateSeries(series);
  }
}

customElements.define("aoc-bar-chart", Chart);
