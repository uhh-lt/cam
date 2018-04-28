import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  selectedTab = 'home';
  constructor() { }

  ngOnInit() {
  }

  setSelectedTab(tab: string) {
    this.selectedTab = tab;
  }



}
