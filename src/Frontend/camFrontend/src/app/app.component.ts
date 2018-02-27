import { Component, Inject } from "@angular/core";
import { Http } from "@angular/http";
import "rxjs/add/operator/toPromise";

@Component({
  selector: "app-root",
  template: `
  <p>object 1: </p><input #objA>
  <p>object 2:</p><input #objB>
  <p>aspect:</p><input #asp>
  <p>weight:</p><input #wght>
  <button (click)="addAspect(asp.value, wght.value)">Add aspect</button>
  <p>chosen aspects: {{aspects}}</p>
  <button (click)="compare(objA.value, objB.value)">Compare</button>
  {{json}}`,
  styleUrls: ["./app.component.css"]
})
export class AppComponent {
  title = "CAM";
  aspects = "";
  aspectList = {};
  json = "";

  constructor(private http: Http) {}

  compare(objA, objB, aspectList) {
    console.log(this.buildURL(objA, objB, aspectList));
    return this.http.get(this.buildURL(objA, objB, aspectList));
  }
  buildURL(objA, objB, aspectList) {
    let URL = this.buildObjURL(objA, objB);
    URL += this.addAspectURL(aspectList);
    return URL;
  }

  buildObjURL(objA, objB) {
    return `http://127.0.0.1:5000/cam?objectA=${objA}&objectB=${objB}`;
  }

  addAspectURL(aspectList) {
    let url_part = ``;
    let i = 1;
    Object.keys(aspectList).forEach(key => {
      url_part += `&aspect${i}=${key}&weight${i}=${aspectList[key]}`;
      i++;
    });
    return url_part;
  }

  addAspect(aspect, weight) {
    if (this.aspects !== "") {
      this.aspects += `,`;
    }
    this.aspects += `${aspect}(${weight})`;
    this.aspectList[aspect] = weight;
  }

  private handleError(error: any): Promise<any> {
    console.error("An error occurred", error); // for demo purposes only
    return Promise.reject(error.message || error);
  }
}
