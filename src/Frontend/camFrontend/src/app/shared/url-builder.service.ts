import { Injectable } from '@angular/core';

@Injectable()
export class UrlBuilderService {

  constructor() { }
  /**
    *  The name of the backend server.
    */
  HOSTNAME_DEFAULT = 'http://localhost:10050/cam';
  HOSTNAME_ML = 'http://localhost:10050/cam/ml';

  /**
   * Builds the URL needed for communicating with the server and requesting the search.
   *
   * @param objA the first object entered by the user
   * @param objB the second object entered by the user
   * @param aspectList the list of aspects with their weights entered by the user
   * @param model the backend model to be used for the comparison
   * @returns the URL
   */
  buildURL(objA, objB, aspectList, model, fastSearch) {
    let URL = `${this.getUrlBase(model)}fs=${fastSearch}&objectA=${objA}&objectB=${objB}`;
    URL += this.addAspectURL(aspectList);
    return URL;
  }

  /**
   * Adds a URL part containing the aspects entered by the user to an already existing first part
   * of a URL.
   *
   * @param aspectList the list of aspects with their weights entered by the user
   * @returns the second part of the URL
   */
  private addAspectURL(aspectList) {
    let url_part = ``;
    let i = 1;
    Object.entries(aspectList).forEach(
      ([key, value]) => (url_part += `&aspect${i}=${key}&weight${i++}=${value}`)
    );
    return url_part;
  }

  /**
   * Selects the right url as basis
   *
   * @param model the backend model to be used for the comparison
   * @returns the url basis (HOSTNAME)
   */
  private getUrlBase(model: string) {
    if (model === 'default') {
      return `${this.HOSTNAME_DEFAULT}?`;
    } else if (model === 'ml1') {
      return `${this.HOSTNAME_ML}?model=bow&`;
    } else if (model === 'ml2') {
      return `${this.HOSTNAME_ML}?model=infersent&`;
    }
    console.error('Model was neither default nor machine_learning');
  }

  /**
   * Builds the url to request the status of the answer preparation.
   *
   * @param model the backend model to be used for the comparison
   * @return status request url
   */
  getStatusUrl(model: string) {
    return this.HOSTNAME_DEFAULT + '/status';
  }

}
