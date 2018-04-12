import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { UrlBuilderService } from './shared/url-builder.service';
import { ClustererService } from './shared/clusterer.service';
import { HTTPRequestService } from './shared/http-request.service';
import { HeaderComponent } from './components/header/header.component';
import { AboutComponent } from './components/about/about.component';
import { ApiInfoComponent } from './components/api-info/api-info.component';
import { ContactComponent } from './components/contact/contact.component';
import { UserInterfaceComponent } from './components/user-interface/user-interface.component';
import { ResultPresentationComponent } from './components/result-presentation/result-presentation.component';


const appRoute: Routes = [
  { path: '', component: UserInterfaceComponent},
  { path: 'About', component: AboutComponent},
  { path: 'API-Info', component: ApiInfoComponent},
  { path: 'Contact', component: ContactComponent}

];

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    AboutComponent,
    ApiInfoComponent,
    ContactComponent,
    UserInterfaceComponent,
    ResultPresentationComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    RouterModule.forRoot(appRoute)
  ],
  providers: [UrlBuilderService, ClustererService, HTTPRequestService],
  bootstrap: [AppComponent]
})
export class AppModule { }
