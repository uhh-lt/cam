import { BrowserModule, HAMMER_GESTURE_CONFIG } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { FlexLayoutModule } from '@angular/flex-layout';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ScrollToModule } from '@nicky-lenaers/ngx-scroll-to';

import { AppComponent } from './app.component';
import { UrlBuilderService } from './shared/url-builder.service';
import { HTTPRequestService } from './shared/http-request.service';
import { HeaderComponent } from './components/header/header.component';
import { AboutComponent } from './components/about/about.component';
import { ApiInfoComponent } from './components/api-info/api-info.component';
import { ContactComponent } from './components/contact/contact.component';
import { UserInterfaceComponent } from './components/user-interface/user-interface.component';
import { ResultPresentationComponent } from './components/result-presentation/result-presentation.component';


import { MaterialModule } from './material/material.module';
import { MarkClassesPipe } from './pipes/mark-classes/mark-classes.pipe';
import { MultiselectChiplistComponent } from './components/result-presentation/multiselect-chiplist/multiselect-chiplist.component';
import { SentenceFilterPipe } from './pipes/sentence-filter/sentence-filter.pipe';
import { ScorePresentationComponent } from './components/result-presentation/score-presentation/score-presentation.component';
import { SentencePresentationComponent } from './components/result-presentation/sentence-presentation/sentence-presentation.component';
import { ContextPresentationComponent } from './components/result-presentation/context-presentation/context-presentation.component';
import { KeywordSearchComponent } from './components/keyword-search/keyword-search.component';
import { MarkQueryWordsPipe } from './components/keyword-search/mark-query-words.pipe';

const appRoute: Routes = [
  { path: '', component: UserInterfaceComponent },
  { path: 'Search', component: KeywordSearchComponent },
  { path: 'About', component: AboutComponent },
  { path: 'API-Info', component: ApiInfoComponent },
  { path: 'Contact', component: ContactComponent }

];

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    AboutComponent,
    ApiInfoComponent,
    ContactComponent,
    UserInterfaceComponent,
    ResultPresentationComponent,
    MarkClassesPipe,
    MultiselectChiplistComponent,
    SentenceFilterPipe,
    ScorePresentationComponent,
    SentencePresentationComponent,
    ContextPresentationComponent,
    KeywordSearchComponent,
    MarkQueryWordsPipe
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FlexLayoutModule,
    HttpClientModule,
    FormsModule,
    RouterModule.forRoot(appRoute, { useHash: true }),
    MaterialModule,
    ScrollToModule.forRoot()
  ],
  entryComponents: [ContextPresentationComponent],
  providers: [UrlBuilderService, HTTPRequestService],
  bootstrap: [AppComponent]
})
export class AppModule { }
