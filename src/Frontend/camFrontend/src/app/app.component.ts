import { Component, Inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import "rxjs/add/operator/toPromise";

import { map } from "rxjs/operators";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"]
})
export class AppComponent {
  title = "CAM";
  aspects = "";
  aspectList = {};
  json = { "object 1": "test", "object 2": "test2" };
  results = {};
  resshow = false;
  object_A = "";
  object_B = "";
  A_won = false;
  B_won = false;
  A_score = 0;
  B_score = 0;
  A_mainaspects = "";
  B_mainaspects = "";

  constructor(private http: HttpClient) {}

  compare(objA, objB) {
    this.http
      .get(this.buildURL(objA, objB, this.aspectList))
      .subscribe(async res => {
        await this.saveResult(res);
      });
  }

  saveResult(result) {
    this.results = result;
    this.resshow = true;
    this.object_A = this.results["object 1"];
    this.object_B = this.results["object 2"];
    this.A_score = this.results["score object 1"];
    this.B_score = this.results["score object 2"];
    if (this.A_score > this.B_score) {
      this.A_won = true;
    } else if (this.A_score < this.B_score) {
      this.B_won = true;
    } else {
      this.A_won = true;
      this.B_won = true;
    } /* main aspects not working yet
    let aspA = result["main aspects object 1"].keys;
    console.log(aspA);
    let aspB = result["main aspects object 2"].keys;
    for (const key of aspA) {
      this.A_mainaspects += `${key}(${result["main aspects object 1"][key]}), `;
    }
    for (const key of aspB) {
      this.B_mainaspects += `${key}(${result["main aspects object 2"][key]}), `;
    }
    console.log(this.A_mainaspects); */
  }

  buildURL(objA, objB, aspectList) {
    let URL = this.buildObjURL(objA, objB);
    URL += this.addAspectURL(aspectList);
    return URL;
  }

  buildObjURL(objA, objB) {
    return `http://localhost:5000/cam?objectA=${objA}&objectB=${objB}`;
  }

  addAspectURL(aspectList) {
    let url_part = ``;
    let i = 1;
    Object.entries(aspectList).forEach(
      ([key, value]) => (url_part += `&aspect${i}=${key}&weight${i++}=${value}`)
    );
    return url_part;
  }

  addAspect(aspect, weight) {
    if (this.aspects !== "") {
      this.aspects += `,`;
    }
    this.aspects += `${aspect}(${weight})`;
    this.aspectList[aspect] = weight;
  }
}
