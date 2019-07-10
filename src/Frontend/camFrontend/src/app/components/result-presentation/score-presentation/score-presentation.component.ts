import { Component, Input, AfterViewInit, ChangeDetectorRef } from '@angular/core';
import { DispensableResult } from '../../../model/dispensable-result';
import { Chart } from 'chart.js';

@Component({
  selector: 'app-score-presentation',
  templateUrl: './score-presentation.component.html',
  styleUrls: ['./score-presentation.component.css']
})
export class ScorePresentationComponent implements AfterViewInit {

  @Input() dispensableResult: DispensableResult;
  @Input() categories: Array<string>;

  public headlineChart = [];
  public chart = [];

  private canvas: any;
  private ctx: any;
  private barThickness = 30;
  private headerThickness = 52.5;

  private headlineCanvas: any;
  private headlineCTX: any;

  constructor(private changeDetection: ChangeDetectorRef) { }

  ngAfterViewInit() {

    this.setUpHeaderChart();
    if (this.categories.length > 0) {
          this.setUpScoreChart();
    }
    this.changeDetection.detectChanges();

  }

  private setUpScoreChart() {
    this.canvas = document.getElementById('canvas');
    this.ctx = this.canvas.getContext('2d');
    this.canvas.height = (this.barThickness * this.categories.length + this.categories.length * 2 + 50) * 0.28;

    const barOptions_stacked = this.getOptions(this.barThickness,
      function () {

        const chartInstance = this.chart;
        const ctx = chartInstance.ctx;
        ctx.textAlign = 'left';
        ctx.font = '15px Roboto,"Helvetica Neue",sans-serif';
        ctx.fillStyle = '#000000';

        Chart.helpers.each(this.data.datasets.forEach(function (dataset, i) {
          Chart.helpers.each(chartInstance.controller.getDatasetMeta(i).data.forEach(function (bar, index) {
            const data = dataset.data[index];
            if (i === 0) {
              ctx.fillText(data + '%', 25, bar._model.y + 2);
            } else {
              ctx.fillText(data + '%', bar._model.x - (25 + ctx.measureText(data).width), bar._model.y + 2);
            }
          }));
        }));

        Chart.helpers.each(chartInstance.controller.getDatasetMeta(0).data.forEach((bar, index) => {
          const label = this.data.labels[index];
          const labelPositionX = (this.canvas.width / (2 * this.chart.currentDevicePixelRatio));
          ctx.textBaseline = 'middle';
          ctx.textAlign = 'center';
          ctx.fillStyle = '#000000';
          ctx.font = '20px Roboto,"Helvetica Neue",sans-serif';
          ctx.fillText(label, labelPositionX, bar._model.y);
        }));
      }
    );

    this.chart = new Chart(this.ctx, {
      type: 'horizontalBar',
      data: {
        labels: this.categories,

        datasets: [{
          data: this.obtainScores(this.dispensableResult.winnerScoresPercent),
          backgroundColor: 'rgba(24, 226, 51, 0.4)',
          hoverBackgroundColor: 'rgba(24, 226, 51, 0.1)'
        }, {
          data: this.obtainScores(this.dispensableResult.looserScoresPercent),
          backgroundColor: 'rgba(49,130,189, 0.4)',
          hoverBackgroundColor: 'rgba(49,130,189, 0.1)'
        }]
      },

      options: barOptions_stacked
    });
  }





  private setUpHeaderChart() {
    this.headlineCanvas = document.getElementById('headlineCanvas');
    this.headlineCTX = this.headlineCanvas.getContext('2d');
    this.headlineCanvas.height = 30;

    const barOptions_stacked = this.getOptions(this.headerThickness,
      function () {
        const chartInstance = this.chart;
        const ctx = chartInstance.ctx;
        ctx.textAlign = 'left';
        ctx.font = 'bold 19px Roboto,"Helvetica Neue", sans-serif';
        ctx.fillStyle = '#000000';

        Chart.helpers.each(this.data.datasets.forEach(function (dataset, i) {
          Chart.helpers.each(chartInstance.controller.getDatasetMeta(i).data.forEach(function (bar, index) {
            const data = dataset.data[index];
            const text = `${dataset.object} (${data}%)`;
            if (i === 0) {
              ctx.fillText(text, 25, bar._model.y + 2);
            } else {
              ctx.fillText(text, bar._model.x - (25 + ctx.measureText(text).width),
                bar._model.y + 2);
            }
          }));
        }));
      }
    );

    this.headlineChart = new Chart(this.headlineCTX, {
      type: 'horizontalBar',
      data: {
        datasets: [{
          data: [this.dispensableResult.winnerTotalScore],
          object: this.dispensableResult.winner,
          backgroundColor: 'rgba(24, 226, 51, 0.4)',
          hoverBackgroundColor: 'rgba(24, 226, 51, 0.1)'
        }, {
          data: [this.dispensableResult.looserTotalScore],
          object: this.dispensableResult.looser,
          backgroundColor: 'rgba(49,130,189, 0.4)',
          hoverBackgroundColor: 'rgba(49,130,189, 0.1)'
        }]
      },

      options: barOptions_stacked
    });
  }

  getOptions(barThickness, onComplete) {
    const barOptions_stacked = {
      responsive: true,
      hover: {
        animationDuration: 0
      },
      tooltips: {
        enabled: false
      },
      scales: {
        xAxes: [{
          ticks: {
            display: false
          },
          gridLines: {
            zeroLineColor: 'rgba(0,0,0,0)',
            display: true,
            color: ['rgba(0,0,0,0)', 'rgba(0,0,0,0)', 'rgba(0,0,0,0)', 'rgba(0,0,0,0)', 'rgba(0,0,0,0)',
              'rgba(255,0,0,0.4)', 'rgba(0,0,0,0)', 'rgba(0,0,0,0)', 'rgba(0,0,0,0)', 'rgba(0,0,0,0)']
          },
          stacked: true
        }],
        yAxes: [{
          display: false,
          barThickness: barThickness,
          ticks: {
            display: false
          },
          stacked: true
        }]
      },
      legend: {
        display: false
      },

      animation: {
        onComplete: onComplete
      },
      pointLabelFontFamily: 'Quadon Extra Bold',
      scaleFontFamily: 'Quadon Extra Bold',
    };
    return barOptions_stacked;
  }

  private obtainScores(dict: {}) {
    const scores = [];
    this.categories.forEach(category => {
      scores.push(dict[category]);
    });
    return scores;
  }

}
