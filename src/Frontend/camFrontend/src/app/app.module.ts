import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { UrlBuilderService } from './shared/url-builder.service';
import { ClustererService } from './shared/clusterer.service';
import { HTTPRequestService } from './shared/http-request.service';
import { HeaderComponent } from './components/header/header.component';

@NgModule({
  declarations: [AppComponent, HeaderComponent],
  imports: [BrowserModule, HttpClientModule, FormsModule],
  providers: [UrlBuilderService, ClustererService, HTTPRequestService],
  bootstrap: [AppComponent]
})
export class AppModule { }
