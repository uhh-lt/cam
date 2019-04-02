import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Result } from '../model/result';
import { Sentence } from '../model/sentence';

@Injectable()
export class HTTPRequestService {

  constructor(private http: HttpClient) { }

  getScore(url: string) {
    return this.http.get<Result>(url);
  }

  getSuggestions(url: string) {
    //return this.http.get('https://jsonplaceholder.typicode.com/todos/34', { headers: { 'Authorization': 'Basic cmVhZGVyOnJlYWRlcg==' } });
    return this.http.get(url, { headers: { 'Authorization': 'Basic cmVhZGVyOnJlYWRlcg==' } });  }

  /**
   * Requests the status of answer processing to show the user the progress.
   *
   * @param url to the backend status endpoint
   * @returns subscribable
   */
  getStatus(url: string) {
    return this.http.get<string>(url);
  }

  removeStatus(url: string) {
    this.http.delete<any>(url).subscribe();
  }

  register(url: string) {
    return this.http.get<string>(url);
  }

  getContext(url: string) {
    return this.http.get<Array<Sentence>>(url);
  }

  getSentences(url: string) {
    console.log(this.http.get<Array<Sentence>>(url));

    return this.http.get<Array<Sentence>>(url);
  }
}
