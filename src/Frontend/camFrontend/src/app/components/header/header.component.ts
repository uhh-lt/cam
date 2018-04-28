import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  private selectedTab = 'home';
  constructor() { }

  ngOnInit() {
  }

  private setSelectedTab(tab: string) {
    this.selectedTab = tab;
  }



}
