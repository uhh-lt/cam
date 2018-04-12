import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class HTTPRequestService {

  constructor(private httpClient: HttpClient) { }

  getScore(url: string) {
    return this.httpClient.get(url);
  }

}
