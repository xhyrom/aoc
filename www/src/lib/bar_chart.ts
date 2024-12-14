import ApexCharts from "apexcharts";
import { numberFormatter } from "./common";

class Chart extends HTMLElement {
  private data: any;
  private chart: ApexCharts;
  static observedAttributes = ["data-year"];

  constructor() {
    super();

    this.data = JSON.parse(atob(this.dataset.data!));
    let selectedYear = this.dataset.year ? parseInt(this.dataset.year) : null;

    if (!selectedYear) {
      selectedYear = new Date().getFullYear();

      if (new Date().getMonth() < 11) {
        selectedYear--;
      }
    }

    const selectedData = this.data.find((e: any) => e.name == selectedYear);

    const series = [
      {
        name: "First star",
        data: selectedData.data.map((e: any) => e.first).reverse(),
        type: "bar",
      },
      {
        name: "Both stars",
        data: selectedData.data.map((e: any) => e.both).reverse(),
        type: "bar",
      },
      {
        name: "Trend",
        data: createSlopePoints(selectedData),
        type: "line",
      },
    ];

    this.chart = new ApexCharts(document.getElementById(this.dataset.id!), {
      chart: {
        type: "bar",
        height: 500,
        stacked: true,
        animations: {
          enabled: false,
        },
      },
      responsive: [
        {
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
              enabled: true,
              style: {
                fontSize: "11px",
                fontFamily: "monospace",
              },
            },
          },
        },
      },
      dataLabels: {
        enabled: true,
        enabledOnSeries: [0, 1],
        formatter: numberFormatter,
        style: {
          fontSize: "11px",
          fontFamily: "monospace",
        },
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
      stroke: {
        width: [0, 0, 3],
        curve: "smooth",
      },
      colors: ["#40403d", "#f5db14", "#ff0000"],
    });

    this.chart.render();
  }

  attributeChangedCallback(_: string, __: string, newValue: string) {
    const selectedData = this.data.find((e: any) => e.name == newValue);

    const series = [
      {
        name: "First star",
        data: selectedData.data.map((e: any) => e.first).reverse(),
        type: "bar",
      },
      {
        name: "Both stars",
        data: selectedData.data.map((e: any) => e.both).reverse(),
        type: "bar",
      },
      {
        name: "Trend",
        data: createSlopePoints(selectedData),
        type: "line",
      },
    ];

    this.chart.updateSeries(series);
  }
}

const createSlopePoints = (data) => {
  const points = [];
  const maxY = Math.max(...data.data.map((e: any) => e.first + e.both));
  for (let x = 0; x < 25; x++) {
    const y = maxY * Math.exp(-0.15 * x);
    points.push(Math.max(0, y));
  }
  return points;
};

customElements.define("aoc-bar-chart", Chart);
