import { Component, OnInit, Input, AfterViewInit, ChangeDetectorRef } from '@angular/core';
import { DispensableResult } from '../../../model/dispensable-result';
import { Chart } from 'chart.js';

@Component({
  selector: 'app-score-presentation',
  templateUrl: './score-presentation.component.html',
  styleUrls: ['./score-presentation.component.css']
})
export class ScorePresentationComponent implements AfterViewInit, OnInit {

  @Input() dispensableResult: DispensableResult;
  @Input() categories: Array<string>;

  chart = [];
  canvas: any;
  ctx: any;
  barThickness = 50;

  constructor(private changeDetection: ChangeDetectorRef) { }

  ngOnInit() {}
  ngAfterViewInit() {

    this.canvas = document.getElementById('canvas');
    this.ctx = this.canvas.getContext('2d');
    console.log(this.ctx.canvas.height);
    this.canvas.height = (this.barThickness * this.categories.length + this.categories.length * 2 + 50) * 0.28;
    console.log(this.ctx.canvas.height);

    const barOptions_stacked = {
      responsive: true,
      tooltips: {
        enabled: true
      },
      hover: {
        animationDuration: 0
      },
      scales: {
        xAxes: [{
          ticks: {
            beginAtZero: true,
            fontFamily: '"Open Sans Bold", sans-serif',
            fontSize: 15,
            display: false
          },
          scaleLabel: {
            display: true
          },
          gridLines: {
            display: true,
            color: ['rgba(0,0,0,0)', 'rgba(0,0,0,0)', 'rgba(0,0,0,0)', 'rgba(0,0,0,0)', 'rgba(0,0,0,0)',
            'rgba(0,0,0,0.8)', 'rgba(0,0,0,0)', 'rgba(0,0,0,0)', 'rgba(0,0,0,0)', 'rgba(0,0,0,0)']
          },
          stacked: true
        }],
        yAxes: [{
          display: false,
          barThickness: this.barThickness,
          gridLines: {
            display: false,
          },
          ticks: {
            fontFamily: '"Open Sans Bold", sans-serif',
            fontSize: 15,
            display: false
          },
          stacked: true
        }]
      },
      legend: {
        display: false
      },

      animation: {
        onComplete: function () {

          const chartInstance = this.chart;
          const ctx = chartInstance.ctx;
          ctx.textAlign = 'left';
          ctx.font = '15px Open Sans';
          ctx.fillStyle = '#000000';

          Chart.helpers.each(this.data.datasets.forEach(function (dataset, i) {
            Chart.helpers.each(chartInstance.controller.getDatasetMeta(i).data.forEach(function (bar, index) {
              const data = dataset.data[index];
              if (i === 0) {
                ctx.fillText(data + '%', 25, bar._model.y + 4);
              } else {
                ctx.fillText(data + '%', bar._model.x - (25 + ctx.measureText(data).width), bar._model.y + 4);
              }
            }));
          }));

          Chart.helpers.each(chartInstance.controller.getDatasetMeta(0).data.forEach((bar, index) => {
            const label = this.data.labels[index];
            const labelPositionX = this.canvas.width / 2;

            ctx.textBaseline = 'middle';
            ctx.textAlign = 'center';
            ctx.fillStyle = '#000000';
            ctx.font = '25px Open Sans';
            ctx.fillText(label, labelPositionX, bar._model.y);
          }));

        }
      },
      pointLabelFontFamily: 'Quadon Extra Bold',
      scaleFontFamily: 'Quadon Extra Bold',
    };


    console.log('this.ctx' , this.ctx);
    this.chart = new Chart(this.ctx, {
      type: 'horizontalBar',
      data: {
        // labels: ['overall', 'cat1', 'cat2'],
        labels: this.categories,

        datasets: [{
          // data: [20, 30, 40],
          data: this.obtainScores(this.dispensableResult.winnerScoresPercent),
          backgroundColor: 'rgba(24, 226, 51, 0.4)',
          hoverBackgroundColor: 'rgba(24, 226, 51, 0.1)'
        }, {
          // data: [80, 70, 60],
          data: this.obtainScores(this.dispensableResult.looserScoresPercent),
          backgroundColor: 'rgba(49,130,189, 0.4)',
          hoverBackgroundColor: 'rgba(49,130,189, 0.1)'
        }]
      },

      options: barOptions_stacked
    });

    this.changeDetection.detectChanges();

  }

  private obtainScores(dict: {}) {
    const scores = [];
    this.categories.forEach(category => {
      console.log(category);
      scores.push(dict[category]);
    });
    return scores;
  }

}
