import { Component } from '@angular/core';
import { Result } from '../../model/result';
import { ClustererService } from '../../shared/clusterer.service';

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
  saveResult(result, finalAspDict) {
    console.log('Save Result accessed');
    // count the number of sentences used for comparison
    console.log(result);
    this.sentenceCount = result['object 1 sentences'].length + result['object 2 sentences'].length;

    const a_won = result['score object 1'] > result['score object 2']; // did object A win?
    this.saveWinner(result, a_won);
    this.saveScores(result, a_won);
    this.saveExtractedAspects(result, a_won);
    this.saveSentences(result, a_won, finalAspDict);
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
   * @param result search result of Elastic Search
   * @param a_won did object A win?
   */
  saveWinner(result, a_won) {
    if (a_won) {
      this.result.winner = result['object 1'];
      this.result.looser = result['object 2'];
    } else {
      this.result.winner = result['object 2'];
      this.result.looser = result['object 1'];
    }
  }

  /**
   * Save the percentage of the scores for each object.
   *
   * @param result search result of Elastic Search
   * @param a_won did object A win?
   */
  saveScores(result, a_won) {
    if (a_won) {
      this.result.winnerScorePercent = (
        result['score object 1'] /
        (result['score object 1'] + result['score object 2']) *
        100
      ).toFixed(2);
      this.result.looserScorePercent = (
        result['score object 2'] /
        (result['score object 1'] + result['score object 2']) *
        100
      ).toFixed(2);
    } else {
      this.result.winnerScorePercent = (
        result['score object 2'] /
        (result['score object 1'] + result['score object 2']) *
        100
      ).toFixed(2);
      this.result.looserScorePercent = (
        result['score object 1'] /
        (result['score object 1'] + result['score object 2']) *
        100
      ).toFixed(2);
    }
  }

  /**
   * Save the extracted aspects for each object.
   *
   * @param result search result of Elastic Search
   * @param a_won did object A win?
   */
  saveExtractedAspects(result, a_won) {
    if (a_won) {
      for (const link of result['extracted aspects object 1']) {
        this.result.winnerAspects.push(link);
      }
      for (const link of result['extracted aspects object 2']) {
        this.result.looserAspects.push(link);
      }
    } else {
      for (const link of result['extracted aspects object 1']) {
        this.result.looserAspects.push(link);
      }
      for (const link of result['extracted aspects object 2']) {
        this.result.winnerAspects.push(link);
      }
    }
  }

  /**
   * Save the clustered sentences each object has won.
   *
   * @param result search result of Elastic Search
   * @param a_won did object A win?
   */
  saveSentences(result, a_won, finalAspDict) {
    let i = 0;
    if (a_won) {
      for (const sentence of result['object 1 sentences']) {
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
      for (const sentence of result['object 2 sentences']) {
        this.looserSentenceExamples[i++] = this.clustererService.getCluster(
          sentence,
          this.result.winnerAspects,
          this.result.looserAspects,
          finalAspDict,
          this.result.winner,
          this.result.looser
        );
      }
    } else {
      for (const sentence of result['object 1 sentences']) {
        this.looserSentenceExamples[i++] = this.clustererService.getCluster(
          sentence,
          this.result.winnerAspects,
          this.result.looserAspects,
          finalAspDict,
          this.result.winner,
          this.result.looser
        );
      }
      i = 0;
      for (const sentence of result['object 2 sentences']) {
        this.winnerSentenceExamples[i++] = this.clustererService.getCluster(
          sentence,
          this.result.winnerAspects,
          this.result.looserAspects,
          finalAspDict,
          this.result.winner,
          this.result.looser
        );
      }
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
