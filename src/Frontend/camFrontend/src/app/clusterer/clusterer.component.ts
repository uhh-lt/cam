import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-clusterer',
  templateUrl: './clusterer.component.html',
  styleUrls: ['./clusterer.component.css']
})
export class ClustererComponent implements OnInit {
  constructor() {}

  ngOnInit() {}

  /**
   * Clusters a sentence, extracting all words and their highlight class. This is needed for
   * highlighting specific words within the result table.
   *
   * Note that we're not satisfied with the current implementation of highlighting. We thought that
   * this should have been possible with a very simple implementation but everything we tried --
   * passing strings containing <mark></mark> or <span></span> to innerHtml or ng-bind-html for
   * example -- didn't work. This may very well be caused by our inexperience with Angular/
   * typescript/html. After we couldn't find a simple solution we decided to use this very complex
   * implementation so that at least the functionality was there.
   *
   * @param sentence the sentence to be clustered
   * @returns a list containing two items: 1. a dictionary with the position of each word within
   * the sentence as key and another dictionary as value. This second dictionary contains the
   * highlight class as key and the word as value. 2. an array containing the numbers from 0 to the
   * amount of words within the sentence. This is needed for *ngFor within the html template.
   */
  getCluster(
    sentence,
    winner_links,
    loser_links,
    finalAspDict,
    object_A,
    object_B
  ) {
    const wordList = sentence.match(/([A-Za-z]+)/g); // extract the words
    // list containing all the words to be highlighted
    const highlightList = winner_links
      .concat(loser_links)
      .concat(Object.keys(finalAspDict));
    highlightList.push(object_A);
    highlightList.push(object_B);
    const retDict = {};
    let i = 0;
    for (const word of wordList) {
      if (highlightList.includes(word)) {
        // word needs to be highlighted
        // find the right highlight class for the word
        retDict[i] = { noHL: '' };
        if (winner_links.includes(word)) {
          retDict[i++] = { link: [word] };
          continue;
        }
        retDict[i] = { link: '' };
        if (loser_links.includes(word)) {
          retDict[i++] = { link: [word] };
          continue;
        }
        retDict[i] = { link: '' };
        if (Object.keys(finalAspDict).includes(word)) {
          retDict[i++] = { aspect: [word] };
          continue;
        }
        retDict[i] = { aspect: '' };
        if (word === object_A) {
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
}
