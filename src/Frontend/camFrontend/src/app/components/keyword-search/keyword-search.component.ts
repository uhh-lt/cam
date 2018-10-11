import { Component, OnInit } from '@angular/core';
import { HTTPRequestService } from '../../shared/http-request.service';
import { UrlBuilderService } from '../../shared/url-builder.service';
import { MatSnackBar } from '@angular/material';
import { Sentence } from '../../model/sentence';

@Component({
  selector: 'app-keyword-search',
  templateUrl: './keyword-search.component.html',
  styleUrls: ['./keyword-search.component.css']
})
export class KeywordSearchComponent implements OnInit {

  public hits = 0;
  public sentences = new Array<Sentence>();
  public keywords = [];
  public query = '';
  public showLoading = false;
  public sentQuery = false;

  constructor(private httpService: HTTPRequestService, private urlBuilderService: UrlBuilderService, private snackBar: MatSnackBar) { }

  ngOnInit() {
  }

  search(query: string) {
    this.query = query;
    const url = this.urlBuilderService.getKeywordSearchURL(query);
    this.getKeywords(query);
    this.showLoading = true;
    this.httpService.getSentences(url).subscribe(
      data => {
        this.showLoading = false;
        this.sentences = data;
        this.hits = this.sentences.length;
      },
      error => {
        this.snackBar.open('The API-Service seems to be unavailable at the moment :/', '', {
          duration: 3500,
        });
        console.error(error);
        this.showLoading = false;
      },
      () => {
        this.sentQuery = true;
      }
    );
  }

  getKeywords(query: string) {
    const queryWords = query.split(/AND|OR/);
    this.keywords = [];
    queryWords.forEach(word => {
      if (word !== 'AND' && word !== 'OR') {
        word = word.replace(new RegExp(/"|\(|\)/, 'ig'), '').trim();
        this.keywords.push(word);
      }
    });
  }
}
