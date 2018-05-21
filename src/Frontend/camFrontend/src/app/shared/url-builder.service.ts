import { Injectable } from '@angular/core';

@Injectable()
export class UrlBuilderService {

  constructor() { }
  /**
    *  The name of the server. Change this to 'http://127.0.0.1:5000/cam' if you want to communicate
    *  with your locally hosted server instead, to 'http://ltdemos.informatik.uni-hamburg.de/cam-api'
    *  if you want to communicate with ltdemos.
    */
  // HOSTNAME_DEFAULT = 'http://127.0.0.1:5000/cam';
  // HOSTNAME_ML = 'http://127.0.0.1:5000/cam/ml';

  HOSTNAME_DEFAULT = 'http://ltdemos.informatik.uni-hamburg.de/cam-api';
  HOSTNAME_ML = 'http://ltdemos.informatik.uni-hamburg.de/cam-api/ml';

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
    let URL = this.buildObjURL(objA, objB, this.getHostname(model), fastSearch);
    URL += this.addAspectURL(aspectList);
    return URL;
  }

  /**
   * Builds the first part of the URL containing the host address and the objects entered.
   *
   * @param objA the first object entered by the user
   * @param objB the second object entered by the user
   * @returns the first part of the URL
   */
  private buildObjURL(objA, objB, hostname, fastSearch) {
    return `${hostname}?fs=${fastSearch}&objectA=${objA}&objectB=${objB}`;
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
  private getHostname(model: string) {
    if (model === 'default') {
      return this.HOSTNAME_DEFAULT;
    } else if (model === 'machine_learning') {
      return this.HOSTNAME_ML;
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
