import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Result } from '../model/result';
import { Sentence } from '../model/sentence';

@Injectable()
export class HTTPRequestService {

  constructor(private httpClient: HttpClient) { }

  getScore(url: string) {
    return this.httpClient.get<Result>(url);
  }

  getSuggestions(url: string) {
    return this.httpClient.get<Result>(url);
  }

  /**
   * Requests the status of answer processing to show the user the progress.
   *
   * @param url to the backend status endpoint
   * @returns subscribable
   */
  getStatus(url: string) {
    return this.httpClient.get<string>(url);
  }

  removeStatus(url: string) {
    this.httpClient.delete<any>(url).subscribe();
  }

  register(url: string) {
    return this.httpClient.get<string>(url);
  }

  getContext(url: string) {
    return this.httpClient.get<Array<Sentence>>(url);
  }

  getSentences(url: string) {
    return this.httpClient.get<Array<Sentence>>(url);
  }
}
