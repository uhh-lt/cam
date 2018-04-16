import { Component } from '@angular/core';
import { Result } from '../../model/result';
import { ClustererService } from '../../shared/clusterer.service';
import { RequestResult } from '../../model/request-result';

@Component({
  selector: 'app-result-presentation',
  templateUrl: './result-presentation.component.html',
  styleUrls: ['./result-presentation.component.css']
})
export class ResultPresentationComponent {

  private result = new Result();
  private winnerSentenceExamples = {}; // stores some example sentences for the first object
  private looserSentenceExamples = {}; // stores some example sentences for the second object

  // sentences to be shown for each object
  private sentenceShowNumberlistWinner = new Array<number>();
  private sentenceShowNumberlistLooser = new Array<number>();

  private sentenceCount: number; // total amount of sentences used for comparison

  private showResult: boolean;


  constructor(private clustererService: ClustererService) { }

  /**
   * Saves the search result so that they can be shown in the UI.
   *
   * @param result the search results to be saved
   */
  saveResult(result: RequestResult, finalAspDict) {
    console.log('Save Result accessed');
    // count the number of sentences used for comparison
    console.log(result);
    this.sentenceCount = result['object 1 sentences'].length + result['object 2 sentences'].length;

    const aWon = result['score object 1'] > result['score object 2']; // did object A win?
    if (aWon) {
      this.saveWinner(result['object 1'], result['object 2']);
      this.saveScores(result['score object 1'], result['score object 2']);
      this.saveExtractedAspects(result['extracted aspects object 1'], result['extracted aspects object 2']);
      this.saveSentences(result['object 1 sentences'], result['object 2 sentences'], finalAspDict);

    } else {
      this.saveWinner(result['object 2'], result['object 1']);
      this.saveScores(result['score object 2'], result['score object 1']);
      this.saveExtractedAspects(result['extracted aspects object 2'], result['extracted aspects object 1']);
      this.saveSentences(result['object 2 sentences'], result['object 1 sentences'], finalAspDict);
    }
    this.setSentenceShow();
    this.showResult = true;
  }

  reset() {
    this.result = new Result();
    this.sentenceShowNumberlistWinner = new Array<number>();
    this.sentenceShowNumberlistLooser = new Array<number>();
    this.sentenceCount = 0;
    this.showResult = false;
  }

  /**
   * Save the winner and loser of the comparison.
   *
   * @param winner object that won the comparation
   * @param looser object that lost the comparation
   */
  saveWinner(winner: string, looser: string) {
    this.result.winner = winner;
    this.result.looser = looser;
  }

  /**
   * Save the percentage of the scores for each object.
   *
   * @param winnerScore the score of the object that won the comparation
   * @param looserScore the score of the object that lost the comparation
   */
  saveScores(winnerScore: number, looserScore: number) {
    this.result.winnerScorePercent = (
      winnerScore /
      (winnerScore + looserScore) *
      100
    ).toFixed(2);
    this.result.looserScorePercent = (
      looserScore /
      (winnerScore + looserScore) *
      100
    ).toFixed(2);
  }

  /**
   * Save the extracted aspects for each object.
   *
   * @param winnerAspects aspects of the object that won the comparation
   * @param looserAspects aspects of the object that lost the comparation
   */
  saveExtractedAspects(winnerAspects: Array<string>, looserAspects: Array<string>) {
    for (const link of winnerAspects) {
      this.result.winnerAspects.push(link);
    }
    for (const link of looserAspects) {
      this.result.looserAspects.push(link);
    }
  }

  /**
   * Save the clustered sentences each object has won.
   *
   * @param winnerSentences sentences of the object that won
   * @param looserSentences sentences of the object that lost
   * @param finalAspDict dict that holds all aspects of the comparation
   */
  saveSentences(winnerSentences: Array<string>, looserSentences: Array<string>, finalAspDict) {
    let i = 0;
    for (const sentence of winnerSentences) {
      this.winnerSentenceExamples[i++] = this.clustererService.getCluster(
        sentence,
        this.result.winnerAspects,
        this.result.looserAspects,
        finalAspDict,
        this.result.winner,
        this.result.looser
      );
    }
    i = 0;
    for (const sentence of looserSentences) {
      this.looserSentenceExamples[i++] = this.clustererService.getCluster(
        sentence,
        this.result.winnerAspects,
        this.result.looserAspects,
        finalAspDict,
        this.result.winner,
        this.result.looser
      );
    }
  }
  /**
   * Sets the amount of initially shown sentence examples for each object. The default is 10 for
   * each, but if an object has less than 10 sentences, it's set to this amount instead.
   *
   */
  setSentenceShow() {
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
    let i1 = 0;
    const minW = Math.min(
      10,
      Object.keys(this.winnerSentenceExamples).length -
      this.sentenceShowNumberlistWinner[
      this.sentenceShowNumberlistWinner.length - 1
      ] -
      1
    );
    while (i1 < minW) {
      this.sentenceShowNumberlistWinner.push(
        this.sentenceShowNumberlistWinner[
        this.sentenceShowNumberlistWinner.length - 1
        ] + 1
      );
      i1++;
    }
    let i2 = 0;
    const minL = Math.min(
      10,
      Object.keys(this.looserSentenceExamples).length -
      this.sentenceShowNumberlistLooser[
      this.sentenceShowNumberlistLooser.length - 1
      ] -
      1
    );
    while (i2 < minL) {
      this.sentenceShowNumberlistLooser.push(
        this.sentenceShowNumberlistLooser[
        this.sentenceShowNumberlistLooser.length - 1
        ] + 1
      );
      i2++;
    }
  }
}
