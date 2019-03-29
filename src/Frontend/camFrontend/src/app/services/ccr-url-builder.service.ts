import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CcrUrlBuilderService {

  constructor() { }
    /**
    *  The name of the backend server.
    */
  // private HOSTNAME_DEFAULT = 'http://localhost:5000/cam';
  private esHostname = 'http://ltdemos.informatik.uni-hamburg.de/depcc-index/';
  private index = 'depcc';
  private crawlDataRepos = '/_search?q=';
  private and = '"%20AND%20"';
  private fromSize = '")&from=0&size=10000'

  /**
   * Builds the URL needed for communicating with the server and requesting the search.
   *esHostname
   * @param objA the first object entered by the user
   * @param vs the versus word
   * @returns the URL
   */
  public buildCcrUrl(objA, vs) {
    return `${this.esHostname + this.index + this.crawlDataRepos}text:(\"${objA + this.and + vs + this.fromSize}`;
  }


}
