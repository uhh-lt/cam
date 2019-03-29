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
   * 
   * what really happenes: http://ltdemos.informatik.uni-hamburg.de/depcc-index/depcc/_search?q=text:(%22toyota%22%20AND%20%22vs%22)&from=0&size=10000
   * what should happen:   http://ltdemos.informatik.uni-hamburg.de/depcc-index/depcc/_search?q=text:("toyota"%20AND%20"vs")&from=0&size=10000
   */
  public buildCcrUrl(objA, vs) {
    return `${this.esHostname + this.index + this.crawlDataRepos}text:(\"${objA + this.and + vs + this.fromSize}`;
  }


}
