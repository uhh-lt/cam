/**
 * UI for the Comparative Argument Machine. Currently everything is done by this one class --
showing the UI, reading the input and requesting the Elastic Search.
 */

import { Component } from "@angular/core";
import { HttpClient } from "@angular/common/http"; // needed for the http.get method

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"]
})
export class AppComponent {
  title = "CAM";
  aspects = [1]; // the rows of aspects currently shown in the UI
  aspectDict = {}; // the aspects currently entered
  weightDict = { 1: 1 }; // the weightings of the aspects currently chosen with the sliders
  resshow = false; // boolean that checks if the result table should be shown
  loadshow = false; // boolean that checks if the loading screen should be shown
  object_A = ""; // the first object currently entered
  object_B = ""; // the second object currently entered
  A_won = ""; // stores if the first object is the winner or not
  B_won = ""; // stores if the second object is the winner or not
  A_score = 0; // stores the score of the first object
  B_score = 0; // stores the score of the second object
  A_mainaspects = ""; // stores the main aspects of the first object
  B_mainaspects = ""; // stores the main aspects of the second object
  A_sentex = {}; // stores some example sentences for the first object
  B_sentex = {}; // stores some example sentences for the second object

  constructor(private http: HttpClient) {}

  /**
   * Reads the input from the UI, starts the search request and calls the save method.
   *
   * @memberof AppComponent
   */
  compare() {
    this.loadshow = true; // show the loading screen
    // reset everything to its default and hide the result table
    this.resshow = false;
    this.A_won = "";
    this.B_won = "";
    this.A_mainaspects = "";
    this.B_mainaspects = "";
    this.A_sentex = {};
    this.B_sentex = {};
    const finalAspDict = {};
    // read the aspects entered by the user and store them with their weight
    for (const aspect of this.aspects) {
      finalAspDict[this.aspectDict[aspect]] = this.weightDict[aspect];
    }
    // read the objects entered, build the URL and start the search request
    this.http
      .get(this.buildURL(this.object_A, this.object_B, finalAspDict))
      .subscribe(async res => {
        await this.saveResult(res);
      });
  }

  /**
   * Saves the search result so that they can be shown in the UI.
   *
   * @param {any} result the search results that should be saved
   * @memberof AppComponent
   */
  saveResult(result) {
    this.resshow = true; // show the result table
    // save the scores
    this.A_score = result["score object 1"];
    this.B_score = result["score object 2"];
    // save the winner
    if (this.A_score > this.B_score) {
      this.A_won = "X";
    } else if (this.A_score < this.B_score) {
      this.B_won = "X";
    } else {
      this.A_won = "X";
      this.B_won = "X";
    }
    // sort the main aspects for both objects by their values and save them
    const A_aspkeys = Object.keys(result["main aspects object 1"]);
    for (const _i of [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) {
      let maxi = 0;
      let maxkey = "";
      for (const key of A_aspkeys) {
        if (result["main aspects object 1"][key] > maxi) {
          maxi = result["main aspects object 1"][key];
          maxkey = key;
        }
      }
      if (A_aspkeys.length > 0) {
        this.A_mainaspects += `${maxkey}(${maxi})`;
        const index = A_aspkeys.indexOf(maxkey, 0);
        if (index > -1) {
          A_aspkeys.splice(index, 1);
        }
        this.A_mainaspects += `, `;
      } else {
        break;
      }
    }
    const B_aspkeys = Object.keys(result["main aspects object 2"]);
    for (const _i of [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) {
      let maxi = 0;
      let maxkey = "";
      for (const key of B_aspkeys) {
        if (result["main aspects object 2"][key] > maxi) {
          maxi = result["main aspects object 2"][key];
          maxkey = key;
        }
      }
      if (B_aspkeys.length > 0) {
        this.B_mainaspects += `${maxkey}(${maxi})`;
        const index = B_aspkeys.indexOf(maxkey, 0);
        if (index > -1) {
          B_aspkeys.splice(index, 1);
        }
        this.B_mainaspects += `, `;
      } else {
        break;
      }
    }
    // save the sentences each of the objects has won
    let i = 0;
    for (const sentence of result["object 1 sentences"]) {
      this.A_sentex[i++] = sentence;
    }
    i = 0;
    for (const sentence of result["object 2 sentences"]) {
      this.B_sentex[i++] = sentence;
    }
    this.loadshow = false; // hide the loading screen
  }

  buildURL(objA, objB, aspectList) {
    let URL = this.buildObjURL(objA, objB);
    URL += this.addAspectURL(aspectList);
    return URL;
  }

  buildObjURL(objA, objB) {
    return `http://localhost:5000/cam?objectA=${objA}&objectB=${objB}`;
  }

  addAspectURL(aspectList) {
    let url_part = ``;
    let i = 1;
    Object.entries(aspectList).forEach(
      ([key, value]) => (url_part += `&aspect${i}=${key}&weight${i++}=${value}`)
    );
    return url_part;
  }

  objectsEntered() {
    return this.object_A !== "" && this.object_B !== "";
  }

  addAspect() {
    this.aspects.push(this.aspects[this.aspects.length - 1] + 1);
    this.weightDict[this.aspects[this.aspects.length - 1]] = 1;
  }

  removeAspect(aspect) {
    if (this.aspects.length > 1) {
      const index = this.aspects.indexOf(aspect, 0);
      if (index > -1) {
        this.aspects.splice(index, 1);
      }
    } else {
      this.aspectDict[this.aspects[0]] = "";
    }
  }
}
