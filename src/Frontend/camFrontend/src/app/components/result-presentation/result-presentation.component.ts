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

  private winnerSentenceExamples = {}; // stores some example sentences for the first object
  private looserSentenceExamples = {}; // stores some example sentences for the second object

  // sentences to be shown for each object
  private sentenceShowNumberlistWinner = new Array<number>();
  private sentenceShowNumberlistLooser = new Array<number>();

  showResult: boolean;

  constructor() { }

  /**
   * Saves the search result so that they can be shown in the UI.
   *
   * @param result the search results to be saved
   */
  saveResult(result: Result, finalAspDict) {
    console.log('Save Result accessed');
    this.finalAspectDict = finalAspDict;
    const aWon = result.scoreObject1 > result.scoreObject2; // did object A win?
    if (aWon) {
      this.saveWinner(result.object1, result.object2);
      this.saveScores(result.scoreObject1, result.scoreObject2);
      this.saveExtractedAspects(result.extractedAspectsObject1, result.extractedAspectsObject2);
      this.saveSentences(result.sentencesObject1, result.sentencesObject2);

    } else {
      this.saveWinner(result.object2, result.object1);
      this.saveScores(result.scoreObject2, result.scoreObject1);
      this.saveExtractedAspects(result.extractedAspectsObject2, result.extractedAspectsObject1);
      this.saveSentences(result.sentencesObject2, result.sentencesObject1);
    }
    this.setSentenceShow();
    this.showResult = true;
  }

  reset() {
    this.dispensableResult = new DispensableResult();
    this.sentenceShowNumberlistWinner = new Array<number>();
    this.sentenceShowNumberlistLooser = new Array<number>();
    this.showResult = false;
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
  private saveScores(winnerScore: number, looserScore: number) {
    this.dispensableResult.winnerScorePercent = (winnerScore / (winnerScore + looserScore) * 100).toFixed(2);
    this.dispensableResult.looserScorePercent = (looserScore / (winnerScore + looserScore) * 100).toFixed(2);
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
  private saveSentences(winnerSentences: Array<string>, looserSentences: Array<string>) {
    this.winnerSentenceExamples = winnerSentences;
    this.looserSentenceExamples = looserSentences;
  }

  /**
   * Sets the amount of initially shown sentence examples for each object. The default is 10 for
   * each, but if an object has less than 10 sentences, it's set to this amount instead.
   *
   */
  private setSentenceShow() {
    const minW = Math.min(9, Object.keys(this.winnerSentenceExamples).length);
    const minL = Math.min(9, Object.keys(this.looserSentenceExamples).length);
    this.sentenceShowNumberlistWinner = Array.from(Array(minW).keys());
    this.sentenceShowNumberlistLooser = Array.from(Array(minL).keys());
  }

  /**
   * Shows 10 more sentences in the result table for both objects or, if an object has less than 10
   * sentences left to be shown, instead only the remaining sentences will be added.
   *
   */
  showMoreSentences() {
    this._showMoreSentences(this.winnerSentenceExamples, this.sentenceShowNumberlistWinner);
    this._showMoreSentences(this.looserSentenceExamples, this.sentenceShowNumberlistLooser);
  }

  private _showMoreSentences(sentecesExamples, showNumber) {
    const minW = Math.min(10, Object.keys(sentecesExamples).length - showNumber[showNumber.length - 1] - 1);
    for (let i = 0; i < minW; i++) {
      showNumber.push(showNumber[showNumber.length - 1] + 1);
    }
  }
}
