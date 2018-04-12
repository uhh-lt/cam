import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { UrlBuilderService } from './shared/url-builder.service';
import { ClustererService } from './shared/clusterer.service';
import { HttpRequestService } from './shared/http-request.service';

@NgModule({
  declarations: [AppComponent],
  imports: [BrowserModule, HttpClientModule, FormsModule],
  providers: [UrlBuilderService, ClustererService, HttpRequestService],
  bootstrap: [AppComponent]
})
export class AppModule { }
