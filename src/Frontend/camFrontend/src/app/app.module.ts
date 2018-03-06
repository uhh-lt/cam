import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { UrlBuilderComponent } from './url-builder/url-builder.component';

@NgModule({
  declarations: [AppComponent, UrlBuilderComponent],
  imports: [BrowserModule, HttpClientModule, FormsModule],
  providers: [UrlBuilderComponent],
  bootstrap: [AppComponent]
})
export class AppModule {}
