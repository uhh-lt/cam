import { Component, Input } from '@angular/core';
import { UrlBuilderService } from './shared/url-builder.service';
import { ClustererService } from './shared/clusterer.service';
import { HttpRequestService } from './shared/http-request.service';

/**
 * UI for the Comparative Argument Machine. Currently everything is done by this one class --
showing the UI, reading the input and requesting the Elastic Search.
 *
 * @export
 * @class AppComponent
 */
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'CAM';
  aspects = [1]; // the rows of aspects currently shown in the UI
  aspectDict = {}; // the aspects currently entered
  finalAspDict = {}; // holds all aspects after compare() was called
  weightDict = { 1: 1 }; // the weightings of the aspects currently chosen with the sliders
  selectedModel = 'default'; // the comparison model to be used
  fastSearch = false; // the possibility to do a fast comparison
  loadshow = false; // boolean that checks if the loading screen should be shown
  resshow = false; // boolean that checks if the result table should be shown
  rescount = 0; // total amount of sentences used for comparison
  object_A = ''; // the first object currently entered
  object_B = ''; // the second object currently entered
  winner_obj = ''; // the winning object of the results shown
  loser_obj = ''; // the losing object of the results shown
  winner_score = ''; // stores the score of the first object
  loser_score = ''; // stores the score of the second object
  winner_links = []; // stores the main links of the first object
  loser_links = []; // stores the main links of the second object
  winner_sentex = {}; // stores some example sentences for the first object
  loser_sentex = {}; // stores some example sentences for the second object
  // sentences to be shown for each object
  sentence_show_numberlist_winner = [];
  sentence_show_numberlist_loser = [];

  constructor(private urlbuilderService: UrlBuilderService, private clustererService: ClustererService,
    private httpRequestService: HttpRequestService) { }

  /**
   * Reads the input from the UI, starts the search request and calls the save method.
   */
  compare() {
    this.loadshow = true; // show the loading screen
    this.reset(); // reset everything to its default and hide the result table
    // read the aspects entered by the user and store them with their weight
    for (const aspect of this.aspects) {
      if (this.aspectDict[aspect] !== undefined) {
        this.finalAspDict[this.aspectDict[aspect].trim()] = this.weightDict[
          aspect
        ];
      }
    }
    // read the objects entered, build the URL and start the search request
    this.saveObjects();
    this.httpRequestService.getScore(this.urlbuilderService.buildURL(this.object_A, this.object_B,
      this.finalAspDict, this.selectedModel, this.fastSearch)
    )
      .subscribe(async res => {
        await this.saveResult(res);
      });
  }

  /**
   * reset all results to its default and hide the result table.
   *
   */
  reset() {
    this.resshow = false;
    this.rescount = 0;
    this.winner_links = [];
    this.loser_links = [];
    this.winner_sentex = {};
    this.loser_sentex = {};
    this.finalAspDict = {};
    this.sentence_show_numberlist_winner = [];
    this.sentence_show_numberlist_loser = [];
  }

  resetInput() {
    this.object_A = '';
    this.object_B = '';
    for (const aspect of Object.keys(this.aspectDict)) {
      this.aspectDict[aspect] = '';
    }
    this.aspects = [1];
    this.fastSearch = false;
  }

  /**
   * Saves the search result so that they can be shown in the UI.
   *
   * @param result the search results to be saved
   */
  saveResult(result) {
    this.resshow = true; // show the result table
    // count the number of sentences used for comparison
    this.rescount =
      result['object 1 sentences'].length + result['object 2 sentences'].length;
    const a_won = result['score object 1'] > result['score object 2']; // did object A win?
    this.saveWinner(result, a_won);
    this.saveScores(result, a_won);
    this.saveExtractedAspects(result, a_won);
    this.saveSentences(result, a_won);
    this.setSentenceShow();
    this.loadshow = false; // hide the loading screen
  }

  /**
   * Sets the amount of initially shown sentence examples for each object. The default is 10 for
   * each, but if an object has less than 10 sentences, it's set to this amount instead.
   *
   */
  setSentenceShow() {
    const minW = Math.min(9, Object.keys(this.winner_sentex).length);
    const minL = Math.min(9, Object.keys(this.loser_sentex).length);
    this.sentence_show_numberlist_winner = Array.from(Array(minW).keys());
    this.sentence_show_numberlist_loser = Array.from(Array(minL).keys());
  }

  /**
   * Save the trimmed objects that were entered after compare() was called.
   *
   */
  saveObjects() {
    this.object_A = this.object_A.trim();
    this.object_B = this.object_B.trim();
  }

  /**
   * Save the winner and loser of the comparison.
   *
   * @param result search result of Elastic Search
   * @param a_won did object A win?
   */
  saveWinner(result, a_won) {
    if (a_won) {
      this.winner_obj = result['object 1'];
      this.loser_obj = result['object 2'];
    } else {
      this.winner_obj = result['object 2'];
      this.loser_obj = result['object 1'];
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
      this.winner_score = (
        result['score object 1'] /
        (result['score object 1'] + result['score object 2']) *
        100
      ).toFixed(2);
      this.loser_score = (
        result['score object 2'] /
        (result['score object 1'] + result['score object 2']) *
        100
      ).toFixed(2);
    } else {
      this.winner_score = (
        result['score object 2'] /
        (result['score object 1'] + result['score object 2']) *
        100
      ).toFixed(2);
      this.loser_score = (
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
        this.winner_links.push(link);
      }
      for (const link of result['extracted aspects object 2']) {
        this.loser_links.push(link);
      }
    } else {
      for (const link of result['extracted aspects object 1']) {
        this.loser_links.push(link);
      }
      for (const link of result['extracted aspects object 2']) {
        this.winner_links.push(link);
      }
    }
  }

  /**
   * Save the clustered sentences each object has won.
   *
   * @param result search result of Elastic Search
   * @param a_won did object A win?
   */
  saveSentences(result, a_won) {
    let i = 0;
    if (a_won) {
      for (const sentence of result['object 1 sentences']) {
        this.winner_sentex[i++] = this.clustererService.getCluster(
          sentence,
          this.winner_links,
          this.loser_links,
          this.finalAspDict,
          this.winner_obj,
          this.loser_obj
        );
      }
      i = 0;
      for (const sentence of result['object 2 sentences']) {
        this.loser_sentex[i++] = this.clustererService.getCluster(
          sentence,
          this.winner_links,
          this.loser_links,
          this.finalAspDict,
          this.winner_obj,
          this.loser_obj
        );
      }
    } else {
      for (const sentence of result['object 1 sentences']) {
        this.loser_sentex[i++] = this.clustererService.getCluster(
          sentence,
          this.winner_links,
          this.loser_links,
          this.finalAspDict,
          this.winner_obj,
          this.loser_obj
        );
      }
      i = 0;
      for (const sentence of result['object 2 sentences']) {
        this.winner_sentex[i++] = this.clustererService.getCluster(
          sentence,
          this.winner_links,
          this.loser_links,
          this.finalAspDict,
          this.winner_obj,
          this.loser_obj
        );
      }
    }
  }

  /**
   * Checks if the user entered something in both the first and the second object fields.
   *
   * @returns true, if the user entered something in both fields, false if not
   */
  objectsEntered() {
    return this.object_A !== '' && this.object_B !== '';
  }

  /**
   * Calls compare() if the user entered something in both the first and the second object fields.
   *
   */
  compIfEntered() {
    if (this.objectsEntered()) {
      this.compare();
    }
  }

  /**
   * Adds an aspect to the list of currently shown aspects.
   *
   */
  addAspect() {
    this.aspects.push(this.aspects[this.aspects.length - 1] + 1);
    this.weightDict[this.aspects[this.aspects.length - 1]] = 1;
  }

  /**
   * Removes an aspect from the list of currently shown aspects which makes the UI remove this
   * aspect row.
   *
   * @param aspect the aspect row to be removed, given as a number
   */
  removeAspect(aspect) {
    if (this.aspects.length > 1) {
      const index = this.aspects.indexOf(aspect, 0);
      if (index > -1) {
        this.aspects.splice(index, 1);
      }
    } else {
      this.aspectDict[this.aspects[0]] = '';
    }
  }

  /**
   * Shows 10 more sentences in the result table for both objects or, if an object has less than 10
   * sentences left to be shown, instead only the remaining sentences will be added.
   *
   */
  show_more_sentences() {
    let i1 = 0;
    const minW = Math.min(
      10,
      Object.keys(this.winner_sentex).length -
      this.sentence_show_numberlist_winner[
      this.sentence_show_numberlist_winner.length - 1
      ] -
      1
    );
    while (i1 < minW) {
      this.sentence_show_numberlist_winner.push(
        this.sentence_show_numberlist_winner[
        this.sentence_show_numberlist_winner.length - 1
        ] + 1
      );
      i1++;
    }
    let i2 = 0;
    const minL = Math.min(
      10,
      Object.keys(this.loser_sentex).length -
      this.sentence_show_numberlist_loser[
      this.sentence_show_numberlist_loser.length - 1
      ] -
      1
    );
    while (i2 < minL) {
      this.sentence_show_numberlist_loser.push(
        this.sentence_show_numberlist_loser[
        this.sentence_show_numberlist_loser.length - 1
        ] + 1
      );
      i2++;
    }
  }
}
