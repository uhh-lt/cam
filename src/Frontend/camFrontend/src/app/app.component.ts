import { Component, Input } from '@angular/core';
import { HttpClient } from '@angular/common/http'; // needed for the http.get method
import { UrlBuilderComponent } from './url-builder/url-builder.component';

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
  loadshow = false; // boolean that checks if the loading screen should be shown
  resshow = false; // boolean that checks if the result table should be shown
  rescount = 0; // total amount of sentences used for comparison
  object_A = ''; // the first object currently entered
  object_B = ''; // the second object currently entered
  winner_obj = ''; // the first object of the results shown
  loser_obj = ''; // the second object of the results shown
  winner_score = ''; // stores the score of the first object
  loser_score = ''; // stores the score of the second object
  winner_links = []; // stores the main links of the first object
  loser_links = []; // stores the main links of the second object
  winner_sentex = {}; // stores some example sentences for the first object
  loser_sentex = {}; // stores some example sentences for the second object
  sentence_show_numberlist = [1, 2, 3, 4, 5, 6, 7, 8, 9];

  constructor(
    private http: HttpClient,
    private urlbuilder: UrlBuilderComponent
  ) {}

  /**
   * Reads the input from the UI, starts the search request and calls the save method.
   */
  compare() {
    this.loadshow = true; // show the loading screen
    // reset everything to its default and hide the result table
    this.reset();
    // read the aspects entered by the user and store them with their weight
    for (const aspect of this.aspects) {
      if (this.aspectDict[aspect] !== undefined) {
        this.finalAspDict[this.aspectDict[aspect]] = this.weightDict[aspect];
      }
    }
    // read the objects entered, build the URL and start the search request
    this.http
      .get(
        this.urlbuilder.buildURL(
          this.object_A,
          this.object_B,
          this.finalAspDict
        )
      )
      .subscribe(async res => {
        await this.saveResult(res);
      });
  }

  /**
   * reset everything to its default and hide the result table.
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
    this.sentence_show_numberlist = [1, 2, 3, 4, 5, 6, 7, 8, 9];
  }

  /**
   * Saves the search result so that they can be shown in the UI.
   *
   * @param result the search results to be saved
   */
  saveResult(result) {
    this.resshow = true; // show the result table
    this.rescount =
      result['object 1 sentences'].length + result['object 2 sentences'].length;
    const a_won = result['score object 1'] > result['score object 2'];
    // save the winner
    if (a_won) {
      this.winner_obj = result['object 1'];
      this.loser_obj = result['object 2'];
    } else {
      this.winner_obj = result['object 2'];
      this.loser_obj = result['object 1'];
    }
    // save the scores
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
    // sort the main links for both objects by their values and save them
    if (a_won) {
      for (const link of result['main links object 1']) {
        this.winner_links.push(link);
      }
      for (const link of result['main links object 2']) {
        this.loser_links.push(link);
      }
    } else {
      for (const link of result['main links object 1']) {
        this.loser_links.push(link);
      }
      for (const link of result['main links object 2']) {
        this.winner_links.push(link);
      }
    }
    // save the sentences each of the objects has won
    let i = 0;
    if (a_won) {
      for (const sentence of result['object 1 sentences']) {
        this.winner_sentex[i++] = this.getCluster(sentence);
      }
      i = 0;
      for (const sentence of result['object 2 sentences']) {
        this.loser_sentex[i++] = this.getCluster(sentence);
      }
    } else {
      for (const sentence of result['object 1 sentences']) {
        this.loser_sentex[i++] = this.getCluster(sentence);
      }
      i = 0;
      for (const sentence of result['object 2 sentences']) {
        this.winner_sentex[i++] = this.getCluster(sentence);
      }
    }
    this.loadshow = false; // hide the loading screen
  }

  getCluster(sentence) {
    const wordList = sentence.match(/([A-Za-z]+)/g);
    const highlightList = this.winner_links
      .concat(this.loser_links)
      .concat(Object.keys(this.finalAspDict));
    highlightList.push(this.object_A);
    highlightList.push(this.object_B);
    const retDict = {};
    let i = 0;
    for (const word of wordList) {
      if (highlightList.includes(word)) {
        retDict[i] = { noHL: '' };
        if (this.winner_links.includes(word)) {
          retDict[i++] = { link: [word] };
          continue;
        }
        retDict[i] = { link: '' };
        if (this.loser_links.includes(word)) {
          retDict[i++] = { link: [word] };
          continue;
        }
        retDict[i] = { link: '' };
        if (Object.keys(this.finalAspDict).includes(word)) {
          retDict[i++] = { aspect: [word] };
          continue;
        }
        retDict[i] = { aspect: '' };
        if (word === this.object_A) {
          retDict[i++] = { winner: [word] };
          continue;
        }
        retDict[i] = { winner: '' };
        retDict[i++] = { loser: [word] };
        continue;
      }
      retDict[i++] = { noHL: [word] };
    }
    const retList = [];
    retList.push(retDict);
    retList.push(Array.from(Array(wordList.length).keys()));
    return retList;
  }

  /**
   * Checks if the user entered something in both the first and the second object fields.
   *
   * @returns true, if the user entered something in both fields, false if not
   */
  objectsEntered() {
    return this.object_A !== '' && this.object_B !== '';
  }

  compIfEntered() {
    if (this.objectsEntered()) {
      this.compare();
    }
  }

  /**
   * Adds an aspect to the list of currently shown aspects which makes the UI show a new aspect row
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

  show_more_sentences() {
    let i = 0;
    while (i < 10) {
      this.sentence_show_numberlist.push(
        this.sentence_show_numberlist[
          this.sentence_show_numberlist.length - 1
        ] + 1
      );
      i++;
    }
  }
}
