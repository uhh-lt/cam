import { Component, Input } from '@angular/core';
import { UrlBuilderService } from './shared/url-builder.service';
import { HTTPRequestService } from './shared/http-request.service';

/**
 * UI for the Comparative Argument Machine. Currently everything is done by this one class --
showing the UI, reading the input and requesting the Elastic Search.
 *
 * @export
 * @class AppComponent
 */
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'CAM';
}
