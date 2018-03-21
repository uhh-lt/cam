import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { UrlBuilderComponent } from './url-builder/url-builder.component';
import { ClustererComponent } from './clusterer/clusterer.component';

@NgModule({
  declarations: [AppComponent, UrlBuilderComponent, ClustererComponent],
  imports: [BrowserModule, HttpClientModule, FormsModule],
  providers: [UrlBuilderComponent, ClustererComponent],
  bootstrap: [AppComponent]
})
export class AppModule {}
