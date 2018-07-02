import { Component } from '@angular/core';
import { DispensableResult } from '../../model/dispensable-result';
import { Result } from '../../model/result';

@Component({
  selector: 'app-result-presentation',
  templateUrl: './result-presentation.component.html',
  styleUrls: ['./result-presentation.component.css']
})
export class ResultPresentationComponent {

  private dispensableResult = new DispensableResult();
  private finalAspectDict = {};
  private categories = new Array<string>();
  private categoriesChartOrder = new Array<string>();
  private categoryLabels = {
    'none': 'General Comparison',
    'multiple': 'Multiple Aspects',
  };

  private sentenceCount: number; // total amount of sentences used for comparison

  showResult: boolean;

  constructor() { }

  /**
   * Saves the search result so that they can be shown in the UI.
   *
   * @param result the search results to be saved
   */
  saveResult(result: Result, finalAspDict) {
    this.finalAspectDict = finalAspDict;

    // count the number of sentences used for comparison
    this.sentenceCount = result.sentenceCount;

    const aWon = result.scoreObject1 > result.scoreObject2; // did object A win?
    if (aWon) {
      this.saveWinner(result.object1, result.object2);
      this.saveScores(result.scoreObject1, result.scoreObject2, result.totalScoreObject1, result.totalScoreObject2);
      this.saveExtractedAspects(result.extractedAspectsObject1, result.extractedAspectsObject2);
      this.saveSentences(result.sentencesObject1, result.sentencesObject2);

    } else {
      this.saveWinner(result.object2, result.object1);
      this.saveScores(result.scoreObject2, result.scoreObject1, result.totalScoreObject2, result.totalScoreObject1);
      this.saveExtractedAspects(result.extractedAspectsObject2, result.extractedAspectsObject1);
      this.saveSentences(result.sentencesObject2, result.sentencesObject1);
    }
    console.log(this.dispensableResult);
    this.showResult = true;
  }

  reset() {
    this.dispensableResult = new DispensableResult();
    this.sentenceCount = 0;
    this.showResult = false;
    this.categories = [];
    this.categoriesChartOrder = [];
  }

  /**
   * Save the winner and loser of the comparison.
   *
   * @param winner object that won the comparation
   * @param looser object that lost the comparation
   */
  private saveWinner(winner: string, looser: string) {
    this.dispensableResult.winner = winner;
    this.dispensableResult.looser = looser;
  }

  /**
   * Save the percentage of the scores for each object.
   *
   * @param winnerScore the score of the object that won the comparation
   * @param looserScore the score of the object that lost the comparation
   */
  private saveScores(winnerScores: any, looserScores: any, totalScoreA: number, totalScoreB: number) {

    this.categories = Array.from(new Set(Object.keys(winnerScores).concat(Object.keys(looserScores))));
    this.setScores(winnerScores['none'], looserScores['none'], this.categoryLabels['none']);
    if (this.categories.length > 1) {
      this.categories.forEach(key => {
        if (key !== 'none' && key !== 'multiple') {
          this.setScores(winnerScores[key], looserScores[key], key);
          this.categoryLabels[key] = key;
        }
      });

      if (this.categories.indexOf('multiple') !== -1) {
        this.setScores(winnerScores['multiple'], looserScores['multiple'], this.categoryLabels['multiple']);
      }
    }
    this.setScores(totalScoreA, totalScoreB, 'Overall Comparison');

  }

  private setScores(a: number, b: number, label: string): void {
    this.dispensableResult.winnerScoresPercent[label] = this.calcScore(a, b);
    this.dispensableResult.looserScoresPercent[label] = this.calcScore(b, a);
    this.categoriesChartOrder.push(label);
  }

  private calcScore(a: number, b: number): string {
    if (a === undefined) {
      a = 0;
    }
    if (b === undefined) {
      b = 0;
    }

    return (a / (a + b) * 100).toFixed(2);
  }

  /**
   * Save the extracted aspects for each object.
   *
   * @param winnerAspects aspects of the object that won the comparation
   * @param looserAspects aspects of the object that lost the comparation
   */
  private saveExtractedAspects(winnerAspects: Array<string>, looserAspects: Array<string>) {
    this.dispensableResult.winnerLinks = winnerAspects;
    this.dispensableResult.looserLinks = looserAspects;
  }

  /**
   * Save the clustered sentences each object has won.
   *
   * @param winnerSentences sentences of the object that won
   * @param looserSentences sentences of the object that lost
   */
  private saveSentences(winnerSentences: {}, looserSentences: {}) {
    this.dispensableResult.winnerSentences = winnerSentences;
    this.dispensableResult.looserSentences = looserSentences;
  }
}
