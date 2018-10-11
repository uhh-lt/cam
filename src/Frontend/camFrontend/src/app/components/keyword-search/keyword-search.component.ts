import { Component, OnInit } from '@angular/core';
import { HTTPRequestService } from '../../shared/http-request.service';
import { UrlBuilderService } from '../../shared/url-builder.service';

@Component({
  selector: 'app-keyword-search',
  templateUrl: './keyword-search.component.html',
  styleUrls: ['./keyword-search.component.css']
})
export class KeywordSearchComponent implements OnInit {

  public hits = 0;
  public sentences = new Array<string>();
  public keywords = [];
  public query = '';

  constructor(private httpService: HTTPRequestService, private urlBuilderService: UrlBuilderService) { }

  ngOnInit() {
  }

  search(query: string) {
    this.query = query;
    const url = this.urlBuilderService.getKeywordSearchURL(query);
    this.getKeywords(query);
    this.httpService.getSentences(url).subscribe(
      data => {
        this.sentences = data;
        this.hits = this.sentences.length;
      },
      error => {
        console.error(error);
      },
      () => {
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
